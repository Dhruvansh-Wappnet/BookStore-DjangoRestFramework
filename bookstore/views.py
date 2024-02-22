# views.py
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Booking, OTP, ResetToken
from .serializers import BookSerializer, BookingSerializer, UserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
import random
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Authentication successful
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ForgetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

       # Check if an OTP object already exists for the email
        otp_object, created = OTP.objects.get_or_create(email=email)

        # Update the existing OTP object or delete and create a new one
        if not created:
            otp_object.otp = otp
            otp_object.save()
        else:
            otp_object = OTP.objects.create(email=email, otp=otp)

        # Send email with OTP
        subject = 'Password Reset OTP'
        message = f'Your OTP for password reset is: {otp}'
        from_email = 'dev1.wappnet@gmail.com'  # Update with your email address
        to_email = [email]

        try:
            send_mail(subject, message, from_email, to_email)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        # Check if OTP matches stored OTP for the user
        try:
            stored_otp = OTP.objects.get(email=email).otp
        except OTP.DoesNotExist:
            return Response({'error': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

        if otp == stored_otp:
            # OTP verification successful
            # Generate token
            user = User.objects.get(email=email)  # Assuming you have a User model
            token, _ = Token.objects.get_or_create(user=user)
            # token = token.generate_token()

            # Save token to the database (optional if not already saved)
            # token.save()

            return Response({'message': 'OTP verified successfully', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Invalid OTP
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ResetPasswordAPIView(APIView):
    def post(self, request):
        new_password = request.data.get('new_password')
        token = request.data.get('token')

        # Verify token against the one stored in the database
        try:
            reset_token = ResetToken.objects.get(token=token)
        except ResetToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if reset_token.expired():
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Update password, encode it, and delete the token
        user = reset_token.user
        user.password = make_password(new_password)
        user.save()
        reset_token.delete()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class AddBookAPIView(APIView):
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAPIView(APIView):
    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assuming using authentication
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)