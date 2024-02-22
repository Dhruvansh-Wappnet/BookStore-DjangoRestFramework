from django.db import models
import uuid, random, string
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.title} Book ID: {self.id}'

class Booking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date_time = models.DateTimeField(auto_now_add=True)
    # returning_date_time = models.DateTimeField()
    
    def __str__(self):
        return f'Booking ID: {self.id} , User: {self.user.username} , Book: {self.book.title} , Book ID: {self.id} , Booking Time: {self.booking_date_time}'

class ReturningBook(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    returning_date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Returning ID: {self.id} , Booking ID: {self.booking.id} , Book ID: {self.id} , Returning Time: {self.returning_date_time}'

class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email}"

class ResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, unique=True, default='', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))  # Default expiry in 1 day

    def __str__(self):
        return f"Reset token for {self.user.username}"

    def generate_token(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=6))
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)