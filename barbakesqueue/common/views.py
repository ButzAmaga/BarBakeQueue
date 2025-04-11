from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin 
from django.views import generic
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.core.exceptions import ImproperlyConfigured

class LoginWithPermissionMixin(PermissionRequiredMixin, LoginRequiredMixin):
    raise_exception = True
    permission_required = "None"


    

class FormResponse(generic.TemplateView):
    template_name = "common/form_response/response.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["response"] = self.request.GET.get("response", "No response data inputted") 
        return context
    