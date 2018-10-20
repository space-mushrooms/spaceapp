from django.conf.urls import url, include

from app.views.default import DefaultView

urlpatterns = [
    url(r'^$', DefaultView.as_view(), name='default'),
]
