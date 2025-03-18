from django.db import models
from django.contrib.auth.models import AbstractUser

from booking import settings

class Room(models.Model):
    SINGLE_ROOM = 'single'
    STANDART_ROOM = 'standart'
    LUX_ROOM = 'lux'
    ROOM_TYPES = [
        (SINGLE_ROOM, 'Single Room'),
        (STANDART_ROOM, 'Standart Room'),
        (LUX_ROOM, 'Delux Room'),
    ]
    
    CURRENCY_TYPES = [
        ('USD', 'USD'),
        ('USD', 'EUR'),
    ]

    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price_per_night = models.IntegerField(default=150)
    currency = models.CharField(default='USD', max_length=10, choices=CURRENCY_TYPES)
    max_occupancy = models.IntegerField(default=1)
    describtion = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.name} ({self.type})'
    

class RoomImage(models.Model):
    image = models.ImageField(upload_to="room_images/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f'Image for {self.room.name} - {self.caption or 'No Caption'}'
    

class OccupiedDate(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="occupied_dates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="booked_dates")
    date = models.DateField()

    def __str__(self):
        return f'{self.date} - {self.room.name} booked by {self.user.username}'

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default="")