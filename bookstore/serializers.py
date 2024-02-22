# serializers.py
from rest_framework import serializers
from .models import Book, Booking
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        # Hash the password before creating the user
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['book']
