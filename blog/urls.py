from django.urls import path
from . import views

urlpatterns= [
 path('', views.index, name='index'),
 path('view-blog/<int:blog_id>/<slug:blog_slug>', views.blog_ditaes, name='blog_ditaes'),
 path('blog/', views.user_blog_show, name='user_blog_show'),
 path('add-blog', views.add_blog, name='add_blog'),
 path('edit-blog/<int:blog_id>/<slug:blog_slug>', views.edit_blog, name='edit_blog'),
 path('remove-blog/<int:blog_id>', views.remove_blog, name='remove_blog'),

]