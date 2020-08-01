from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-referral-code', views.add_referral_code, name='add_referral_code'),
    # path('create-wallet', views.create_wallet, name='create_wallet'),
    # path('check-wallet-id', views.check_wallet_id, name='check_wallet_id'),
    # path('check-wallet-code', views.check_wallet_code, name='check_wallet_code'),
    # path('check-amount', views.check_amount, name='check_amount'),
    # path('order-by-wallet', views.order_by_wallet, name='order_by_wallet'),
    # path('fake-payment', views.fake_payment, name='fake_payment'),
]