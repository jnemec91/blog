from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.forms.LoginForm import LoginForm
from blog.forms.BlogPostForm import BlogPostForm
from blog.forms.CategoryForm import CategoryForm


def index(request):
    return render(request, 'blog/index.html', {'categories': Category.objects.filter(blogpost__is_published=True).distinct()})

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

def posts(request, search_phrase=None, category=None):
    if category:
        content = BlogPost.objects.filter(category=category).filter(is_published=True).order_by('-created_at')
        category_name = category
        pagination_url = reverse('blog:category', args=[category.hash_field])
        
    else:
        content = BlogPost.objects.filter(is_published=True).order_by('-created_at')
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
    categories = Category.objects.filter(blogpost__is_published=True).distinct()
    latest_post = BlogPost.objects.filter(is_published=True)
    if latest_post:
        latest_post = latest_post.latest('created_at').hash_field
    else:
        latest_post = None
    return render(request, 'blog/components/navbar.html', {'categories': categories, 'latest':latest_post})

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid(request):
        user = form.login(request)
        if user:
            HistoryLog.objects.create(source=user, action='login')
            return redirect('blog:home')
        
    return render(request, 'blog/login.html', {'form': form})

def logout(request):
    HistoryLog.objects.create(source=request.user, action='logout')
    auth_logout(request)
    
    return redirect('blog:home')

def posts_admin(request):
    return render(request, 'blog/posts_admin.html')

def get_posts_table_part(request, last_id=None):
    # get first 20 posts if last_id is None, else get the next 20 posts after last_id
    if last_id:
        posts = BlogPost.objects.filter(id__lt=last_id).order_by('-id')[:20]
    else:
        posts = BlogPost.objects.all().order_by('-id')[:20]

    return render(request, 'blog/components/post_table.html', {'posts': posts})


def post_edit(request, post_hash=None):
    post = None
    if post_hash:
        post = get_object_or_404(BlogPost, hash_field=post_hash)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post, user=request.user)
        if form.is_valid():
            post = form.save()
            return redirect('blog:posts_admin')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

def post_delete(request, post_hash):
    if request.method == "DELETE":
        post = get_object_or_404(BlogPost, hash_field=post_hash)
        post.delete()
    return redirect('blog:posts_admin')

def categories_admin(request):
    return render(request, 'blog/categories_admin.html')

def get_categories_table_part(request, last_id=None):
    # get first 20 categories if last_id is None, else get the next 20 posts after last_id
    if last_id:
        categories = Category.objects.filter(id__lt=last_id).order_by('-id')[:20]
    else:
        categories = Category.objects.all().order_by('-id')[:20]

    return render(request, 'blog/components/category_table.html', {'categories': categories})


def category_edit(request, category_hash=None):
    category = None
    if category_hash:
        category = get_object_or_404(Category, hash_field=category_hash)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('blog:categories_admin')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'blog/category_edit.html', {'form':form, 'category':category})

def category_delete(request, category_hash):
    if request.method == "DELETE":
        category = get_object_or_404(Category, hash_field=category_hash)
        category.delete()
        return redirect('blog:categories_admin')