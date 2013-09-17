from django.conf.urls import patterns, include, url
from assess.views import hello, current_datetime

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
      url(r'^hello/$', hello),
      url(r'^time/$', current_datetime),
      (r'^admin/', include(admin.site.urls)),
)
