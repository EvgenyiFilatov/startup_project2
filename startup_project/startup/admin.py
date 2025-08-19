from django.contrib import admin
from .models import CustomUser, Startup


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator')
