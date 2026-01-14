from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import BlogUserManager
from .utils.hashmaker import make_hash_from_model

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
    # create field to store 32 bit hash value created from id and email, automatically create hash value when user is created
    hash_field = models.CharField(_("hash field"), max_length=32, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BlogUserManager()

    def __str__(self):
        return f'User: {self.email}'
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            HistoryLog.objects.create(source=f'NEW:{self}', action="User created")
        else:
            if kwargs.get("update_fields"):
                if not "last_login" in kwargs.get("update_fields"):
                    HistoryLog.objects.create(source=f'{self.pk}:{self}', action="User updated")
            
        super().save(*args, **kwargs)
        # fill the hash field with 32 bit hash value created from id and str representation of the object
        self.hash_field = make_hash_from_model(self)
        super().save(update_fields=["hash_field"])
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="User deleted")
        super().delete(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    description = models.TextField(_("description"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    hash_field = models.CharField(_("hash field"), max_length=32, blank=True)

    def __str__(self):
        return f'Category: {self.name}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            HistoryLog.objects.create(source=f'NEW:{self}', action="Category created")
        else:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Category updated")
        super().save(*args, **kwargs)

        self.hash_field = make_hash_from_model(self)
        super().save(update_fields=["hash_field"])
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Category deleted")
        super().delete(*args, **kwargs)
    

class BlogPost(models.Model):
    title = models.CharField(_("title"), max_length=100)
    subtitle = models.CharField(_("subtitle"), max_length=200, blank=True)
    content = models.TextField(_("content"))
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    image = models.ImageField(_("image"), upload_to="blog_images", blank=True) # title image for the blog page
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    hash_field = models.CharField(_("hash field"), max_length=32, blank=True)
    is_published = models.BooleanField(_("is published"), default=False)
    stats = models.OneToOneField("Stats", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'BlogPost: {self.title}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.stats = Stats.objects.create()
            HistoryLog.objects.create(source=f'NEW:{self}', action="Blog created")
        else:
            HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Blog updated")
        super().save(*args, **kwargs)

        self.hash_field = make_hash_from_model(self)
        super().save(update_fields=["hash_field"])
    
    def delete(self, *args, **kwargs):
        HistoryLog.objects.create(source=f'{self.pk}:{self}', action="Blog deleted")
        super().delete(*args, **kwargs)
    

class HistoryLog(models.Model):
    source = models.CharField(_("source"), max_length=320)
    action = models.CharField(_("action"), max_length=20)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"HistoryLog: {self.source} - {self.action}"
    
class Stats(models.Model):
    def default_dict():
        return {'sessions':[]}

    likes = models.IntegerField(_("likes"), default=0)
    dislikes = models.IntegerField(_("dislikes"), default=0)
    views = models.IntegerField(_("views"), default=0)
    visited = models.JSONField(_("visited sessions"), default=default_dict)
    voted = models.JSONField(_("voted sessions"), default=default_dict)
    
