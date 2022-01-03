from django.urls import path
from .views import GetTimeline, CreateTweet, ToggleLikeTweet

app_name='app'
urlpatterns = [
    path('', GetTimeline, name='home'),
    path('create/', CreateTweet.as_view(), name='create'),
    path('like/', ToggleLikeTweet.as_view(), name='like_tweet'),
    # path('retweet/', RetweetTweet.as_view(), name='retweet_tweet')
]
