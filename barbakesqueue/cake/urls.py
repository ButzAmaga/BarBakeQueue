from django.urls import path, include
from .views import * 

app_name = 'cake'

urlpatterns = [
    path('list/', CakeList.as_view(), name='cakes'), # list of cakes
    path('edit/<pk>', CakeEdit.as_view(), name='edit'), # edit cake
] 
