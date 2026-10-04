from django.urls import path

from . import views

app_name = 'products_api'

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('coupons/validate/', views.CouponValidateAPIView.as_view(), name='coupon-validate'),
    path('<slug:slug>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('', views.ProductListAPIView.as_view(), name='product-list'),
]
