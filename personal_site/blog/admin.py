from django.contrib import admin
from blog.models import BlogUser, BlogPost, Category, HistoryLog

# Register your models here.
admin.site.register(BlogUser)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(HistoryLog)
