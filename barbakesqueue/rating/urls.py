from django.urls import path, include
from .views import * 

app_name = 'rating'

urlpatterns = [
    path('rate_cake/<int:cake_id>', RatingForm.as_view(), name='customer_rate'), # form for rating the cake
    path('cake_reviews/<int:cake_id>', CakeReviews.as_view(), name='cake_reviews'), # list out cake reviews
] 
