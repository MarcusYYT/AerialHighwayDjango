from django.urls import path
from . import views

urlpatterns = [
    path('deploy/<str:video_filename>/', views.DeployAlgorithmView.as_view(), name='deploy_algorithm'),
    path('matchvehicle/<str:video_filename>/', views.MatchVehiclesView.as_view(), name='match_vehicle'),
    path('calculatespeed/<str:video_filename>/', views.CalculateSpeedView.as_view(), name='calculate_speed')
]