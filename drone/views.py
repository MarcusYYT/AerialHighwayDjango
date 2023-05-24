from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Drone

# Create your views here.
from .serializers import DroneSerializer


class DroneUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        drone_id = request.data.get('drone_id')
        if not drone_id:
            return Response({"error": "Drone ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            drone = Drone.objects.get(id=drone_id)  # Assuming id is the primary key for Drone model
        except Drone.DoesNotExist:
            return Response({"error": "Drone does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        drone.users.add(user)
        drone.save()

        return Response({"message": "User successfully associated with the drone"}, status=status.HTTP_200_OK)


class DroneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        drones = Drone.objects.filter(user=user)
        drone_serializer = DroneSerializer(drones, many=True)
        return Response(drone_serializer.data)

    def post(self, request):
        user = request.user
        drone_serializer = DroneSerializer(data=request.data)
        if drone_serializer.is_valid():
            drone = drone_serializer.save(user=user)
            return Response(DroneSerializer(drone).data, status=status.HTTP_201_CREATED)
        return Response(drone_serializer.errors, status=status.HTTP_400_BAD_REQUEST)