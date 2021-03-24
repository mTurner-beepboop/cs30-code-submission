from django.urls import path
from webapp import views
app_name = 'webapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('dbview/', views.dbview, name='dbview'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<refnum>', views.edit, name='edit'),
    path('delete/<refnum>', views.delete, name='delete'),
    path('add/', views.add, name='add'),
    path('viewdb/', views.search, name='search'),
]
