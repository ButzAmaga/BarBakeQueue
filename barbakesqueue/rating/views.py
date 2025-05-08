from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, UpdateView, View, FormView
from common.views import LoginWithPermissionMixin
from common.mixin import FormResponseMixin
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from customer.models import *
# Create your views here.

class RatingForm(FormResponseMixin, LoginWithPermissionMixin, FormView):
    form_class = CustomerRatingForm
    permission_required = ["rating.add_rating"]
    form_success_message = "Thank you!"
    template_name = "rating/rating_form.html"

    def get_form(self, form_class=None):
        """ 
            the form_class is not used, this can also be modified specific in get and post request
            but this would be much better choice to avoid breaking up the full sequence of 
            post and get method
        """
        if self.request.POST:
            return self.form_class(instance = self.get_object(), **self.get_form_kwargs())

        return self.form_class(**self.get_form_kwargs())
    
    def get_form_kwargs(self):
      context = super().get_form_kwargs()    

      context["customer"] = customer.objects.get(account = self.request.user)
      context["cake"] = Cake.objects.get(id = self.kwargs["cake_id"])
       
      return context

    def get_object(self):
        """ 
            get the rating object with signiture of current user id and cake, return none if it is 
            a new rating
        """
        try:
            self.customer = customer.objects.get(account = self.request.user)
            self.cake = Cake.objects.get(id = self.kwargs["cake_id"])

            rating = Rating.objects.get(customer = self.customer, cake = self.cake)

            return rating
        
        except Rating.DoesNotExist:
            return None
    
    def get_initial(self):
        initial = super().get_initial()

        self.obj = self.get_object()
        
        if self.obj:
            initial["customer"] = self.obj.customer
            initial["cake"] = self.obj.cake 
            initial["rate"] = self.obj.rate 
            initial["comment"] = self.obj.comment
            
        
        return initial
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cake"] = self.cake
        
        return context
            
''' 


class RatingForm(FormResponseMixin, LoginWithPermissionMixin, FormView):
    form_class = CustomerRatingForm
    permission_required = ["rating.add_rating"]
    form_success_message = "Thank you!"
    template_name = "rating/rating_form.html"

    def get_form_kwargs(self):
      context = super().get_form_kwargs()    

      context["customer"] = customer.objects.get(account = self.request.user)
      context["cake"] = Cake.objects.get(id = self.kwargs["cake_id"])

      if self.obj:
        context["initial"] = self.obj
       
      return context

    def get_object(self):
        """ 
            get the rating object with signiture of current user id and cake, return none if it is 
            a new rating
        """
        try:
            self.customer = customer.objects.get(account = self.request.user)
            self.cake = Cake.objects.get(id = self.kwargs["cake_id"])

            rating = Rating.objects.get(customer = self.customer, cake = self.cake)

            return rating
        
        except Rating.DoesNotExist:
            return None
    
    def get_initial(self):
        initial = super().get_initial()

        self.obj = self.get_object()
        
        if self.obj:
            initial["customer"] = self.obj.customer
            initial["cake"] = self.obj.cake 
            initial["rate"] = self.obj.rate 
            initial["comment"] = self.obj.comment
            
        
        return initial
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cake"] = self.cake
        
        return context
            

''' 
class RatingCreateView(FormResponseMixin, LoginWithPermissionMixin, CreateView):
    permission_required = ["rating.add_rating"]
    form_success_message = "Thank you!"
    template_name = "rating/rating_form.html"
    model = Rating
    form_class = CustomerRatingForm
    
    def get_form_kwargs(self):
        context = super().get_form_kwargs()    

        context["customer"] = customer.objects.get(account = self.request.user)
        context["cake"] = Cake.objects.get(id = self.kwargs["cake_id"])

        return context
    
    
class RatingUpdateView(UpdateView):
    model = Rating
    form_class = CustomerRatingForm 
    template_name = 'rating/rating_form.html'

    def get_object(self, queryset):
        
        self.model.objects.get(customer)
        
        return rating 
    
    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

class RatingDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        cake = get_object_or_404(Cake, id=kwargs['cake_id'])
        
        try:
            customer = customer.objects.get(account = request.user) 
            rating = Rating.objects.get(cake=cake, customer = customer)  # per-user logic
            return RatingUpdateView.as_view()(request, pk=rating.pk, customer = customer, **kwargs)
        except Rating.DoesNotExist:
            print("new rating")
            return RatingCreateView.as_view()(request, **kwargs)
