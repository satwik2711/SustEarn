from django.urls import path
from .views import *

urlpatterns = [
    path('calculate/', calculate_footprint, name='calculate_footprint'),
    path('lcs', get_life_cycle_stages, name='get_life_cycle_stages'),
    # path('lca', fetch_industry_benchmark_lca, name='fetch_industry_benchmark_lca'),
]