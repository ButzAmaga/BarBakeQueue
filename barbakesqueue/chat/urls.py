from django.urls import path, include
from .views import * 
app_name = 'chat'

urlpatterns = [
    path('lobby', Index.as_view(), name='main'), # chat room lobby
    path('<str:chatroom>/', Room.as_view(), name='room'), # chatroom
    
    path('', Index.as_view(template_name="chat/practice.html"), name='htmx'), # chat room lobby
    path('test1', Index.as_view(template_name="chat/test/test1.html"), name='test1'), # chat room lobby
    path('person_form_submit', PersonFormView.as_view(), name='personSubmit'), # chat room lobby

    path('stream/', include('chat.sse_routing'))
] 
