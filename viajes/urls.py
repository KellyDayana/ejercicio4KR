from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('viajes/', views.viaje_lista, name='viaje_lista'),
    path('viajes/nuevo/', views.nuevo_viaje, name='nuevo_viaje'),
    path('viajes/guardar/', views.guardar_viaje, name='guardar_viaje'),
    path('reporte/', views.reporte, name='reporte'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

