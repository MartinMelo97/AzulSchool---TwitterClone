from django.shortcuts import render
from django import views
from .models import Tweet
from accounts.models import TwitterUser, Follow
from django.db.models import Count

def GetTimeline(request):
    TWEETS_PER_PAGE = 10
    page_number = request.GET['page'] if 'page' in request.GET else 1
    offset = (page_number - 1) * TWEETS_PER_PAGE
    limit = page_number * TWEETS_PER_PAGE
    following_users = TwitterUser.objects.filter(followers__in=Follow.objects.filter(follower=request.user))
    likes_counter = Count('likes', distinct=True)
    retweets_counter = Count('retweets', distinct=True)
    responses_counter = Count('responses', distinct=True)
    tweets = Tweet.objects\
        .filter(user__in=following_users)\
        .annotate(
            likes_count=likes_counter,
            retweets_count=retweets_counter,
            responses_count=responses_counter
        )\
        .order_by('-created_at')[offset:limit]
    template_name = 'tweets/timeline.html'
    context = {
        'tweets': tweets
    }
    return render(request, template_name, context)