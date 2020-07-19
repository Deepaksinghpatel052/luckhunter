from django.urls import path
from . import views


urlpatterns= [
 path('', views.index, name='index'),
 path('update-image', views.update_image, name='update_image'),
 path('update_password', views.update_password, name='update_password'),
]