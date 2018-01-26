from django.conf.urls import include, url
from django.contrib import admin

from utils.views import HealthCheck
from v1.urls import urlpatterns as v1_urls

admin.autodiscover()
admin.site.site_header = 'Luiza Employee Manager'

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'healthcheck/', HealthCheck.as_view()),

    url(r'v1/', include(v1_urls)),
]
