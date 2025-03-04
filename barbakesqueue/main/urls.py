from django.urls import path, include
from .views import * 

app_name = 'main'

urlpatterns = [
    path('', Index.as_view(), name='index'), # chat room lobby
    
] 
