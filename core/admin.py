from django.contrib import admin
from .models import Cliente, Servicio, HistorialEstado

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "dni_cuit", "telefono", "email")
    search_fields = ("nombre", "apellido", "dni_cuit", "telefono", "email")
    ordering = ("apellido", "nombre")

class HistorialInline(admin.TabularInline):
    model = HistorialEstado
    extra = 0
    readonly_fields = ("fecha_cambio",)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "tipo_equipo", "estado_actual", "fecha_ingreso", "fecha_entrega", "costo_total")
    list_filter = ("estado_actual", "tipo_equipo")
    search_fields = ("id", "cliente__nombre", "cliente__apellido", "cliente__dni_cuit", "tipo_equipo", "marca_modelo")
    autocomplete_fields = ("cliente",)
    inlines = [HistorialInline]

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ("servicio", "estado", "fecha_cambio")
    list_filter = ("estado",)
    search_fields = ("servicio__id", "observaciones")
