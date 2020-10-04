from django.urls import path
from . import views


urlpatterns= [

  path('', views.user_order_show, name='user_order_show'),
  path('add-product', views.index, name='index'),
  path('remove-product/<int:id>', views.remove_product, name='remove_product'),
  path('get-add-to-card-product', views.get_add_to_card_product, name='get_add_to_card_product'),
  path('my-card', views.my_card, name='my_card'),
  path('remove-all-product', views.remove_all_product, name='remove_all_product'),
  path('get-coupon-code', views.get_coupon_code, name='get_coupon_code'),
  path('plased-order', views.plased_order, name='plased_order'),
  path('get_order_item', views.get_order_item, name='get_order_item'),
  path('get-order-info', views.get_order_info, name='get_order_info'),
  path('set-winner', views.set_winner, name='set_winner'),
  path('test_order', views.test_order, name='test_order'),


]