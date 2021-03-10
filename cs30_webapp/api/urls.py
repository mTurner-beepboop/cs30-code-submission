from django.conf.urls import url
from api import views
app_name= 'api'

urlpatterns = [
    url(r'^api/carbon$', views.entry_list),
    url(r'^api/carbon/(?P<pk>[0-9]+)$', views.entry_detail),
    url(r'^api/carbon/scope$', views.categories),
    url(r'^api/carbon/info$', views.item_calc),
    url(r'^api/home$', views.home, name='home'),
]