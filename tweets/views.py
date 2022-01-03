from django import views
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from accounts.models import TwitterUser, Follow
from tweets.forms import CreateTweetForm
from .models import Like, Tweet


def GetTimeline(request):
    TWEETS_PER_PAGE = 10
    page_number = request.GET['page'] if 'page' in request.GET else 1
    offset = (page_number - 1) * TWEETS_PER_PAGE
    limit = page_number * TWEETS_PER_PAGE
    following_users = TwitterUser.objects.filter(Q(followers__in=Follow.objects.filter(follower=request.user)) | Q(id=request.user.id))
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
    create_tweet_form = CreateTweetForm()
    template_name = 'tweets/timeline.html'
    context = {
        'tweets': tweets,
        'create_tweet_form': create_tweet_form,
    }
    return render(request, template_name, context)

class CreateTweet(views.View):
    def post(self, request):
        tweet_form = CreateTweetForm(data=request.POST)
        if tweet_form.is_valid():
            try:
                user = TwitterUser.objects.get(id=request.user.id)
                Tweet.objects.create(
                    user=user,
                    body=tweet_form.cleaned_data['body']
                )
                return redirect('/app/')
            except Exception as e:
                print(e)
                messages.error(request, 'No se pudo crear el tweet')
                return redirect('/app/')
        else:
            messages.error(request, 'Bad request')
            return redirect('/app/')

class ToggleLikeTweet(views.View):
    def post(self, request):
        try:
            tweet = Tweet.objects.get(id=request.POST['tweet_id'])

            liked_tweet = Like.objects.filter(user=request.user, liked_tweet=tweet)

            if len(liked_tweet) == 0:
                Like.objects.create(
                    user = request.user,
                    liked_tweet = tweet
                )
            else:
                liked_tweet.delete()
            return redirect('/app/')
        except Exception as e:
            print(e)
            messages.error(request, 'No se puede dar like al tweet')
            return redirect('/app/')

# class RetweetTweet(views.View):
#     def post(self, request):
#         try:
#             tweet = Tweet.objects.get(id=request.POST['tweet_id'])
#             print(request.POST['quote'] == None)
#         except Exception as e:
#             print(e)
#             messages.error(request, 'No se pudo realizar el retweet')
#             return redirect('/app/')