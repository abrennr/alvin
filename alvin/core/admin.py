from alvin.core.models import Collection 
from alvin.core.models import Item 
from alvin.core.models import Digital_Collection 
from alvin.core.models import File 
from alvin.core.models import Media_Object 
from alvin.core.models import Location 
from alvin.core.models import Creator 
from alvin.core.models import Format 
from alvin.core.models import Batch 
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    list_filter = ('collection', 'digital_collection', 'batch')
    search_fields = ('identifier',)
    
admin.site.register(Collection)
admin.site.register(Item, ItemAdmin)
admin.site.register(Digital_Collection)
admin.site.register(File)
admin.site.register(Media_Object)
admin.site.register(Location)
admin.site.register(Creator)
admin.site.register(Format)
admin.site.register(Batch)
