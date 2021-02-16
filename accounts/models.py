from django.db import models
from django.contrib.auth.models import AbstractUser

class TwitterUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='users/profile', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover', blank=True, null=True)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(TwitterUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(TwitterUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
