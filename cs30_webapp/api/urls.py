from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/carbon$', views.entry_list),
    url(r'^api/carbon/(?P<pk>[0-9]+)$', views.entry_detail),
]