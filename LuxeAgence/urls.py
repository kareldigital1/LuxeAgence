from django.contrib import admin
from django.urls import path
from Agence import views
from django.conf import settings
from django.conf.urls.static import static  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view.as_view(), name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Hotel management URLs
    path('hotels/', views.ListHotelView.as_view(), name='list_hotel'),
    path('gestionhotels/', views.GestionHotelView.as_view(), name='gesthotels'),
    path('hotels/<int:pk>/edit/', views.UpdateHotelView.as_view(), name='edit_hotel'),
    path('hotels/create/', views.CreateHotelView.as_view(), name='create_hotel'),
    path('hotels/<int:pk>/delete/', views.DeleteHotelView.as_view(), name='delete_hotel'),
    path('hotels/<int:pk>/', views.DetailHotelView.as_view(), name='detail_hotel'),

    # Room management URLs
    path('rooms/<int:hotel_id>/', views.ListRoomView.as_view(), name='list_room'),
    path('gestionrooms/', views.GestionRoomView.as_view(), name='gestrooms'),
    path('rooms/create/', views.CreateRoomView.as_view(), name='create_room'),
    path('room/<int:pk>/', views.DetailRoomView.as_view(), name='detail_room'),
    path('rooms/<int:pk>/edit/', views.UpdateRoomView.as_view(), name='edit_room'),
    path('rooms/<int:pk>/delete/', views.DeleteRoomView.as_view(), name='delete_room'),

    # Booking management URLs
    path('gestionbookings/', views.GestionBookingView.as_view(), name='gestbooking'),
    path('bookings/create/', views.CreateBookingView.as_view(), name='create_booking'),
    path('bookings/<int:pk>/', views.DetailBookingView.as_view(), name='detail_booking'),
    path('bookings/<int:pk>/edit/', views.UpdateBookingView.as_view(), name='edit_booking'),
    path('bookings/<int:pk>/delete/', views.DeleteBookingView.as_view(), name='delete_booking'),

    # Role and user management URLs
    path('gestionroles/', views.GestionRoleView.as_view(), name='gestroles'),
    path('roles/create/', views.CreateRoleView.as_view(), name='create_role'),
    path('roles/<int:pk>/edit/', views.UpdateRoleView.as_view(), name='edit_role'),
    path('roles/<int:pk>/delete/', views.DeleteRoleView.as_view(), name='delete_role'),
    path('roles/<int:pk>/', views.DetailRoleView.as_view(), name='detail_role'),
    path('gestionusers/', views.GestionUserView.as_view(), name='gestusers'),
    path('users/<int:pk>/edit/', views.ProfileUpdateRoleView.as_view(), name='edit_user'),
    path('users/<int:pk>/toggle_status/', views.toggle_user_status, name='toggle_user_status'),

    # Password reset URLs
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)