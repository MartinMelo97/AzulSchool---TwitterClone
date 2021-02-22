from django.db import models
from accounts.models import TwitterUser

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(TwitterUser, related_name='tweets', on_delete=models.CASCADE)
    body = models.CharField(max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body}'

class Like(models.Model):
    user = models.ForeignKey(TwitterUser, related_name='likes', on_delete=models.CASCADE)
    liked_tweet = models.ForeignKey(Tweet, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.liked_tweet.user.username} tweet'

class Retweet(models.Model):
    retweet_tweet = models.OneToOneField(Tweet, related_name='retweeted', on_delete=models.CASCADE)
    retweeted_tweet = models.ForeignKey(Tweet, related_name='retweets', on_delete=models.CASCADE)
    quote = models.CharField(max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.retweet_tweet.user.username} retweeted {self.retweeted_tweet.user.username} tweet'

class Thread(models.Model):
    response_tweet = models.OneToOneField(Tweet, related_name='responsed', on_delete=models.CASCADE)
    responsed_tweet = models.ForeignKey(Tweet, related_name='responses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.response_tweet.user.username} responses {self.responsed_tweet.user.username} tweet'