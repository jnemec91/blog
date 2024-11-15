from django.shortcuts import render
from blog.models import BlogUser, BlogPost, Category

def index(request):
    return render(request, 'blog/index.html', {'categories': Category.objects.all()})

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

def posts(request):
    return render(request, 'blog/posts.html', {'posts': BlogPost.objects.all().order_by('-created_at')})

def category(request, category_hash):
    category = Category.objects.get(hash_field=category_hash)
    
    category_posts = BlogPost.objects.filter(category=category).order_by('-created_at')

    return render(request, 'blog/posts.html', {'category': category, 'posts': category_posts})

def post(request, post_hash):
    post = BlogPost.objects.get(hash_field=post_hash)

    return render(request, 'blog/post_detail.html', {'post': post})