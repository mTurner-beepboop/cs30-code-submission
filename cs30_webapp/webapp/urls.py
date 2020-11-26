from django.urls import path
from webapp import views
app_name = 'webapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('dbview/', views.dbview, name='dbview'),
]
