from datetime import datetime, timedelta
from .models import Ticket
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.template.loader import render_to_string
from calendar import monthrange
from django.templatetags.static import static
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
import pandas as pd
import plotly.express as px
import json
import io

@login_required
def crear_ticket(request):
    if request.user.rol not in ['soporte','admin', 'empleado']:
        return HttpResponseForbidden("NO TIENES ACCESO")    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            descripcion = data.get('descripcion')
            categoria = data.get('categoria')
            if not descripcion or not categoria:
                return JsonResponse({'succes': False, 'error': 'Faltan campos obligatorios'})
            ticket = Ticket.objects.create(
                empleado = request.user,
                descripcion = descripcion,
                categoria= categoria
            )

            return JsonResponse({'success': True, 'ticket_id': ticket.id})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido.'}, status=400)
        
    tickets_user = Ticket.objects.filter(empleado = request.user).order_by('-fecha_creado')[:5]
    return render(request, 'ticket/crear_ticket.html',{
        'tickets_user': tickets_user
    })

@login_required
def crear_ticket_ajax(request):
    tickets_user = Ticket.objects.filter(empleado = request.user).order_by('-fecha_creado')[:5]
    html = render_to_string('ticket/seguimiento.html', {'tickets_user': tickets_user})
    return HttpResponse(html)

@login_required
def dashboard_soporte(request):
    if request.user.rol not in ['soporte','admin']:
        return HttpResponseForbidden("Acceso restringido a soporte.")
    
    # --- Exportar a Excel si se solicita ---
    if request.GET.get('exportar') == 'excel':
        mes_str = request.GET.get('mes')
        today = datetime.today()

        if mes_str:
            try:
                selected_date = datetime.strptime(mes_str, '%Y-%m')
            except ValueError:
                selected_date = today
        else:
            selected_date = today

        first_day = selected_date.replace(day=1)
        last_day = selected_date.replace(day=monthrange(selected_date.year, selected_date.month)[1])

        queryset = Ticket.objects.filter(fecha_creado__range=(first_day, last_day)).select_related('empleado', 'atendido_por')

        df = pd.DataFrame.from_records(queryset.values(
            'id',
            'descripcion',
            'categoria',
            'estado',
            'empleado__first_name',
            'empleado__last_name',
            'empleado__depto',
            'atendido_por__username',
            'tiempo_resolucion_seg',
            'fecha_creado',
            'fecha_cierre'
        ))

        # Renombrar columnas
        df.rename(columns={
            'id': 'ID',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'estado': 'Estado',
            'empleado__first_name': 'Nombre',
            'empleado__last_name': 'Apellido',
            'empleado__depto': 'Departamento',
            'atendido_por__username': 'Atendido por',
            'tiempo_resolucion_seg': 'Duración',
            'fecha_creado': 'Fecha Ingreso',
            'fecha_cierre': 'Fecha Cierre'
        }, inplace=True)

        for col in ['Fecha Ingreso', 'Fecha Cierre']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
        output = io.BytesIO()
        df.to_excel(output, index=False, sheet_name='Tickets')
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"tickets_{selected_date.strftime('%Y_%m')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        accion = request.POST.get('accion')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if accion == 'atender' and ticket.estado == 'pendiente':
                ticket.estado = 'en curso'
                ticket.atendido_por = request.user
                ticket.save()
            elif accion == 'cerrar' and ticket.estado == 'en curso':
                ticket.estado = 'resuelto'
                ticket.atendido_por = request.user
                ticket.save()
            messages.success(request, f"Ticket #{ticket_id} actualizado.")
        except Ticket.DoesNotExist:
            messages.error(request, "El ticket no existe")
        
        return redirect('dashboard_soporte')
    
    tickets_list = Ticket.objects.select_related('empleado','atendido_por').order_by('-fecha_creado')
    paginator = Paginator(tickets_list, 15)

    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)

    return render(request, 'soporte/dashboard.html', {
        'tickets': tickets,
        'categorias': Ticket._meta.get_field('categoria').choices
        })

@login_required
def estadisticas_tickets(request):
    if request.user.rol not in ['soporte','admin']:
        return HttpResponseForbidden("Acceso restringido.")

    # Obtener mes desde parámetro GET, por defecto el mes actual
    mes_str = request.GET.get('mes')
    today = now()

    if mes_str:
        try:
            selected_date = datetime.strptime(mes_str, '%Y-%m')
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    first_day = selected_date.replace(day=1)
    last_day = selected_date.replace(day=monthrange(selected_date.year, selected_date.month)[1])

    queryset = Ticket.objects.filter(fecha_creado__range=(first_day, last_day))

    df = pd.DataFrame.from_records(queryset.values(
        'categoria', 'empleado__depto', 'estado'
    ))

    if df.empty:
        context = {
            'sin_datos': True,
            'mes': selected_date.strftime('%B %Y'),
            'selected_month': selected_date.strftime('%Y-%m'),
        }
        return render(request, 'soporte/estadisticas.html', context)
     # Grafica de Pastel
    df['categoria'] = df['categoria'].str.title()
    fig_categoria = px.pie(
        df, 
        names='categoria', 
        title='Categorías más reportadas',
        labels={'categoria':'Categorias'}
        )
    chart_categoria = fig_categoria.to_html(full_html=False)

     # Grafica de Barras
    df_deptos = df.groupby('empleado__depto').size().reset_index(name='total')
    fig_deptos = px.bar(
        df_deptos,
        x='empleado__depto', 
        y='total',
        color= 'empleado__depto', 
        title='Reportes por departamento',
        labels={
            'empleado__depto': 'Departamento',
            'total': 'Número de Tickets'
        })
    chart_deptos = fig_deptos.to_html(full_html=False)

    total_resueltos = len(df[df['estado'] == 'resuelto'])
    meta_mensual = 30 
    progreso = min (round((total_resueltos / meta_mensual)* 100 ), 100)

    context = {
        'chart_categoria': chart_categoria,
        'chart_deptos': chart_deptos,
        'total_resueltos': total_resueltos,
        'progreso': progreso,
        'meta_mensual': meta_mensual,
        'mes': selected_date.strftime('%B %Y'),
        'selected_month': selected_date.strftime('%Y-%m'),
        'sin_datos': False
    }
    
    return render(request, 'soporte/estadisticas.html', context)

@require_POST
@login_required
def editar_ticket(request, ticket_id):
    if request.user.rol not in ['soporte', 'admin']:
        return HttpResponseForbidden("No autorizado.")

    descripcion = request.POST.get('descripcion')
    categoria = request.POST.get('categoria')

    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.descripcion = descripcion
        ticket.categoria = categoria
        ticket.save()
        messages.success(request, f"Ticket #{ticket_id} actualizado correctamente.")
    except Ticket.DoesNotExist:
        messages.error(request, "Ticket no encontrado.")

    return redirect('dashboard_soporte')


@require_POST
@login_required
def eliminar_ticket(request, ticket_id):
    if request.user.rol not in ['soporte', 'admin']:
        return HttpResponseForbidden("No autorizado.")
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
        messages.success(request, f"Ticket #{ticket_id} eliminado.")
    except Ticket.DoesNotExist:
        messages.error(request, "El ticket no existe.")
    
    return redirect('dashboard_soporte')