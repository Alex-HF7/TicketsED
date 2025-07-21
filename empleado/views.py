from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Empleado


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            if user.rol in 'soporte admin':
                return redirect('estadisticas')
            elif user.rol == 'empleado':
                return redirect('crear_ticket')
            else:
                messages.error(request, "Tu rol no tiene acceso.")
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, 'empleado/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')