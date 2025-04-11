
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.core.exceptions import ImproperlyConfigured

class FormResponseMixin():
    
    url_success = reverse_lazy('common:form_response')   
    form_success_message = None
    def get_success_url(self):
       if self.url_success is None:
           raise ImproperlyConfigured(
               f"{self.__class__.__name__} requires 'url_success' to be set."
           )
       
       if self.form_success_message is None:
           raise ImproperlyConfigured(
               f"{self.__class__.__name__} requires 'form_success_message' to be set."
           )

       query_string = urlencode({'response': self.form_success_message})
       
       # return the url
       return f"{self.url_success}?{query_string}"