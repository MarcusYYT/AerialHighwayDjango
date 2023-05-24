from django.urls import path
from .views import DroneAPIView, DroneUserAPIView

urlpatterns = [
    path('', DroneAPIView.as_view(), name='drones'),
    path('drones/user/', DroneUserAPIView.as_view(), name='drone_user'),
]