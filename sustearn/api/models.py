from django.db import models

# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=100)
    life_cycle_stages = models.JSONField()
    weights = models.JSONField()
    weighted_average_emission = models.FloatField()
    optimized_emission = models.FloatField()

    