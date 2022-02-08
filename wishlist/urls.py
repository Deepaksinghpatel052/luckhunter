from django.urls import path
from . import views


urlpatterns= [

  path('', views.index, name='index'),
  path('add-remove', views.add_remove, name='add_remove'),
  path('remove-product/<int:id>', views.remove_product, name='remove_product'),
  path('remove-all', views.remove_all, name='remove_all'),

]