from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Booking)
admin.site.register(ReturningBook)
# admin.site.register(OTP)
# admin.site.register(ResetToken)