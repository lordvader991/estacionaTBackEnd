from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
        email = models.EmailField()
        phone = models.CharField(max_length=50)
        rol_usuario = models.BooleanField(default=False)
        correo_auth = models.BooleanField(default=False)
        created_at= models.DateTimeField(auto_now_add=True)
        updated_at= models.DateTimeField(auto_now=True)
        
