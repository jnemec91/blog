from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import BlogUserManager

# this app will need following models with folowng parameters
# User - this will be the user who will be writing the blog. Needs to have username, password, email, first_name, last_name. 
# Its a good idea to create a custom user model, just because i want to learn how to do it.

# Blog_post - this will be the blog model. Needs to have title, content, autho(fk user), created_at, updated_at. Also needs an image field to store title image of the blog.
# Also needs to have a category field(fk category) to categorize the blog.

# Category - this will be the category model. Needs to have name, description, created_at, updated_at.

# HistoryLog - this will be the history log model. Needs to have user(fk user), blog_post(fk blog_post), action, created_at. 

class BlogUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BlogUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="User created")
        else:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="User updated")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="User deleted")
        super().delete(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    description = models.TextField(_("description"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Category created")
        else:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Category updated")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Category deleted")
        super().delete(*args, **kwargs)
    

class BlogPost(models.Model):
    title = models.CharField(_("title"), max_length=100)
    content = models.TextField(_("content"))
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    image = models.ImageField(_("image"), upload_to="blog_images", blank=True) # title image for the blog page
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Blog created")
        else:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Blog updated")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Blog deleted")
        super().delete(*args, **kwargs)
    

class HistoryLog(models.Model):
    source = models.CharField(_("source"), max_length=320)
    action = models.CharField(_("action"), max_length=20)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.action}"