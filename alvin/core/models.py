from django.db import models
from django import forms
import django_filters

MIME_TYPE_CHOICES = (
    ('IMAGE_TIFF', 'image/tiff'),
    ('IMAGE_JPEG', 'image/jpeg'),
    ('IMAGE_JP2', 'image/jp2'),
    ('IMAGE_GIF', 'image/gif'),
    ('TEXT_CSV', 'text/csv'),
    ('TEXT_HTML', 'text/html'),
    ('TEXT_XML', 'text/xml'),
    ('APPLICATION_ZIP', 'application/zip'),
    ('APPLICATION_PDF', 'application/pdf'),
)

FILE_USE_CHOICES = (
    ('MASTER', 'master'),
    ('TARGET', 'target'),
    ('THUMB', 'thumbnail'),
    ('MARCXML', 'MARCXML'),
    ('FGDC', 'FGDC'),
    ('KML', 'KML'),
    ('VRA_CORE', 'VRA Core'),
    ('MODS', 'MODS'),
    ('DC', 'Dublin Core'),
    ('PDF', 'PDF'),
    ('METS', 'METS'),
    ('EAD', 'EAD'),
    ('COPYRIGHTMD', 'copyrightMD'),
    ('THUMB', 'thumbnail'),
    ('OCR_ZIP', 'ocr - zipped'),
    ('OTHER', 'other'),
)

ITEM_TYPE_CHOICES = (
    ('image', 'image'),
    ('audio', 'audio'),
    ('video', 'video'),
)

NAME_TYPE_CHOICES = (
    ('personal', 'personal'),
    ('corporate', 'corporate'),
    ('conference', 'conference'),
    ('family', 'family'),
)

COPYRIGHT_STATUS_VALUES = (
    ('copyrighted', 'copyrighted'),
    ('pd', 'public domain'),
    ('pd_usfed', 'public domain - us federal document'),
    ('pd_holder', 'public domain - dedicated by rights holder'),
    ('pd_expired', 'public domain - expired copyright'),
    ('unknown', 'unknown')
)

PUBLICATION_STATUS_VALUES = (
    ('published', 'published'),
    ('unpublished', 'unpublished'),
    ('unknown', 'unknown')
)

