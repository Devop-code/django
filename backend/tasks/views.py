import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializer import LoginSerializer, RegisterSerializer, TaskSerializer
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
class RegisterView(APIView):
    serializer_class =  RegisterSerializer
    def post(self , request):
        serializer =  self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = Response({'message': 'Register successful'}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer_class = LoginSerializer
    def post(self , request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            
            access_token = str(refresh.access_token)
            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class= TaskSerializer
    permission_classes = [IsAuthenticated]

class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self , request , pk):
        task = Task.objects.get(pk=pk)
        if  task.user != request.user:
            return Response(status=403)
        task.delete()
        
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        user = request.user
        return  Response(
            {'id': user.id,
            'email': user.email,
            'username': user.username,}
        )

class Logout(APIView):
    def post(self,request):
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response