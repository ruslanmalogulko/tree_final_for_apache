from django.conf.urls import patterns, include, url
from views import show_child, post, send_zip, send_file, upload_file, xml_data, login, tree

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', login),
	(r'login/$', login),
	(r'tree/$', tree),
	(r'xml/$', xml_data),
    (r'upload/$', upload_file),
    (r'send/$', send_file),
    (r'sendzip/$', send_zip),
    (r'post/$', post),
    # (r'xml-test/$', xml_test),
    (r'tree/childs/$', show_child),

    # Examples:
    # url(r'^$', 'tree.views.home', name='home'),
    # url(r'^tree/', include('tree.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
