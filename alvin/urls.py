from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from alvin.core.models import Item, Batch, ItemForm, BatchForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

item_update_dict = { 
    'form_class': ItemForm,
}

item_list_dict = { 
    'queryset': Item.objects.all(), 
}

batch_list_dict = {
    'queryset': Batch.objects.all(),
}

batch_update_dict = {
    'form_class': BatchForm,
}

urlpatterns = patterns('',

    # Example:
    # (r'^alvin/', include('alvin.foo.urls')),
    (r'^$', 'alvin.core.views.main'),
    (r'^logout/$', 'alvin.core.views.logout_passthrough'),
    (r'^login/$', 'alvin.core.views.handle_login'),
    #(r'^item/$', 'alvin.core.views.get_items'),
    (r'^item/$', 'django.views.generic.list_detail.object_list', item_list_dict, 'item_list'), 
    #(r'^item/new/$', 'alvin.core.views.item_new'),
    #(r'^item/(?P<item_id>.+)/$', 'alvin.core.views.item_detail'),
    (r'^item/new$', 'django.views.generic.create_update.create_object', item_update_dict, 'new_item'), 
    (r'^item/(?P<object_id>.+)/$', 'django.views.generic.create_update.update_object', item_update_dict, 'item_detail'), 


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
