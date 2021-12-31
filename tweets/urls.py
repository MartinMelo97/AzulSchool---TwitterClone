from django.urls import path
from .views import GetTimeline, CreateTweet

app_name='app'
urlpatterns = [
    path('', GetTimeline, name='home'),
    path('create/', CreateTweet.as_view(), name='create')
]
