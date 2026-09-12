from . import views
from django.urls import path

urlpatterns = [

    path('handle-request', views.handle_request, name='handle_request'),
    path('handle-request/', views.handle_request, name='handle_request'),
    path('razorpay-payment-request/<slug:order_id>', views.send_request_to_razorpay_for_get_amount, name='send_request_to_razorpay_for_get_amount'),
]
