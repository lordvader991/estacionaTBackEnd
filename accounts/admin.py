from django.contrib import admin
from .models import User  # Asegúrate de importar tu modelo de usuario personalizado si estás usando uno

class UserAdmin(admin.ModelAdmin):
    search_fields = ['name', 'lastname', 'email', 'phone']  # Definir los campos que quieres que sean buscables en el administrador

admin.site.register(User, UserAdmin)