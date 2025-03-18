from django.urls import path, include
from .views import * 

app_name = 'main'

urlpatterns = [
    path('', Cake_page.as_view(), name='cake_page'), # cake customer page
    
] 
