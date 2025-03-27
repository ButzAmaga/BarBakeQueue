from django.urls import path, include
from .views import * 

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'), # chat room lobby
    path('login/promp', Login_first_promp.as_view(), name='login_promp'), # chat room lobby
    
] 
