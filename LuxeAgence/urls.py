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
    path('hotels/', views.ListHotelView.as_view(), name='list_hotel'),
    path('gestionhotels/', views.GestionHotelView.as_view(), name='gesthotels'),
    path('hotels/<int:pk>/edit/', views.UpdateHotelView.as_view(), name='edit_hotel'),
    path('hotels/create/', views.CreateHotelView.as_view(), name='create_hotel'),
    path('hotels/<int:pk>/delete/', views.DeleteHotelView.as_view(), name='delete_hotel'),
    path('hotels/<int:pk>/', views.DetailHotelView.as_view(), name='detail_hotel'),
    path('rooms/', views.ListRoomView.as_view(), name='list_room'),
    path('gestionrooms/', views.GestionRoomView.as_view(), name='gestrooms'),
    path('rooms/create/', views.CreateRoomView.as_view(), name='create_room'),
    path('rooms/<int:pk>/', views.DetailRoomView.as_view(), name='detail_room'),
    path('rooms/<int:pk>/edit/', views.UpdateRoomView.as_view(), name='edit_room'),
    path('rooms/<int:pk>/delete/', views.DeleteRoomView.as_view(), name='delete_room'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)