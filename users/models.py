from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, blank=True, verbose_name='URL')

    def __str__(self):
        return f'Email:{self.email}'


class Contact(models.Model):
    email = models.EmailField(max_length=128, unique=True)