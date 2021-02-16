from django import template
from ..models import TwitterUser, Follow

register = template.Library()

@register.simple_tag
def user_following_stat(user_id):
    user = TwitterUser.objects.get(id=user_id)
    count = Follow.objects.filter(follower=user).count()
    return count

@register.simple_tag
def user_followers_stat(user_id):
    user = TwitterUser.objects.get(id=user_id)
    count = Follow.objects.filter(followed=user).count()
    return count

