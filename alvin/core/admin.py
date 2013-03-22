from alvin.core.models import Collection 
from alvin.core.models import Item 
from alvin.core.models import Digital_Collection 
from alvin.core.models import File 
from alvin.core.models import Media_Object 
from alvin.core.models import SubjectLocation 
from alvin.core.models import Name 
from alvin.core.models import Format 
from alvin.core.models import Batch 
from alvin.core.models import Subject 
from alvin.core.models import Genre 
from alvin.core.models import TypeOfResource 
from alvin.core.models import Language
from alvin.core.models import GeoTag
from django.contrib import admin
from django.conf import settings

#def thumbnail(self):
#        url = '%s%s%s' % (settings.MEDIA_URL, 'thumbs/', self.get_thumb())
#        return '<img src="%s"/>' % (url,)
#
#thumbnail.short_description = 'Image thumbnail'
#thumbnail.allow_tags = True

class GeoTagInline(admin.StackedInline):
    model = GeoTag
    max_num = 1

class FileInline(admin.TabularInline):
    model = File

class MediaObjectInline(admin.StackedInline):
    model = Media_Object
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail',)
    list_display = ('thumbnail', 'identifier', 'title', 'format', 'source_collection', 'scanning_status', 'processing_status',)
    list_filter = ('batches', 'source_collection', 'digital_collection', )
    list_per_page = 25
    search_fields = ('identifier', 'title', 'description',)
    filter_horizontal = ('batches', 'genres', 'subjects', 'creators', 'contributors',)
    inlines = [GeoTagInline, MediaObjectInline]
    fieldsets = (
        ('Basic Fields', {
            'fields': ('identifier', 'title', 'description', ('date', 'date_qualifier'), 'creators', 'contributors','source_collection')
        }),
        ('Subjects', {
            'classes': ('collapse', 'wide'),
            'fields': ('subjects',)
        }),
        ('Physical Description', {
            'classes': ('collapse',),
            'fields': ('type', 'format', 'extent', 'publisher', 'language', 'source_id')
        }),
        ('Rights Information', {
            'classes': ('collapse',),
            'fields': ('copyright_status', 'publication_status', 'copyright_holder', 'copyright_notes', 'restriction_status', 'restriction_notes', 'release_forms',)
        }),
        ('Location Information', {
            'classes': ('collapse',),
            'fields': ('subject_location', 'address',)
        }),
        ('Workflow Information', {
            'classes': ('collapse',),
            'fields': (('scanning_status', 'processing_status', 'completed_by'), ('digital_collection', 'date_digitized', 'digital_notes'),)
        }),
    )
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'related_aat_term_notes')
    

admin.site.register(Collection)
admin.site.register(Item, ItemAdmin)
admin.site.register(Digital_Collection)
admin.site.register(File)
admin.site.register(Media_Object)
admin.site.register(SubjectLocation)
admin.site.register(Name)
admin.site.register(Format)
admin.site.register(Batch)
admin.site.register(Subject)
admin.site.register(Genre, GenreAdmin)
admin.site.register(TypeOfResource)
admin.site.register(Language)
admin.site.register(GeoTag)
