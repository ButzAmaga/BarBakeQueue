from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin 

class LoginWithPermissionMixin(PermissionRequiredMixin, LoginRequiredMixin):
    raise_exception = True
    permission_required = "None"