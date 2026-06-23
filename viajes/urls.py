from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('viajes/', views.viaje_lista, name='viaje_lista'),
    path('viajes/crear/', views.viaje_crear, name='viaje_crear'),
    path('reporte/', views.reporte, name='reporte'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
