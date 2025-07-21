from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empleado

class EmpleadoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('depto', 'rol')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'rol', 'depto', 'is_staff')

admin.site.register(Empleado, EmpleadoAdmin)