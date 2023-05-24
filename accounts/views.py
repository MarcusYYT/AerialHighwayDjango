from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import token_backend

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class GetUsernameView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        username = get_username_from_token(token)

        if username is None:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'username': username}, status=status.HTTP_200_OK)


def get_username_from_token(token):
    try:
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        print(e)
        return None

    id = token_backend.decode(token)['user_id']
    return User.objects.get(id=id).username
