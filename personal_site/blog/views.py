from django.shortcuts import render
from blog.models import BlogUser, BlogPost, Category, HistoryLog

def index(request):
    return render(request, 'blog/index.html', {'categories': Category.objects.all()})

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')