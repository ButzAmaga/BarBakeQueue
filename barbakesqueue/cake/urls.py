from django.urls import path, include
from .views import * 

app_name = 'cake'

urlpatterns = [
    path('list/', CakeList.as_view(), name='cakes'), 
    path('create/', CakeCreate.as_view(), name='create'),
    path('edit/<pk>', CakeEdit.as_view(), name='edit'), 
    path('delete/<pk>', CakeDelete.as_view(), name='delete'),
] 
