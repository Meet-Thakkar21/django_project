# myapp/urls.py
from django.urls import path
from .views import register, user_login,home,logout_request,create_blog_post,myallblogs,update_blog,delete_blog

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path("logout/", logout_request, name="logout"),
    path('create/', create_blog_post, name='create_blog_post'),
    path('myallblogs/', myallblogs, name='myallblogs'),
    path('update_blog/<int:pk>/', update_blog, name='update_blog'),
    path('delete_blog/<int:pk>/', delete_blog, name='delete_blog'),

    # path('delete/<int:pk>/', delete_blog, name='delete_blog'),

]