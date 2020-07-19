from django.urls import path
from . import views


urlpatterns= [

 path('register', views.register, name='register'),
 path('register/', views.register, name='register'),

 path('login-user', views.login_user, name='login_user'),
 path('login-user/', views.login_user, name='login_user'),

 path('system-info', views.system_info, name='system_info'),
 path('test', views.test, name='test'),

 path('profile/', views.set_session_for_socila_login, name='set_session_for_socila_login'),

 path('logout', views.logout, name='logout'),
 path('logout/', views.logout, name='logout'),

]