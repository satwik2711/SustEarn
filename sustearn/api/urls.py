from django.urls import path
from .views import *

urlpatterns = [
    path('calculate/', calculate_footprint, name='calculate_footprint'),
]