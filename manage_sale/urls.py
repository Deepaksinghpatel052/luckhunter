from django.urls import path
from . import views

urlpatterns= [
    path('', views.show_salse, name='show_salse'),
    path('set-winners-for-sale', views.SetWinnersForSale, name='SetWinnersForSale'),
    path('add-coins-for-product-sale', views.AddCoinsForProductSale, name='AddCoinsForProductSale'),
    path('get-product-coin-info/<slug:product_id>/<slug:sale_id>', views.get_product_coin_info, name='get_product_coin_info'),
]