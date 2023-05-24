from django.apps import AppConfig
from .detect_track import VehicleTrackerSingleton


class VehicleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehicle'

    def ready(self):
        # This will load the model when Django starts
        VehicleTrackerSingleton.getInstance()