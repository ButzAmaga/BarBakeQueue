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

MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
]


class TransactionFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(label="Customer Name",field_name='full_name', lookup_expr='icontains')
    month = django_filters.ChoiceFilter(
        field_name='date_submitted__month',
        choices=MONTH_CHOICES,
        label='Month'
    )
    payment_type = django_filters.ChoiceFilter(
        field_name='payment_type',
        choices= Type_choices,
        label='Payment Type'
    )
    class Meta:
        model = Transaction
        fields = ["customer_name", "month", "payment_type"]