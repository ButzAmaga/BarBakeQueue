from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from cake.models import *
from django.db.models import Avg, Sum, Q
from django.db.models.functions import Ceil
from cake.filters import Cake_filter
# Create your views here.

class Cake_page(ListView):
    template_name = 'main/cake_page.html'
    model = Cake
    context_object_name = 'cakes'
    filterset = Cake_filter

    def get_queryset(self):
        cakes = self.model.objects.annotate(avg_rating = Ceil(Avg("ratings__rate")), sold=Sum("cart__quantity", filter=Q(cart__is_ordered=True))).order_by("group_by", "-price")
        self.filterset = self.filterset(self.request.GET, queryset=cakes)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context

class Index_page(TemplateView):
    template_name = "main/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["occasions"] = Cake.OCCASION_CHOICES
        
        return context        
    
from django.utils.timezone import now
from django.db.models.functions import TruncMonth


class Index_whats_new(ListView):
    model = Cake
    template_name = "main/index/cake_listing.html"
    context_object_name = "cakes"
    paginate_by = 3

    def get_queryset(self):
        today = now()
        queryset = Cake.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month
        ).annotate(avg_rating = Ceil(Avg("ratings__rate")), sold=Sum("cart__quantity", filter=Q(cart__is_ordered=True))).order_by("group_by", "-price")
        return queryset
    

    
      
