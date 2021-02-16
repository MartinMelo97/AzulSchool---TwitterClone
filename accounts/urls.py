from django.urls import path
from .views import UserList, FollowUser, UnfollowUser

app_name = 'accounts'
urlpatterns = [
    path('', UserList, name='list'),
    path('follow/', FollowUser, name='follow'),
    path('unfollow/', UnfollowUser, name='unfollow')
]