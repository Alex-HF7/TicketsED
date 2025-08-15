from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', crear_ticket, name='crear_ticket'),
    path('dashboard/', dashboard_soporte, name='dashboard_soporte'),
    path('stats/', estadisticas_tickets, name='estadisticas'),
    path('seguimiento/ajax/', crear_ticket_ajax, name='seguimiento_ajax'),
    path('editar/<int:ticket_id>/', editar_ticket, name='editar_ticket'),
    path('eliminar/<int:ticket_id>/', eliminar_ticket, name='eliminar_ticket'),
]
