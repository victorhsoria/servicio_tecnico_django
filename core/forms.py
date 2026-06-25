from django import forms
from django.utils import timezone
from .models import Cliente, Servicio, HistorialEstado, EstadoServicio

def add_bootstrap(form: forms.Form):
    for name, field in form.fields.items():
        widget = field.widget
        base = widget.attrs.get("class", "")
        if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.DateTimeInput)):
            widget.attrs["class"] = (base + " form-control").strip()
        elif isinstance(widget, forms.Textarea):
            widget.attrs["class"] = (base + " form-control").strip()
        elif isinstance(widget, forms.Select):
            widget.attrs["class"] = (base + " form-select").strip()
        else:
            widget.attrs["class"] = (base + " form-control").strip()

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "dni_cuit", "telefono", "email", "direccion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap(self)

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "cliente",
            "tipo_equipo",
            "marca_modelo",
            "problema_reportado",
            "observaciones_tecnicas",
            "solucion_implementada",
            "costo_total",
            "fecha_ingreso",
            "fecha_entrega",
            "estado_actual",
        ]
        labels = {
            "fecha_ingreso": "Fecha de ingreso",
            "fecha_entrega": "Fecha de entrega (opcional)",
        }
        help_texts = {
            "fecha_ingreso": "Se registra aunque el servicio todavía no esté entregado.",
            "fecha_entrega": "Puede dejarse vacía hasta que el equipo sea entregado.",
        }
        widgets = {
            "fecha_ingreso": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "step": "60"},
            ),
            "fecha_entrega": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "step": "60"},
            ),
            "problema_reportado": forms.Textarea(attrs={"rows": 3}),
            "observaciones_tecnicas": forms.Textarea(attrs={"rows": 3}),
            "solucion_implementada": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_ingreso"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["fecha_entrega"].input_formats = ["%Y-%m-%dT%H:%M"]

        if not self.is_bound and not self.instance.pk:
            self.initial["fecha_ingreso"] = timezone.localtime().replace(
                second=0,
                microsecond=0,
            )

        add_bootstrap(self)

    def clean(self):
        cleaned = super().clean()
        estado = cleaned.get("estado_actual")
        fecha_entrega = cleaned.get("fecha_entrega")

        # Si está Entregado y no pusiste fecha, la ponemos
        if estado == EstadoServicio.ENTREGADO and not fecha_entrega:
            cleaned["fecha_entrega"] = timezone.now()
        return cleaned

class HistorialEstadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEstado
        fields = ["estado", "observaciones"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_bootstrap(self)
