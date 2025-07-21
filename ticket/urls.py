from django.urls import path
from .views import crear_ticket, estadisticas_tickets, dashboard_soporte, crear_ticket_ajax

urlpatterns = [
    path('crear/', crear_ticket, name='crear_ticket'),
    path('dashboard/', dashboard_soporte, name='dashboard_soporte'),
    path('stats/', estadisticas_tickets, name='estadisticas'),
    path('seguimiento/ajax/', crear_ticket_ajax, name='seguimiento_ajax')
]
