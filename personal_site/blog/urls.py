from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # views
    path('', views.about_redirect, name='about_redirect'),
    path('about/', views.about, name='about'),
    path('samba/', views.samba, name='samba'),    
    path('home/', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('posts/<str:search_phrase>/', views.posts, name='posts'),
    path('category/<str:category_hash>/', views.category, name='category'),
    path('post/<str:post_hash>/', views.post, name='post'),
    
    # admin views
    path('posts_admin/', views.posts_admin, name='posts_admin'),
    path('post_edit/', views.post_edit, name='post_edit'),
    path('post_edit/<str:post_hash>/', views.post_edit, name='post_edit'),
    path('post_delete/<str:post_hash>/', views.post_delete, name='post_delete'),
    path('categories_admin/', views.categories_admin, name='categories_admin'),
    path('category_edit/', views.category_edit, name='category_edit'),
    path('categories_edit/<str:category_hash>/', views.category_edit, name='category_edit'),
    path('category_delete/<str:category_hash>/', views.category_delete, name='category_delete'),
    path('history_log/', views.history_log, name='history_log'),
    path('stats/', views.stats, name='stats'),


    # ajax views
    path('update_navbar/', views.update_navbar, name='update_navbar'),
    path('get_posts_table/', views.get_posts_table_part, name='get_posts_table_part'),
    path('get_posts_table/<int:last_id>', views.get_posts_table_part, name='get_posts_table_part'),
    path('get_categories_table/', views.get_categories_table_part, name='get_categories_table_part'),
    path('get_categories_table/<int:last_id>', views.get_categories_table_part, name='get_categories_table_part'),
    path('get_history_log_table_part/', views.get_history_log_table_part, name='get_history_log_table_part'),
    path('get_history_log_table_part/<int:last_id>/', views.get_history_log_table_part, name='get_history_log_table_part'),
    path('like_post/<str:post_hash>/<str:like_type>/', views.like_post, name='like_post'),
    path('post_footer/<str:post_hash>/', views.post_footer, name='post_footer'),

    # auth views
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]