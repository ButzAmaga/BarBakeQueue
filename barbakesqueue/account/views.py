from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


# Create your views here.
class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True  # Redirect already authenticated users

    def get_success_url(self):
        if self.request.user.groups.first().name == 'Staff':
            return reverse_lazy('chat:main')
        else:
            return reverse_lazy('main:index') # a customer account 