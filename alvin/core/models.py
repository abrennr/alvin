from django.db import models
from django.conf import settings
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
    pref_cite = models.TextField(blank=True)

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
    description = models.TextField(blank=True)

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

class SubjectLocation(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Name(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, choices=NAME_TYPE_CHOICES)
    viaf_uri = models.URLField(verify_exists=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class TypeOfResource(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Genre(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(TypeOfResource)
    notes = models.TextField(blank=True)
    related_marcgt_term = models.CharField(max_length=255, blank=True)
    related_aat_term = models.CharField(max_length=255, blank=True)
    related_aat_term_id = models.CharField(max_length=255, blank=True)
    related_aat_term_notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Language(models.Model):
    name = models.CharField(max_length=255)
    iso639_1 = models.CharField(max_length=2)
    iso639_2b = models.CharField(max_length=3)
    iso639_2t = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]



class Item(models.Model):
    # basic item descriptive metadata
    identifier = models.CharField(max_length=255, unique=True) 
    type = models.ForeignKey(TypeOfResource) 
    genres = models.ManyToManyField(Genre, blank=True) 
    batches = models.ManyToManyField(Batch, blank=True) 
    title = models.CharField(max_length=255) 
    creators = models.ManyToManyField(Name, blank=True, related_name='creator_name') 
    contributors = models.ManyToManyField(Name, blank=True, related_name='contributor_name') 
    description = models.TextField(blank=True)
    date = models.CharField(max_length=255, blank=True) 
    date_qualifier = models.BooleanField(verbose_name="date qualified?") 
    format = models.ForeignKey(Format, blank=True, null=True)
    extent = models.CharField(max_length=255, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True) 
    copyright_status = models.CharField(max_length=255, choices=COPYRIGHT_STATUS_VALUES, default='unknown') 
    publication_status = models.CharField(max_length=255, choices=PUBLICATION_STATUS_VALUES, default='unknown') 
    copyright_holder = models.CharField(max_length=255, blank=True) 
    copyright_notes = models.CharField(max_length=255, blank=True) 
    restriction_status = models.CharField(max_length=255, blank=True) 
    restriction_notes = models.CharField(max_length=255, blank=True) 
    release_forms = models.CharField(max_length=255, blank=True) 
    publisher = models.CharField(max_length=255, blank=True) 
    language = models.ForeignKey(Language, blank=True, null=True) 
    source_collection = models.ForeignKey(Collection, blank=True, null=True) 
    digital_collection = models.ForeignKey(Digital_Collection, blank=True, null=True) 
    source_id = models.CharField(max_length=255, blank=True, verbose_name="legacy id for source object") 
    subject_location = models.ForeignKey(SubjectLocation, blank=True, null=True, verbose_name="location")
    #geotag = models.ForeignKey(GeoTag, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True) 
    notes = models.TextField(blank=True) 
    record_created = models.DateTimeField(max_length=255, auto_now_add=True) 
    last_modified = models.DateTimeField(max_length=255, auto_now=True) 
    scanning_status = models.CharField(max_length=255, blank=True) 
    processing_status = models.CharField(max_length=255, blank=True) 
    completed_by = models.CharField(max_length=255, blank=True) 
    date_digitized = models.DateTimeField(max_length=255, blank=True, null=True) 
    digital_notes = models.CharField(max_length=255, blank=True) 

    def __unicode__(self):
        return u'%s / %s' % (self.identifier, self.title)
  
    def thumbnail(self):
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
                return '<img src="%s%s%s"/>' % (settings.MEDIA_URL, 'thumbs/', thumb_filename,)
        except:
            return None 
    thumbnail.short_description = "Image Thumbnail"
    thumbnail.allow_tags = True

    def get_path(self):
        try:
            filepath =  File.objects.filter(item_file__item=self)[0].path
            return filepath
        except:
            return None 

    class Meta:
        ordering = ["identifier"]
    
    class Facet:    
        fields = ['source_collection', 'digital_collection', ]

class GeoTag(models.Model):
    item = models.ForeignKey(Item)
    lat = models.FloatField()
    long = models.FloatField()
    heading = models.FloatField(null=True, blank=True)
    pitch = models.FloatField(null=True, blank=True)
    zoom = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return '%s, %s' % (self.lat, self.long)

    class Meta:
        ordering = ["lat"]

class Media_Object(models.Model):
    item = models.ForeignKey(Item)
    identifier = models.CharField(max_length=255, unique=True) 
    title = models.CharField(max_length=255) 
    creator = models.ForeignKey(Name, blank=True, null=True) 
    description = models.TextField(blank=True)
    normalized_date = models.CharField(max_length=255, blank=True) 
    display_date = models.CharField(max_length=255, blank=True) 
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
    path = models.CharField(max_length=255, blank=True)
    size_bytes = models.IntegerField(blank=True, null=True, editable=False)
    mime_type = models.CharField(max_length=255, choices=MIME_TYPE_CHOICES, blank=True)
    use = models.CharField(max_length=255, choices=FILE_USE_CHOICES, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Media_Object_File(File):
    media_object = models.ForeignKey(Media_Object)

class Image_Item_File(File):
    image_item = models.ForeignKey(Item)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item 
   
class NameForm(forms.ModelForm):
    class Meta:
        model = Name 
   
class FormatForm(forms.ModelForm):
    class Meta:
        model = Format 
   
class SubjectLocationForm(forms.ModelForm):
    class Meta:
        model = SubjectLocation 
   
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


