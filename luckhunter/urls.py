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
from django.contrib.auth import views as auth_login

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('superadmin/', admin.site.urls),

    path('', include(('home.urls','home'),namespace='home')),
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

    path('user/referral', include('referral_user.urls')),
    path('user/referral/', include('referral_user.urls')),





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


    path('sale/', include(('manage_sale.urls','manage_sale'),namespace='manage_sale')),
    path('sale', include(('manage_sale.urls','manage_sale'),namespace='manage_sale')),

    path('send-email', include('send_email.urls')),
    path('send-email/', include('send_email.urls')),


    path('password_reset/done/', auth_login.PasswordResetCompleteView.as_view(template_name='web/forgot_password/password_reset_done.html', extra_context={'BASE_URL': settings.BASE_URL}),name='password_reset_done'),
    path('password_reset/', auth_login.PasswordResetView.as_view(template_name='web/forgot_password/password_reset_form.html', extra_context={'BASE_URL': settings.BASE_URL}, extra_email_context={'BASE_URL': settings.BASE_URL}), name='password_reset'),

    path('reset/<uidb64>/<token>/', auth_login.PasswordResetConfirmView.as_view(template_name='web/forgot_password/password_reset_confirm.html', extra_context={'BASE_URL': settings.BASE_URL}), name='password_reset_confirm'),
    path('reset/done/', auth_login.PasswordResetCompleteView.as_view(template_name='web/forgot_password/password_reset_complete.html', extra_context={'BASE_URL': settings.BASE_URL}),
                       name='password_reset_complete'),


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
