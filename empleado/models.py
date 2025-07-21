from django.db import models
from django.contrib.auth.models import AbstractUser

class Empleado(AbstractUser):
    ROLES = (
        ('empleado', 'Empleado'),
        ('soporte','Soporte'),
        ('admin', 'Admin'),
    )
    DEPTO =(
        ('Dir General', 'Direccion General'),
        ('Del Administrativa', 'Delegación Administrativa'),
        ('UCG', 'Unidad de Control de Gestion'), 
        ('Sub Jurídica', 'Subdirección Jurídica'), 
        ('Sub Planeación', 'Subdirección de Planeación'), 
        ('Sub Comercialización', 'Subdirección de Comercialización'), 
        ('Sub Técnica', 'Subdirección Técnica')
    )
    depto = models.CharField(max_length=100, choices=DEPTO)
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')

    def __str__(self):
        return f"{self.username} ({self.rol})"
