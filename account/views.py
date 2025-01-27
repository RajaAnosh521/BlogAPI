from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from .serializers import RegisterSerializer

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), # type: ignore
    }

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data) 
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED) 
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({"message": "User logged in successfully", "tokens": tokens}, status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "User logged out successfully"}, status.HTTP_200_OK) 