from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Example:
    # (r'^alvin/', include('alvin.foo.urls')),
    (r'^$', 'alvin.core.views.main'),
    (r'^logout/$', 'alvin.core.views.logout_passthrough'),
    (r'^login/$', 'alvin.core.views.handle_login'),
    (r'^item/$', 'alvin.core.views.get_items'),
    (r'^item/new/$', 'alvin.core.views.item_new'),
    (r'^item/(?P<item_id>.+)/$', 'alvin.core.views.item_detail'),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
