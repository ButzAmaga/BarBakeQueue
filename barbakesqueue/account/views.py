from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

# Create your views here.
class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True  # Redirect already authenticated users

    def get_success_url(self):
        if self.request.user.groups.first().name == 'Staff':
            return reverse_lazy('order:orders')
        else:
            return reverse_lazy('main:cake_page') # a customer account 

            

class Login_first_promp(generic.TemplateView):
    template_name = 'account/login_first_promp.html'

    
# Permissions 
class GroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    # add value to who inherit
    group_required = None

    def test_func(self):
        if self.group_required:
            return self.request.user.groups.filter(name=self.group_required).exists()
        
        return False

    def handle_no_permission(self):
        return HttpResponseRedirect(redirect_to=reverse_lazy("account:login_promp"))

class StaffPermission(GroupRequiredMixin):
    group_required = 'Staff'

class CustomerPermission(GroupRequiredMixin):
    group_required = 'Customer' 