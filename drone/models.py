from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Drone(models.Model):
    drone_brand = models.CharField(max_length=20, null=True)
    drone_model = models.CharField(max_length=20, null=True)
    drone_magnification = models.FloatField(default=1.33, null=True)
    users = models.ManyToManyField(User, related_name='drones')

    class Meta:
        db_table = 'drone'
        verbose_name = 'Drone'
        verbose_name_plural = 'Drones'