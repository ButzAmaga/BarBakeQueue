from django.urls import path, include
from .views import * 

app_name = 'common'

urlpatterns = [
    path('response', FormResponse.as_view(), name='form_response'), # form response
] 
