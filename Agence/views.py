from django.shortcuts import render , redirect, get_object_or_404
from .form import CustomUserCreationForm, HotelForm, BookingForm, ProfileRoleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Hotel, Booking, Room, Profile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView
from django.db.models import Q, Count, Sum, F
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .form import RoleForm, PERMISSION_TRANSLATIONS, CustomPasswordResetForm, CustomSetPasswordForm
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
import json
from django.utils import timezone
from datetime import timedelta


# Les classes
#Pour afficher la page d'accueil
class HomeView(TemplateView):
    template_name = 'home/home.html'

#Pour se deconnecter
class logout_view(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('home')    

#Pour afficher la page à propos
class AboutView(TemplateView):
    template_name = 'home/about.html'

#Pour afficher la page de contact
class ContactView(TemplateView):
    template_name = 'home/contact.html'

#Pour afficher la liste des hotels avec une barre de recherche
class ListHotelView(ListView):
    template_name = 'hotels/list_hotel.html'
    model = Hotel
    context_object_name = 'hotels'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(city__icontains=q) | Q(country__icontains=q)
            )
        return queryset

#Pour afficher la liste des chambres 
class ListRoomView(ListView):
    template_name = 'rooms/list_room.html'
    model = Room
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = super().get_queryset()

        # 🔥 récupérer l'id de l'hôtel depuis l'URL
        hotel_id = self.kwargs.get('hotel_id')

        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)

        # 🔍 recherche
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(room_number__icontains=q) |
                Q(room_type__icontains=q) |
                Q(capacity__icontains=q)
            )

        return queryset
    
#Pour afficher la liste des reservations des utilisateur
class ListBookingView(LoginRequiredMixin,ListView):
    template_name = 'bookings/list_booking.html'
    model = Booking
    context_object_name = 'bookings'

    
#Pour afficher la page de gestion des hotels pour les administrateurs
#Pour modifier un hotel
class UpdateHotelView(LoginRequiredMixin,UpdateView):
    template_name = 'hotels/form_hotel.html' 
    model = Hotel
    fields = ['name', 'description', 'country', 'city', 'address', 'owner', 'image']
    success_url = '/gestionhotels/'

#Pour ajouter un hotel
class CreateHotelView(LoginRequiredMixin,CreateView):
    template_name = 'hotels/form_hotel.html' 
    model = Hotel
    fields = ['name', 'description', 'country', 'city', 'address', 'owner', 'image']
    success_url = '/gestionhotels/'    

#Pour supprimer un hotel
class DeleteHotelView(LoginRequiredMixin,DeleteView):
    model = Hotel
    success_url = '/gestionhotels/'    

#Pour afficher les details d'un hotel
class DetailHotelView(DetailView):
    template_name = 'hotels/detail_hotel.html'
    model = Hotel
    context_object_name = 'hotel'

#Pour afficher la page de gestion des hotels pour les administrateurs
class GestionHotelView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'administrateur/gesthotels.html'
    context_object_name = 'hotels'      

#Pour afficher la page de gestion des chambres pour les administrateurs
class GestionRoomView(LoginRequiredMixin,ListView):
    model = Room
    template_name = 'administrateur/gestrooms.html'
    context_object_name = 'rooms'

#Pour créer une chambre
class CreateRoomView(LoginRequiredMixin,CreateView):
    model = Room
    template_name = 'rooms/form_room.html' 
    fields = ['hotel', 'room_number', 'room_type', 'price_per_night', 'available', 'capacity', 'image']
    success_url = '/gestionrooms/'

#Pour afficher les details d'une chambre
class DetailRoomView(DetailView):
    model = Room
    template_name = 'rooms/detail_room.html'
    context_object_name = 'room'

#Pour modifier une chambre
class UpdateRoomView(LoginRequiredMixin,UpdateView):
    model = Room
    template_name = 'rooms/form_room.html' 
    fields = ['hotel', 'room_number', 'room_type', 'price_per_night', 'available', 'capacity', 'image']
    success_url = '/gestionrooms/'

#Pour supprimer une chambre
class DeleteRoomView(LoginRequiredMixin,DeleteView):
    model = Room
    success_url = '/gestionrooms/'

#Pour afficher la page de gestion des reservations pour les administrateurs
class GestionBookingView(LoginRequiredMixin,ListView):
    model = Booking
    template_name = 'administrateur/gestbooking.html'
    context_object_name = 'bookings'

#Pour afficher les details d'une reservation
class DetailBookingView(DetailView):
    model = Booking
    template_name = 'bookings/detail_booking.html'
    context_object_name = 'booking'

#Pour créer une reservation
class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/form_booking.html'
    
    def get_success_url(self):
        return reverse('detail_booking', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.request.GET.get('room_id')  # 🔥 récupérer l'id de la chambre si présent
        
        if room_id:
            # Si une chambre spécifique est demandée, afficher uniquement cette chambre
            context['rooms'] = Room.objects.filter(id=room_id)
            context['single_room'] = True
        else:
            # Sinon, afficher toutes les chambres disponibles (pour accès via admin)
            context['rooms'] = Room.objects.filter(available=True)  # 🔥 seulement chambres dispo
            context['single_room'] = False
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)

        #  Calcul du prix total
        nights = (booking.check_out - booking.check_in).days
        booking.total_price = nights * booking.room.price_per_night

        booking.save()

        #  RENDRE LA CHAMBRE INDISPONIBLE
        room = booking.room
        room.available = False
        room.save()

        return super().form_valid(form)

