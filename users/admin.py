from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Aggiungiamo il nostro campo personalizzato alla schermata di modifica
    fieldsets = UserAdmin.fieldsets + (
        ('Permessi E-commerce', {'fields': ('is_store_manager',)}),
    )
    
    # Le colonne che vedremo nella lista principale
    list_display = ['username', 'email', 'is_store_manager', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)