from django.contrib import admin
from .models import User,History,Category,BlogPost,Like,Comment,Community,UserCommunity
# Register your models here.
# admin.site.register(User)
admin.site.register(History)

admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Community)
admin.site.register(UserCommunity)