#Pour modifier une reservation
class UpdateBookingView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/form_booking.html' 
    
    def get_success_url(self):
        return reverse('detail_booking', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        nights = (booking.check_out - booking.check_in).days
        booking.total_price = nights * booking.room.price_per_night
        booking.save()
        return super().form_valid(form)

#Pour supprimer une reservation
class DeleteBookingView(LoginRequiredMixin,DeleteView):
    model = Booking
    success_url = '/gestionbookings/'

#Pour afficher le dashboard de l'administrateur avec les statistiques
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'administrateur/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Compteurs principaux
        context['nb_hotels'] = Hotel.objects.count()
        context['nb_reservations'] = Booking.objects.count()
        context['nb_chambres'] = Room.objects.count()
        context['nb_utilisateurs'] = User.objects.filter(is_active=True).count()

        # Réservations par hôtel
        reservations_par_hotel = (
            Booking.objects
            .values('room__hotel__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        context['hotels_chart_labels'] = [item['room__hotel__name'] for item in reservations_par_hotel]
        context['hotels_chart_data'] = [item['count'] for item in reservations_par_hotel]

        # Chambres par type
        chambres_par_type = (
            Room.objects
            .values('room_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['types_chart_labels'] = [item['room_type'] for item in chambres_par_type]
        context['types_chart_data'] = [item['count'] for item in chambres_par_type]

        # Réservations par mois (derniers 6 mois)
        mois_data = {}
        for i in range(6):
            date = timezone.now() - timedelta(days=30*i)
            mois_key = date.strftime('%B')
            mois_data[mois_key] = Booking.objects.filter(
                created_at__year=date.year,
                created_at__month=date.month
            ).count()
        
        context['mois_labels'] = list(reversed(list(mois_data.keys())))
        context['mois_data'] = list(reversed(list(mois_data.values())))

        # Taux d'occupation
        total_chambres = Room.objects.count()
        chambres_libres = Room.objects.filter(available=True).count()
        chambres_occupees = total_chambres - chambres_libres
        context['taux_occupation'] = round((chambres_occupees / total_chambres * 100) if total_chambres > 0 else 0, 1)
        context['chambres_occupees'] = chambres_occupees
        context['chambres_libres'] = chambres_libres
        return context

#Pour afficher la liste des rôles
class GestionRoleView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'administrateur/gestroles.html'
    context_object_name = 'roles'

    def get_queryset(self):
        return Group.objects.annotate(
            user_count=Count('profiles')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vérifier si l'utilisateur a la permission pour afficher "Actions"
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile') and self.request.user.profile.role:
            context['can_manage_roles'] = self.request.user.profile.role.permissions.filter(
                codename__in=['change_group', 'view_group']
            ).exists()
        else:
            context['can_manage_roles'] = False
        return context

# Pour afficher les details d'un rôle avec la traduction des permissions
class DetailRoleView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'roles/detail_role.html'
    context_object_name = 'role'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        translated_permissions = []
        for permission in self.object.permissions.all():
            label = PERMISSION_TRANSLATIONS.get(permission.codename, permission.name)
            translated_permissions.append({
                'codename': permission.codename,
                'label': label
            })

        context['translated_permissions'] = translated_permissions
        return context

# Pour créer un rôle avec la traduction des permissions
class CreateRoleView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = RoleForm
    template_name = 'roles/form_role.html'
    success_url = reverse_lazy('gestroles')

# Pour modifier un rôle avec la traduction des permissions
class UpdateRoleView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = RoleForm
    template_name = 'roles/form_role.html'
    success_url = reverse_lazy('gestroles')

# Pour supprimer un rôle
class DeleteRoleView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'roles/role_confirm_delete.html'
    success_url = reverse_lazy('gestroles')


# Pour afficher la page de gestion des utilisateurs pour les administrateurs
class GestionUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'administrateur/gestusers.html' 
    context_object_name = 'users'

# Pour modifier le rôle d'un utilisateur
class ProfileUpdateRoleView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileRoleForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('gestusers')
    
    def get_object(self, queryset=None):
        # Récupère le profil de l'utilisateur via l'ID utilisateur dans l'URL
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

#Les fonctions
@login_required
def toggle_user_status(request, pk):
    if not request.user.profile.has_permission('change_user', app_label='auth'):
        raise PermissionDenied("Vous n'avez pas le droit de modifier les utilisateurs.")

    user = get_object_or_404(User, pk=pk)

    # éviter de se désactiver soi-même
    if user == request.user:
        raise PermissionDenied("Vous ne pouvez pas désactiver votre propre compte.")

    user.is_active = not user.is_active
    user.save()

    return redirect('gestusers')    

#Pour afficher la page de réinitialisation du mot de passe
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
# Pour personnaliser les vues de réinitialisation du mot de passe avec des templates personnalisés et des formulaires personnalisés
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form_CUSTOM.html'
    email_template_name = 'registration/password_reset_email_CUSTOM.html'
    subject_template_name = 'registration/password_reset_subject_CUSTOM.txt'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

# Pour personnaliser la vue de confirmation de réinitialisation du mot de passe avec un template personnalisé et un formulaire personnalisé
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done_CUSTOM.html'

# Pour personnaliser la vue de confirmation de réinitialisation du mot de passe avec un template personnalisé et un formulaire personnalisé
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm_CUSTOM.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

# Pour personnaliser la vue de confirmation de réinitialisation du mot de passe avec un template personnalisé
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete_CUSTOM.html'

#Pour s'inscrire
@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestusers')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#Pour se connecter
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login_view.html') 