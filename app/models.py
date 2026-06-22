from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    name = models.CharField(max_length=64) # Name of Consumer/Provider Platform
    tagline = models.CharField(max_length=32, default='') # Tagline for Consumer/Provider Platform
    description = models.TextField(default='') # Description of Consumer/Provider Platform
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile_picture.jpg')
    account_type = models.CharField(max_length=16, default='client') # Consumer/Provider
    location = models.CharField(max_length=32, default='Faisalabad') # Availability Location
    contact = models.CharField(max_length=16, default='') # Contact Number
    # varification_status = models.BooleanField(default=False) # Whether the profile is verified by admin or not
    # years_active = models.IntegerField(default=0) # Years Active in the field (for providers)

    created_at = models.DateTimeField(auto_now_add=True)

class Tags(models.Model):
    name = models.CharField(max_length=32)

class Services(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='serving_profile')
    title = models.CharField(max_length=64, default='')
    description = models.TextField(default='')
    tags = models.ManyToManyField(Tags, blank=True)
    category = models.CharField(max_length=32, default='Other') # Category of the service (e.g., Catering, Decoration, etc.)
    costs = models.IntegerField()
    rate = models.IntegerField(default=50)
    cover_picture = models.ImageField(upload_to='service_covers/', default='default_service_cover.jpg')

    created_at = models.DateTimeField(auto_now_add=True)

class Event_Extras(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service_extras')
    add_on = models.CharField(max_length=16)
    rate = models.IntegerField()

class Bookings(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='booking_service')
    consumer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='booking_consumer')
    provider = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='booking_provider')
    date = models.DateField(default=None, null=True)
    location = models.CharField(max_length=32, default='Faisalabad')
    guests = models.IntegerField(default=0)
    charges = models.IntegerField(default=0)
    status = models.CharField(max_length=16, default='pending') # pending/accepted/rejected/completed

    extras = models.ManyToManyField(Event_Extras, blank=True, related_name='booking_extras')

    created_at = models.DateTimeField(auto_now_add=True)


# class Dashboard(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dashboard_profile')
#     performance = models.FloatField(default=0.0) # Average rating based on consumer reviews
#     upcoming_bookings = models.ManyToManyField(Bookings, blank=True, related_name='dashboard_upcoming_bookings')
#     bookings_done = models.ManyToManyField(Bookings, blank=True, related_name='dashboard_bookings_done')


#     created_at = models.DateTimeField(auto_now_add=True)


