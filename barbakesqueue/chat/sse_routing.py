from django.urls import path
from .sse_events import *

urlpatterns = [
    path('notification/', NotificationView, name='notification'), # notification
]
