from django.urls import path
from .views import * 

appname = 'chat'

urlpatterns = [
    path('lobby', Index.as_view(), name='main'), # chat room lobby
    path('<str:chatroom>/', Room.as_view(), name='room') # chatroom
]
