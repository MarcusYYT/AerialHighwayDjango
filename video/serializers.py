from rest_framework import serializers
from .models import Video, VideoFrame

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFrame
        fields = '__all__' # list all the fields you want to expose here

