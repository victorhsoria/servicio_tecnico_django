# Servicio Técnico (Django)

App web para gestionar un servicio técnico: **clientes, servicios/órdenes, historial de estados, comprobantes imprimibles y reportes con exportación a Excel/PDF**.  
Hecho con **Django + Bootstrap**, simple, rápido y bien usable.

---

## ✨ Qué incluye

- ✅ CRUD de **Clientes**
- ✅ CRUD de **Servicios** (órdenes de trabajo)
- ✅ **Historial de estados** por servicio
- ✅ Listados con **búsqueda y filtros**
- ✅ **Comprobante / Orden de trabajo** imprimible (con checkboxes tildables antes de imprimir)
- ✅ **Reportes** con filtros (fecha + estado)
- ✅ Exportación desde Reportes:
  - 📄 PDF
  - 📊 Excel

---

## 🧱 Tech stack

- Django (v6.x)
- SQLite (dev)
- Bootstrap 5 + Bootstrap Icons
- reportlab (PDF)
- openpyxl (Excel)
- python-dotenv (variables de entorno)

---

## 🚀 Instalación (Windows)

Cloná el repo y creá un entorno virtual:

```bat
git clone https://github.com/victorhsoria/servicio_tecnico_django.git
cd servicio_tecnico_django

python -m venv env
env\Scripts\activate
