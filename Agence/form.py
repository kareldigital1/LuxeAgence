from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, Booking, Room
# Create your models here.

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'country', 'city', 'address', 'owner', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'hôtel', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description de l\'hôtel'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'required': True}),
            'owner': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'room', 'check_in', 'check_out', 'total_price']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone', 'required': True}),
            'room': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix total', 'required': True, 'step': '0.01'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_number', 'room_type', 'price_per_night', 'available', 'capacity', 'image']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de la chambre', 'required': True}),
            'room_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type de chambre', 'required': True}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix par nuit', 'required': True, 'step': '0.01'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacité', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
