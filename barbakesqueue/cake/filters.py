import django_filters 
from .models import *
from django import forms

PRICE_CHOICES = [
    (100, '> 100'),
    (500, '> 500'),
    (1000, '> 1000'),
    (3000, '> 3000'),
    (5000, '> 5001'),
]

RATING_CHOICES = [
    (1, '1 star'),
    (2, '2 Star'),
    (3, '3 Star'),
    (4, '4 Star'),
    (5, '5 Star'),
]

class Cake_filter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains') 
    price__lt = django_filters.ChoiceFilter(field_name='price',  lookup_expr='lt', choices = PRICE_CHOICES  )
    rating = django_filters.ChoiceFilter(field_name="avg_rating", choices = RATING_CHOICES)
    
    group_by = django_filters.ChoiceFilter(
        field_name='group_by',
        choices=Cake.OCCASION_CHOICES,
        label='Occasion'
    )