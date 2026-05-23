from django.urls import path 
from .views import *




urlpatterns = [
    # HOME PARTIE FRONT
    path("", home , name = 'home') , 
]
