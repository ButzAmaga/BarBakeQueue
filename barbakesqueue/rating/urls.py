from django.urls import path, include
from .views import * 

app_name = 'rating'

urlpatterns = [
    path('rate_cake/<int:cake_id>', RatingDispatchView.as_view(), name='customer_rate'), # form for rating the cake
] 
