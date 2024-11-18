from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('posts/<str:search_phrase>/', views.posts, name='posts'),
    path('category/<str:category_hash>/', views.category, name='category'),
    path('post/<str:post_hash>/', views.post, name='post'),
    path('update_navbar/', views.update_navbar, name='update_navbar'),
]