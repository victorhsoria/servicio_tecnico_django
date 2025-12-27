# Servicio Técnico (Django)

Este proyecto es el port a Django de tu app Flask de servicio técnico (clientes, servicios, historial de estados y reportes).

## Arranque rápido
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # en Windows (o cp en Linux)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Importar datos desde tu SQLite de Flask (opcional)
1. Copiá `servicio_tecnico.db` (el de Flask) al lado del proyecto o ajustá `FLASK_SQLITE_PATH` en `.env`.
2. Corré:
```bash
python manage.py import_flask_sqlite
```

## Apps
- `core`: modelos, CRUD, reportes, templates

> Nota: esto es un starter kit. Lo podés extender con auth, permisos, PDF, etc.
