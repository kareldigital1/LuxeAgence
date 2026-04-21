from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
# Les modèles pour les hôtels, les chambres, les réservations, les avis et les profils d'utilisateurs
#modèle pour les hôtels
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_hotels')
    image = models.ImageField(upload_to='hotels/')
    def __str__(self):
        return self.name

#modèle pour les chambres    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='rooms/', default='rooms/default.jpg')

#modèle pour les réservations
class Booking(models.Model):
    # Infos client (sans compte)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Infos réservation
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name
    
    def delete(self, *args, **kwargs):
        # rendre la chambre disponible
        self.room.available = True
        self.room.save()

        super().delete(*args, **kwargs)

#modèle pour les avis
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()        

#modèle pour les profils d'utilisateurs et les rôles
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profiles'
    )

    def __str__(self):
        return f"Profil de {self.user.username}"

    def has_permission(self, permission_codename, app_label='gestion_app'):
        if self.role is None:
            return False
        return self.role.permissions.filter(
            codename=permission_codename,
            content_type__app_label=app_label
        ).exists()
    

