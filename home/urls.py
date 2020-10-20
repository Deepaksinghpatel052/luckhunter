from django.urls import path
from . import views

urlpatterns= [
 path('', views.under_construction, name='under_construction'),
 # path('home', views.index, name='index'),
 # path('set_cookes/<slug:rerfrral_code>', views.set_cookes, name='set_cookes'),
 # path('winners', views.winners, name='winners'),
 # path('page/<slug:keyword>', views.page_content, name='page_content'),
 # path('get_categoryes', views.get_categoryes, name='get_categoryes'),
 # path('products', views.all_products, name='all_products'),
 # path('products/', views.all_products, name='all_products'),
 # path('running-bid', views.running_bid, name='running_bid'),
 # path('running-bid/', views.running_bid, name='running_bid'),
 #
 # path('this-month-bid', views.this_month_bid, name='this_month_bid'),
 # path('this-month-bid/', views.this_month_bid, name='this_month_bid'),
 #
 # path('upcoming-products', views.upcoming_product, name='upcoming_product'),
 # path('upcoming-products/', views.upcoming_product, name='upcoming_product'),
 #
 # path('products/<slug:slug>/', views.all_products, name='all_products'),
 # path('product/<slug:slug>/<slug:product_id>', views.product, name='product'),





]