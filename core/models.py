from django.db import models
from django.utils import timezone

class EstadoServicio(models.TextChoices):
    PENDIENTE = "Pendiente", "Pendiente"
    DIAGNOSTICO = "En Diagnóstico", "En Diagnóstico"
    REPARACION = "En Reparación", "En Reparación"
    ESPERA_REPUESTOS = "En Espera de Repuestos", "En Espera de Repuestos"
    LISTO_RETIRO = "Listo para Retirar", "Listo para Retirar"
    ENTREGADO = "Entregado", "Entregado"
    CANCELADO = "Cancelado", "Cancelado"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni_cuit = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        indexes = [
            models.Index(fields=["apellido", "nombre"]),
            models.Index(fields=["dni_cuit"]),
            models.Index(fields=["telefono"]),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="servicios")
    tipo_equipo = models.CharField(max_length=100)
    marca_modelo = models.CharField(max_length=100, null=True, blank=True)
    problema_reportado = models.TextField()
    observaciones_tecnicas = models.TextField(null=True, blank=True)
    solucion_implementada = models.TextField(null=True, blank=True)

    # dinero: Decimal > float (tu yo del futuro te lo va a agradecer)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)

    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    estado_actual = models.CharField(
        max_length=50,
        choices=EstadoServicio.choices,
        default=EstadoServicio.PENDIENTE,
        db_index=True,
    )

    class Meta:
        ordering = ["-fecha_ingreso"]
        indexes = [
            models.Index(fields=["estado_actual"]),
            models.Index(fields=["fecha_ingreso"]),
            models.Index(fields=["fecha_entrega"]),
            models.Index(fields=["tipo_equipo"]),
        ]

    def __str__(self):
        return f"Servicio #{self.pk} - {self.cliente} - {self.tipo_equipo}"

class HistorialEstado(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="historial_estados")
    estado = models.CharField(max_length=50, choices=EstadoServicio.choices)
    fecha_cambio = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_cambio"]
        indexes = [models.Index(fields=["fecha_cambio"])]

    def __str__(self):
        return f"{self.servicio_id} -> {self.estado} @ {self.fecha_cambio:%Y-%m-%d %H:%M}"
