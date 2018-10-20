from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from utils.auth import google

auth = [
    url(r'^login/', google.RedirectToGoogle.as_view(), name='login'),
    url(r'^logout/', google.Logout.as_view(), name='logout'),
    url(r'^error/', google.AccessDenied.as_view(), name='access_denied'),
    url(r'^$', google.Login.as_view(), name='login_menu'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include((auth, 'utils'), namespace='auth')),

    url(r'^api/', include('api.urls')),

    url(r'^django_rq/', include('django_rq.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

admin.autodiscover()
