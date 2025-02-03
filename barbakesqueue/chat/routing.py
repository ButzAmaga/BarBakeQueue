from django.urls import re_path
from .consumers import *
urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", Async_ChatConsumer.as_asgi())
]