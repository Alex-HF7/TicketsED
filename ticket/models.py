from django.db import models
from django.conf import settings
from django.utils import timezone

class Ticket(models.Model):
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en curso', 'En Curso'),
        ('resuelto', 'Resuelto')
    ], default='pendiente')
    atendido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank= True,
        on_delete=models.SET_NULL,
        related_name='tickets_atendidos'
    )
    categoria = models.CharField(max_length=30, choices=[
        ('equipo', 'Equipo'),
        ('impresora', 'Impresora'),
        ('mantenimiento', 'Mantenimiento'),
        ('ofimatica', 'Ofimatica'),
        ('internet', 'Internet'),
        ('programas', 'Programas'),
        ('telefono', 'Telefono')
    ])
    tiempo_resolucion_seg = models.PositiveIntegerField(null=True, blank=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_actualizado = models.DateTimeField(auto_now=True)
    fecha_inicio_proceso = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.estado} ({self.empleado.username})"
    
    def save(self, *args, **kwargs):
        if self.estado == 'en curso' and self.fecha_inicio_proceso is None:
            self.fecha_inicio_proceso = timezone.now()

        if self.estado == "resuelto":
            if self.fecha_cierre is None:
                self.fecha_cierre = timezone.now()
            if self.fecha_inicio_proceso:
                delta = self.fecha_cierre - self.fecha_inicio_proceso
                self.tiempo_resolucion_seg = int(delta.total_seconds())
        super().save(*args, **kwargs)
    
    @property
    def tiempo(self):
        delta = self.tiempo_resolucion_seg
        if not delta:
            return None
        total = self.tiempo_resolucion_seg
        dias = total // 86400
        horas = (total % 86400) // 3600
        minutos = (total % 3600) // 60

        partes = []
        if dias:
            partes.append(f"{dias}d")
        if horas:
            partes.append(f"{horas}h")
        if minutos:
            partes.append(f"{minutos}min")
        return " ".join(partes) 
    
    class Meta:
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['empleado']),
            models.Index(fields=['fecha_creado']),
            models.Index(fields=['categoria'])
        ]