class Collection(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_member_item_count(self):
        """Gets count of items that are a member of this collection"""
        return Item.objects.filter(collection=self).count()

    class Meta:
        ordering = ["identifier"]

class Digital_Collection(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_member_item_count(self):
        """Gets count of items that are a member of this digital collection"""
        return Item.objects.filter(digital_collection=self).count()

    class Meta:
        ordering = ["identifier"]

class Batch(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    def get_member_item_count(self):
        """Gets count of items that are a member of this digital collection"""
        return Item.objects.filter(batch=self).count()

    class Meta:
        ordering = ["name"]

class Format(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Creator(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True, choices=NAME_TYPE_CHOICES)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Item(models.Model):
    # basic item descriptive metadata
    identifier = models.CharField(max_length=255, unique=True) 
    type = models.CharField(max_length=255, choices=ITEM_TYPE_CHOICES) 
    batch = models.ForeignKey(Batch, blank=True, null=True) 
    title = models.CharField(max_length=255) 
    creator = models.ForeignKey(Creator, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)
    normalized_date = models.CharField(max_length=255, blank=True, null=True) 
    display_date = models.CharField(max_length=255, blank=True, null=True) 
    format = models.ForeignKey(Format, blank=True, null=True)
    subject = models.TextField(blank=True, null=True) 
    # previously "rights", change to copyrightMD style
    rights = models.CharField(max_length=255, blank=True, null=True) 
    copyright_status = models.CharField(max_length=255, choices=COPYRIGHT_STATUS_VALUES, default='unknown') 
    publication_status = models.CharField(max_length=255, choices=PUBLICATION_STATUS_VALUES, default='unknown') 
    copyright_holder = models.CharField(max_length=255, blank=True, null=True) 
    copyright_notes = models.CharField(max_length=255, blank=True, null=True) 
    collection = models.ForeignKey(Collection, blank=True, null=True) 
    digital_collection = models.ForeignKey(Digital_Collection, blank=True, null=True) 
    image_number = models.CharField(max_length=255, blank=True, null=True) 
    location = models.ForeignKey(Location, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    notes = models.TextField(blank=True, null=True) 
    image_name = models.CharField(max_length=255, blank=True, null=True) 
    ordering_information = models.CharField(max_length=255, blank=True, null=True) 
    date_added = models.CharField(max_length=255, blank=True, null=True) 
    timestamp = models.CharField(max_length=255, blank=True, null=True) 
    date_revised = models.CharField(max_length=255, blank=True, null=True) 
    scanning_status = models.CharField(max_length=255, blank=True, null=True) 
    processing_status = models.CharField(max_length=255, blank=True, null=True) 
    completed_by = models.CharField(max_length=255, blank=True, null=True) 
    digitized_date = models.CharField(max_length=255, blank=True, null=True) 
    date_digitized = models.CharField(max_length=255, blank=True, null=True) 
    digital_notes = models.CharField(max_length=255, blank=True, null=True) 

    def __unicode__(self):
        return self.identifier
  
    def get_thumb(self):
        try:
            if self.type in ['audio', 'video']:
                filename =  Media_Object_File.objects.filter(media_object__item=self)[0].name
            else:
                filename =  Image_Item_File.objects.filter(image_item=self)[0].name
            thumb_filename = filename.replace('.tif', '.jpg')
            thumb_filename = thumb_filename.replace('.TIF', '.jpg')
            if len(thumb_filename) < 1:
                return None
            else:
                return thumb_filename
        except:
            return None 

    def get_path(self):
        try:
            filepath =  File.objects.filter(item_file__item=self)[0].path
            return filepath
        except:
            return None 

    class Meta:
        ordering = ["identifier"]
    
    class Facet:    
        fields = ['collection', 'digital_collection', ]

class Media_Object(models.Model):
    item = models.ForeignKey(Item)
    identifier = models.CharField(max_length=255, unique=True) 
    title = models.CharField(max_length=255) 
    creator = models.ForeignKey(Creator, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)
    normalized_date = models.CharField(max_length=255, blank=True, null=True) 
    display_date = models.CharField(max_length=255, blank=True, null=True) 
    format = models.ForeignKey(Format, blank=True, null=True)

    def inherit_from_parent(self, override_existing=False):
        if not self.title or override_existing:
            self.title = self.item.title
        if not self.creator or override_existing:
            self.creator = self.item.creator
        if not self.description or override_existing:
            self.description = self.item.description
        if not self.normalized_date or override_existing:
            self.normalized_date = self.item.normalized_date
        if not self.display_date or override_existing:
            self.display_date = self.item.display_date
        if not self.format or override_existing:
            self.format = self.item.format

class File(models.Model):
    name = models.CharField(max_length=255) 
    path = models.CharField(max_length=255, blank=True, null=True)
    size_bytes = models.IntegerField(blank=True, null=True, editable=False)
    mime_type = models.CharField(max_length=255, choices=MIME_TYPE_CHOICES, blank=True, null=True)
    use = models.CharField(max_length=255, choices=FILE_USE_CHOICES, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Media_Object_File(File):
    media_object = models.ForeignKey(Media_Object)

class Image_Item_File(File):
    image_item = models.ForeignKey(Item)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item 
   
class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator 
   
class FormatForm(forms.ModelForm):
    class Meta:
        model = Format 
   
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location 
   
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection 
   
class Digital_CollectionForm(forms.ModelForm):
    class Meta:
        model = Digital_Collection 
   
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch 

class MediaObjectFileForm(forms.ModelForm):
    class Meta:
        model = Media_Object_File
   
class ImageItemFileForm(forms.ModelForm):
    class Meta:
        model = Image_Item_File
   
class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = Item.Facet.fields


