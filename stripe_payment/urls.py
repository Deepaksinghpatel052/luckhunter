from . import views
from django.urls import path

urlpatterns = [
    path('do-payments', views.do_payments, name='do_payments'),
    path('update-order-status', views.update_order_update_order, name='update_order_update_order'),
]