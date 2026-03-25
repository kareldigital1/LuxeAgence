from django.contrib import admin
from Agence.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
    search_fields = ('username',)