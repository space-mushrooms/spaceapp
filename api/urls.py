from django.conf.urls import url, include

from api.views.default import DefaultView

urlpatterns = [
    url(r'^$', DefaultView.as_view(), name='default'),
]
