from django.urls import path
from . import views
from django.contrib.auth import views as auth_login

urlpatterns= [

 path('register', views.register, name='register'),
 path('register/', views.register, name='register'),

 path('login-user', views.login_user, name='login_user'),
 path('login-user/', views.login_user, name='login_user'),

 path('check_condition_status', views.check_condition_status, name='check_condition_status'),
 path('check_condition_status/', views.check_condition_status, name='check_condition_status'),
 path('check_and_update_user_emai/', views.check_and_update_user_emai, name='check_and_update_user_emai'),

 path('update_condition_status', views.update_condition_status, name='update_condition_status'),
 path('update_condition_status/', views.update_condition_status, name='update_condition_status'),

 path('system-info', views.system_info, name='system_info'),
 path('test', views.test, name='test'),

 path('profile/', views.set_session_for_socila_login, name='set_session_for_socila_login'),

 path('logout', views.logout, name='logout'),
 path('logout/', views.logout, name='logout'),

 


]