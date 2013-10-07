from django.conf.urls import patterns, include, url
from assess import views
# from assess.views import hello, current_datetime, hours_ahead, student_registration

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^student/login/$', views.student_login),
    url(r'^student/get_data/(?P<table>\w{0,30})/$', views.get_data),
    url(r'^assessment/record/(?P<assessmevent_id>\w{0,15})/$', views.record_assessment),
    # url(r'^sets/finish/$', views.record_assessment),
    url(r'^student/status/$', views.student_status),
    url(r'^student/register/$', views.student_register),
    (r'^admin/', include(admin.site.urls)),
		url(r'^.*', views.student_login),
)
