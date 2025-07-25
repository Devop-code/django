from pyexpat import model
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['username' , 'password' , 'email']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self , validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    def validate(self , data):
        user = authenticate(**data)
        if user and user.is_active:
            return user