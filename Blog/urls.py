# myapp/urls.py
from django.urls import path
from .views import register, user_login,home,logout_request,create_blog_post,myallblogs,update_blog,delete_blog,like_blog,remove_like,add_comment,get_comments,delete_comment,user_profile,create_community,join_community,user_community,leave_community,show_content,delete_community

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path("logout/", logout_request, name="logout"),
    path('create/', create_blog_post, name='create_blog_post'),
    path('myallblogs/', myallblogs, name='myallblogs'),
    path('update_blog/<int:pk>/', update_blog, name='update_blog'),
    path('delete_blog/<int:pk>/', delete_blog, name='delete_blog'),
    path('like_blog/<int:pk>/', like_blog, name='like_blog'),
    path('remove_like/<int:pk>/', remove_like, name='remove_like'),
    path('add_comment/<int:pk>/', add_comment, name='add_comment'),
    path('get_comments/', get_comments, name='get_comments'),
    path('delete_comment/<int:blog_id>/<int:comment_id>/', delete_comment, name='delete_comment'),   
    path('user_profile/', user_profile, name='user_profile'),
    path('create_community/', create_community, name='create_community'),
    path('join_community/', join_community, name='join_community'),
    path('user_community/<int:pk>', user_community, name='user_community'),
    path('leave_community/<int:pk>', leave_community, name='leave_community'),
    path('show_content/<int:pk>', show_content, name='show_content'),
    path('delete_community/<int:pk>', delete_community, name='delete_community'),


]