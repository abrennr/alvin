from django.template import Context, loader, RequestContext
from alvin.core.models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse

def handle_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                t = loader.get_template('alvin/main.html')
                c = RequestContext(request, { })
                return HttpResponse(t.render(c))
            else:
                # TODO: Return a 'disabled account' error message
                return HttpResponseRedirect(reverse('alvin.core.views.handle_login'))
        else:
            # TODO: Return 'invalid login' error message
            return HttpResponseRedirect(reverse('alvin.core.views.handle_login'))
    else:
        t = loader.get_template('alvin/login.html')
        c = RequestContext(request, { })
        return HttpResponse(t.render(c))

def logout_passthrough(request):
    logout(request)
    t = loader.get_template('alvin/main.html')
    c = RequestContext(request, { })
    return HttpResponse(t.render(c))

def main(request):
    item_count = Item.objects.count()
    file_count = File.objects.count()
    batch_count = Batch.objects.count()
    coll_count = Collection.objects.count()
    #last_five_transactions = Transaction.objects.order_by('timestamp').reverse()[:5]
    t = loader.get_template('alvin/main.html')
    c = RequestContext(request, {
    'items': item_count,
    'files': file_count,
    'batches': batch_count,
    'colls': coll_count,
    #'last_five': last_five_transactions,
    })
    return HttpResponse(t.render(c))

def get_instance_fields_as_tuples(instance):
    tupled_instance = []
    for f in instance._meta.fields:
        tupled_instance.append((f.name.replace('_', ' '), getattr(instance, f.name)))
    return tupled_instance 

def get_paged_items(items, request):
    paginator = Paginator(items, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    return paginator.page(page)

def get_facet_block(items_queryset, facet_fields, request):
    facet_block = {}
    for facet_field in facet_fields:
        this_facet_dict = {} 
        # if there's currently a facet selected, add an option to clear
        if facet_field in request.GET.keys() and request.GET[facet_field]:
            this_query_dict = request.GET.copy()
            this_query_dict.__setitem__(facet_field, '')
            this_facet_dict['[clear selection]'] = this_query_dict.urlencode() 
        # get the distinct values for this field in the queryset
        values_query_set = items_queryset.order_by().values(facet_field).distinct()
        for value_dict in values_query_set:
            this_value = value_dict[facet_field]
            # get the count of matching objects
            kwargs = { facet_field:this_value }
            count = items_queryset.filter(**kwargs).count() 
            # get the label for the matching field value.  In order to handle related object fields 
            # that would otherwise be id values, we do the __unicode__ method to get the name
            try:
                label = items_queryset.order_by().filter(**kwargs)[0].__getattribute__(facet_field).__unicode__()
            except:
                try:
                    label = items_queryset.order_by().filter(**kwargs)[0].__getattribute__(facet_field)
                except:
                    label = 'None'
            this_query_dict = request.GET.copy()
            this_query_dict.__setitem__(facet_field, this_value)
            key = '%s (%s)' % (label, count)
            this_facet_dict[key] = this_query_dict.urlencode() 
        facet_block[facet_field] = this_facet_dict
    return facet_block

def get_items(request):
    items = ItemFilter(request.GET, queryset=Item.objects.all()).qs
    if 'q' in request.GET:
        field_lookup = '%s__icontains' % (request.GET['lookup'],)
        field_value = request.GET['q']
        kwargs = { str(field_lookup):field_value }
        items =  items.filter(**kwargs)
        if items.count() == 1:
            return HttpResponseRedirect(reverse('alvin.core.views.item_detail', args=[items[0].identifier]))

    paged_items = get_paged_items(items, request)
    facet_block = get_facet_block(items, Item.Facet.fields, request)
#    batch_facet = []
#    for b in Batch.objects.all():
#        b.count = items.filter(batch=b).count() 
#        if b.count > 0:
#            batch_facet.append(b)
#    collection_facet = []
#    for c in Collection.objects.all():
#        c.count = items.filter(collection=c).count() 
#        if c.count > 0:
#            collection_facet.append(c)
#    digital_collection_facet = []
#    for dc in Digital_Collection.objects.all():
#        dc.count = items.filter(digital_collection=dc).count()
#        if dc.count > 0: 
#            digital_collection_facet.append(dc)
    t = loader.get_template('alvin/item_list.html')
    c = RequestContext(request, { 
        'items' : paged_items, 
        'facet_block': facet_block,
    })
    return HttpResponse(t.render(c))

def item_new(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('alvin.core.views.item_detail', args=[request.POST['identifier']]))
    else:
        form = ItemForm()
        t = loader.get_template('alvin/item.html')
        c = RequestContext(request, { 'alvin_item_form' : form, })
        return HttpResponse(t.render(c))


def item_detail(request, item_id):
    if request.method == 'POST': # update of an existing item
        item = Item.objects.get(identifier=request.POST['identifier'])
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    item = Item.objects.get(identifier=item_id)
    fields = get_instance_fields_as_tuples(item)
    form = ItemForm(instance=item)
    t = loader.get_template('alvin/item.html')
    c = RequestContext(request, { 'item':item, 'alvin_item_form' : form, 'static_fields' : fields, } )
    return HttpResponse(t.render(c))

