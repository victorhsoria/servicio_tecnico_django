from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Cliente, EstadoServicio, Servicio, ServicioImagen


class PanelServicioTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.cliente = Cliente.objects.create(nombre="Ana", apellido="Prueba")
        self.servicio = Servicio.objects.create(
            cliente=self.cliente, tipo_equipo="Notebook", problema_reportado="No enciende",
            fecha_ingreso=timezone.now() - timedelta(days=10),
        )

    def test_panel_orders_open_services_by_age(self):
        reciente = Servicio.objects.create(
            cliente=self.cliente, tipo_equipo="PC", problema_reportado="Reinicio",
        )
        Servicio.objects.create(
            cliente=self.cliente, tipo_equipo="Entregado", problema_reportado="Resuelto",
            estado_actual=EstadoServicio.ENTREGADO,
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_activos"], 2)
        self.assertEqual(list(response.context["servicios_antiguos"]), [self.servicio, reciente])

    def test_upload_and_display_without_media_mapping(self):
        contenido = BytesIO()
        Image.new("RGB", (20, 20), "green").save(contenido, "PNG")
        response = self.client.post(reverse("servicio_imagen_subir", args=[self.servicio.pk]), {
            "imagenes": SimpleUploadedFile("equipo.png", contenido.getvalue(), content_type="image/png"),
            "descripcion": "Equipo reparado",
        })
        self.assertEqual(response.status_code, 302)
        imagen = ServicioImagen.objects.get(servicio=self.servicio)
        url = reverse("servicio_imagen_ver", args=[self.servicio.pk, imagen.pk])
        with override_settings(DEBUG=False):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "image/png")
            self.assertEqual(b"".join(response.streaming_content), contenido.getvalue())
            response.close()
        self.assertContains(self.client.get(reverse("servicio_detalle", args=[self.servicio.pk])), url)

    def test_invalid_upload_shows_errors_without_creating_record(self):
        response = self.client.post(reverse("servicio_imagen_subir", args=[self.servicio.pk]), {
            "imagenes": SimpleUploadedFile("equipo.png", b"invalid", content_type="image/png"),
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context["imagen_form"].errors)
        self.assertTrue(response.context["mostrar_fotos"])
        self.assertFalse(ServicioImagen.objects.exists())

    def test_missing_file_and_wrong_service_return_404(self):
        imagen = ServicioImagen.objects.create(servicio=self.servicio, imagen="servicios/inexistente.png")
        response = self.client.get(reverse("servicio_imagen_ver", args=[self.servicio.pk, imagen.pk]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("servicio_imagen_ver", args=[self.servicio.pk + 1, imagen.pk]))
        self.assertEqual(response.status_code, 404)
