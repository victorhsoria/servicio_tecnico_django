import os
import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import Cliente, Servicio, HistorialEstado

def parse_dt(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        s = str(value)
        # SQLite suele guardar como 'YYYY-MM-DD HH:MM:SS' o ISO
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            # fallback común
            try:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt

class Command(BaseCommand):
    help = "Importa datos desde la SQLite de Flask (cliente/servicio/historial_estado)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=os.getenv("FLASK_SQLITE_PATH", ""),
            help="Ruta al archivo servicio_tecnico.db (Flask). También podés setear FLASK_SQLITE_PATH en .env",
        )

    def handle(self, *args, **options):
        path = options["path"]
        if not path:
            self.stderr.write(self.style.ERROR("No se encontró la ruta. Usá --path o setea FLASK_SQLITE_PATH en .env"))
            return

        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"No existe el archivo: {path}"))
            return

        self.stdout.write(self.style.WARNING(f"Importando desde: {path}"))

        con = sqlite3.connect(path)
        con.row_factory = sqlite3.Row

        with transaction.atomic():
            # Clientes
            rows = con.execute("SELECT * FROM cliente ORDER BY id").fetchall()
            self.stdout.write(f"Clientes: {len(rows)}")
            for r in rows:
                Cliente.objects.update_or_create(
                    id=r["id"],
                    defaults=dict(
                        nombre=r["nombre"],
                        apellido=r["apellido"],
                        dni_cuit=r["dni_cuit"],
                        telefono=r["telefono"],
                        email=r["email"],
                        direccion=r["direccion"],
                    ),
                )

            # Servicios
            rows = con.execute("SELECT * FROM servicio ORDER BY id").fetchall()
            self.stdout.write(f"Servicios: {len(rows)}")
            for r in rows:
                Servicio.objects.update_or_create(
                    id=r["id"],
                    defaults=dict(
                        cliente_id=r["cliente_id"],
                        tipo_equipo=r["tipo_equipo"],
                        marca_modelo=r["marca_modelo"],
                        problema_reportado=r["problema_reportado"],
                        observaciones_tecnicas=r["observaciones_tecnicas"],
                        solucion_implementada=r["solucion_implementada"],
                        costo_total=r["costo_total"] if r["costo_total"] is not None else 0,
                        fecha_ingreso=parse_dt(r["fecha_ingreso"]) or timezone.now(),
                        fecha_entrega=parse_dt(r["fecha_entrega"]),
                        estado_actual=r["estado_actual"],
                    ),
                )

            # Historial
            rows = con.execute("SELECT * FROM historial_estado ORDER BY id").fetchall()
            self.stdout.write(f"Historial: {len(rows)}")
            for r in rows:
                HistorialEstado.objects.update_or_create(
                    id=r["id"],
                    defaults=dict(
                        servicio_id=r["servicio_id"],
                        estado=r["estado"],
                        fecha_cambio=parse_dt(r["fecha_cambio"]) or timezone.now(),
                        observaciones=r["observaciones"],
                    ),
                )

        self.stdout.write(self.style.SUCCESS("Importación lista ✅"))
