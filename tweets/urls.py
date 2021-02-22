from django.urls import path, include
from .views import GetTimeline

app_name='app'
urlpatterns = [
    path('home/', GetTimeline, name='home')
]
