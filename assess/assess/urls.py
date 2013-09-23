from django.conf.urls import patterns, include, url
from assess import views
# from assess.views import hello, current_datetime, hours_ahead, student_registration

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^student/login/$', views.student_login),
        url(r'^student/get_data/(?P<table>\w{0,30})/$', views.get_data),
        url(r'^student/status/$', views.student_status),
		url(r'^student/register/$', views.student_register),
        (r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'assess.views.home', name='home'),
    # url(r'^assess/', include('assess.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
