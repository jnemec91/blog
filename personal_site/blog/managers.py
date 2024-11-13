from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class BlogUserManager(BaseUserManager):
    """
    Custom user manager for the BlogUser model, email is the unique identifier
    for authentication and no username field is required.

    Inherits from BaseUserManager.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        :param email: email of the user
        :param password: password of the user
        :param extra_fields: additional fields to be added to the user model
        :return: user object
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.

        :param email: email of the user
        :param password: password of the user
        :param extra_fields: additional fields to be added to the user model
        :return: user object
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
