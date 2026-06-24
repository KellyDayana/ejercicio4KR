from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio, name='inicio'),
    
    # Rutas de Viajes
    path('viajes/', views.viaje_lista, name='viaje_lista'),
    path('viajes/nuevo/', views.nuevo_viaje, name='nuevo_viaje'),
    path('viajes/guardar/', views.guardar_viaje, name='guardar_viaje'),
    path('viajes/editar/<int:id>/', views.editar_viaje, name='editar_viaje'),
    path('viajes/procesarEdicion/', views.procesar_edicion_viaje, name='procesar_edicion_viaje'),
    path('viajes/eliminar/<int:id>/', views.eliminar_viaje, name='eliminar_viaje'),
    path('viajes/aprobar/<int:id>/', views.aprobar_viaje, name='aprobar_viaje'),
    path('viajes/rechazar/<int:id>/', views.rechazar_viaje, name='rechazar_viaje'),
    
    # Rutas de Recibos asociados a un Viaje
    path('viajes/<int:viaje_id>/recibos/', views.listado_recibos, name='listado_recibos'),
    path('viajes/<int:viaje_id>/recibos/nuevo/', views.nuevo_recibo, name='nuevo_recibo'),
    path('viajes/<int:viaje_id>/recibos/guardar/', views.guardar_recibo, name='guardar_recibo'),
    
    # Rutas de CRUD de Recibos individuales
    path('recibos/editar/<int:id>/', views.editar_recibo, name='editar_recibo'),
    path('recibos/procesarEdicion/', views.procesar_edicion_recibo, name='procesar_edicion_recibo'),
    path('recibos/eliminar/<int:id>/', views.eliminar_recibo, name='eliminar_recibo'),
    
    # Reportes
    path('reporte/', views.reporte, name='reporte'),
    
    # Autenticación y Control de Usuarios
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
]