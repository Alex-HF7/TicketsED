from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('empleado.urls')),
    path('ticket/', include('ticket.urls')),
]
