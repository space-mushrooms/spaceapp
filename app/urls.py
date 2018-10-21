from django.conf.urls import url, include

from app.views.default import DefaultView, LaunchView

urlpatterns = [
    url(r'^$', DefaultView.as_view(), name='default'),
    url(r'^launch$', LaunchView.as_view(), name='launch'),
]
