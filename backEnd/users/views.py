from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Login View
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Logout View
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Assuming TokenAuthentication is used
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# User Settings Update
class UpdateSettingsView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

# Update Topics View (could be combined with UpdateSettingsView)
class UpdateTopicsView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer  # Alternatively, create a separate serializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

# User Detail View (optional, for fetching user info)
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
