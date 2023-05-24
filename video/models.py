from django.db import models

# Create your models here.
class Video(models.Model):
    video_filename = models.FileField(upload_to='videos/', unique=True)
    x_resolution = models.IntegerField(default=3840, null=True)
    y_resolution = models.IntegerField(default=2160, null=True)
    start_datetime = models.DateTimeField(null=True)
    video_latitude = models.FloatField(null=True)
    video_longitude = models.FloatField(null=True)
    drone = models.ForeignKey('drone.Drone', on_delete=models.CASCADE, null=True)

class VideoFrame(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    video_frame_cnt = models.IntegerField()
    frame_diff_time = models.IntegerField(null=True)
    frame_datetime = models.DateTimeField(null=True)
    frame_altitude = models.FloatField(null=True)
    frame_latitude = models.FloatField(null=True)
    frame_longitude = models.FloatField(null=True)
    frame_dzoom_ratio = models.FloatField(null=True)