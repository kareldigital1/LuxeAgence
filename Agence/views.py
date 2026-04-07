from django.shortcuts import render , redirect
from .form import CustomUserCreationForm, HotelForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Hotel, Booking, Room
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView
from django.db.models import Q


# Create your views here.
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
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(room_number__icontains=q) | Q(room_type__icontains=q) | Q(capacity__icontains=q)
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
class DetailRoomView(LoginRequiredMixin,DetailView):
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
class DetailBookingView(LoginRequiredMixin,DetailView):
    model = Booking
    template_name = 'bookings/detail_booking.html'
    context_object_name = 'booking'

#Pour créer une reservation
class CreateBookingView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/form_booking.html' 
    success_url = '/gestionbookings/'

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

#Pour modifier une reservation
class UpdateBookingView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/form_booking.html' 
    success_url = '/gestionbookings/'

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
    login_url = 'login_view'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nb_hotels'] = Hotel.objects.count()
        context['nb_reservations'] = Booking.objects.count()
        context['nb_chambres'] = Room.objects.count()

        return context



#Pour s'inscrire
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_hotel')
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