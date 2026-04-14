from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, Booking, Room
from datetime import date
# Create your models here.

# Formulaire pour la création d'un nouvel utilisateur
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

# Formulaire pour la création et la mise à jour des hôtels
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

# Formulaire pour la création et la mise à jour des réservations
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'room', 'check_in', 'check_out']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone', 'required': True}),
            'room': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'check_in': forms.DateInput(
                        format='%Y-%m-%d',
                        attrs={'class': 'form-control', 'type': 'date'}
                    ),
            'check_out': forms.DateInput(
                        format='%Y-%m-%d',
                        attrs={'class': 'form-control', 'type': 'date'}
                    ),
        }

    # Personnalisation du formulaire pour ajouter des contraintes sur les dates et la disponibilité des chambres
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add today's date as minimum date for check_in and check_out
        today = date.today().isoformat()
        if 'check_in' in self.fields:
            self.fields['check_in'].widget.attrs['min'] = today
        if 'check_out' in self.fields:
            self.fields['check_out'].widget.attrs['min'] = today

        # Limit room choices to available rooms (used in admin creation)
        try:
            self.fields['room'].queryset = Room.objects.filter(available=True)
        except Exception:
            # in case models aren't ready or in migrations, fallback to all rooms
            self.fields['room'].queryset = Room.objects.all()

    # Validation pour s'assurer que la chambre sélectionnée est disponible
    def clean_room(self):
        room = self.cleaned_data['room']
        if not room.available:
            raise forms.ValidationError("Cette chambre n'est pas disponible")
        return room
    # Validation pour s'assurer que les dates sont valides
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_in < date.today():
            self.add_error('check_in', "La date d'entrée ne peut pas être dans le passé")

        if check_out and check_out < date.today():
            self.add_error('check_out', "La date de sortie ne peut pas être dans le passé")

        if check_in and check_out and check_out <= check_in:
            self.add_error('check_out', "La date de sortie doit être après la date d'entrée")

# Formulaire pour la création et la mise à jour des chambres
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
