from django.urls import path, include
from .views import * 

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'), # chat room lobby
    
] 
