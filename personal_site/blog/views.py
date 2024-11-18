from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.forms.LoginForm import LoginForm


def index(request):
    return render(request, 'blog/index.html', {'categories': Category.objects.all()})

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

def latest(request):
    latest_post = BlogPost.objects.latest('created_at')
    return post(request, latest_post.hash_field)

def posts(request, search_phrase=None, category=None):
    if category:
        content = BlogPost.objects.filter(category=category).order_by('-created_at')
        category_name = category
        pagination_url = reverse('blog:category', args=[category.hash_field])
        
    else:
        content = BlogPost.objects.all().order_by('-created_at')
        pagination_url = reverse('blog:posts')
    
    if search_phrase:
        content = content.filter(title__icontains=search_phrase) | content.filter(category__name__icontains=search_phrase)
        category = {'name':'Search','description': f'results for: {search_phrase}'}
        pagination_url = pagination_url + f'{search_phrase}'

    paginator = Paginator(content, 4)
    page_number = request.GET.get('page', 1)
    content = paginator.page(page_number)
    
    return render(request, 'blog/posts.html', {'posts': content, 'category': category, 'pagination_url': pagination_url,})

def category(request, category_hash):
    category = Category.objects.get(hash_field=category_hash)
    return posts(request, category=category)

def post(request, post_hash):
    post = BlogPost.objects.get(hash_field=post_hash)
    return render(request, 'blog/post_detail.html', {'post': post})

def update_navbar(request):
    return render(request, 'blog/components/navbar.html', {'categories': Category.objects.all()})

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid(request):
        user = form.login(request)
        if user:
            HistoryLog.objects.create(source=user, action='login')
            return redirect('blog:home')
        
    return render(request, 'blog/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    HistoryLog.objects.create(source=request.user, action='logout')
    
        
    return redirect('blog:home')