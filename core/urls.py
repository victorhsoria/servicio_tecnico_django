from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    path("clientes/", views.ClienteListView.as_view(), name="clientes_list"),
    path("clientes/nuevo/", views.ClienteCreateView.as_view(), name="clientes_nuevo"),
    path("clientes/<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="clientes_editar"),
    path("clientes/<int:pk>/eliminar/", views.ClienteDeleteView.as_view(), name="clientes_eliminar"),

    path("servicios/", views.ServicioListView.as_view(), name="servicios_list"),
    path("servicios/nuevo/", views.ServicioCreateView.as_view(), name="servicios_nuevo"),
    path("servicios/<int:pk>/", views.ServicioDetailView.as_view(), name="servicio_detalle"),
    path("servicios/<int:pk>/editar/", views.ServicioUpdateView.as_view(), name="servicios_editar"),
    path("servicios/<int:pk>/eliminar/", views.ServicioDeleteView.as_view(), name="servicios_eliminar"),
    path("servicios/<int:pk>/imprimir/", views.ServicioPrintView.as_view(), name="servicio_imprimir"),

    path("reportes/", views.ReportesView.as_view(), name="reportes"),
    path("reportes/", views.ReportesView.as_view(), name="reportes"),
    path("reportes/export/excel/", views.reportes_export_excel, name="reportes_excel"),
    path("reportes/export/pdf/", views.reportes_export_pdf, name="reportes_pdf"),
    path("servicios/<int:pk>/comprobante/", views.ServicioComprobanteView.as_view(), name="servicio_comprobante"),

]
