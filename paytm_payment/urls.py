from . import views
from django.urls import path

urlpatterns = [

    path('', views.index, name='index'),
    path('hendel-request', views.hendel_request, name='hendel_request'),
    path('hendel-request/', views.hendel_request, name='hendel_request'),
    path('paytm-payment-request/<slug:order_id>', views.send_request_to_paytm_for_get_amount, name='send_request_to_paytm_for_get_amount'),
]