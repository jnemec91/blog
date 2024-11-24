from django.contrib import admin
from blog.models import BlogUser, BlogPost, Category, HistoryLog, Stats

# Register your models here.
admin.site.register(BlogUser)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(HistoryLog)
admin.site.register(Stats)
