from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


# Create your models here.

class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=True)
    agent = models.ForeignKey("Agent", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name='leads', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CharField)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=25)  # New, Contacted, Converted, Unconverted
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=True)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
