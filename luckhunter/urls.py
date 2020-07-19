"""luckhunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from home import views

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('superadmin/', admin.site.urls),

    path('', include('home.urls')),
    path('account', include('accounts.urls')),
    path('account/', include('accounts.urls')),
    
    path('accounts/', include('accounts.urls')),

    path('accounts/', include('allauth.urls')),
    path('do-login-first', views.login_page,name="login_page"),
    path('do-login-first/', views.login_page,name="login_page"),

    path('user/product-notification', include('wishlist.urls')),
    path('user/product-notification/', include('wishlist.urls')),

    path('user/my-profile', include('user_profile.urls')),
    path('user/my-profile/', include('user_profile.urls')),

    path('summernote/', include('django_summernote.urls')),

    path('user/orders', include('orders.urls')),
    path('user/orders/', include('orders.urls')),

    path('paytm-payment/', include('paytm_payment.urls')),
    path('stripe-payment/', include('stripe_payment.urls')),

    path('user/address', include('user_address.urls')),
    path('user/address/', include('user_address.urls')),





    path('blog', include('blog.urls')),
    path('blog/<slug:product_slug>', include('blog.urls')),
    path('blog/', include('blog.urls')),
    path('user/', include('blog.urls')),

    path('user/wallet', include('wallet.urls')),
    path('user/wallet/', include('wallet.urls')),

    path('user/complanes', include('queryes.urls')),
    path('user/complanes/', include('queryes.urls')),

    path('get-adds/', include('manage_adds.urls')),
    path('get-adds', include('manage_adds.urls')),

    path('send-email', include('send_email.urls')),
    path('send-email/', include('send_email.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
