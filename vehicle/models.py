from django.db import models

# Create your models here.
class Vehicle(models.Model):
    entry_frame_cnt = models.IntegerField(null=True)
    departure_frame_cnt = models.IntegerField(null=True)
    video_filename = models.CharField(max_length=20, null=True)
    track_id = models.IntegerField()
    image = models.CharField(max_length=40, null=True)
    avg_speed = models.IntegerField(null=True)
    max_speed = models.IntegerField(null=True)

class VehicleFrame(models.Model):
    track_id = models.IntegerField()
    video_filename = models.CharField(max_length=20, null=True)
    video_frame_cnt = models.IntegerField()
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    speed = models.IntegerField(null=True)
    # image = models.ImageField(upload_to="vehicle_imgs")