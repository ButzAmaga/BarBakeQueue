from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from cake.models import *
from django.db.models import Avg, Sum, Q
from django.db.models.functions import Ceil
# Create your views here.

class Cake_page(ListView):
    template_name = 'main/cake_page.html'
    model = Cake
    context_object_name = 'cakes'

    def get_queryset(self):
        return self.model.objects.annotate(avg_rating = Ceil(Avg("ratings__rate")), sold=Sum("cart__quantity", filter=Q(cart__is_ordered=True)))