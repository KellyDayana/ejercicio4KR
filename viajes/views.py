from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Viaje, Recibo


def inicio(request):
    return render(request, 'inicio.html')


@login_required
def viaje_lista(request):
    return render(request, 'listadoViajes.html')


@login_required
def nuevo_viaje(request):
    return render(request, 'nuevoViaje.html')


@login_required
def guardar_viaje(request):
    destino = request.POST['destino']
    fecha_inicio = request.POST['fecha_inicio']
    fecha_fin = request.POST['fecha_fin']
    estado = request.POST['estado']
    departamento = request.POST['departamento']
    requiere_anticipo = 'requiere_anticipo' in request.POST
    foto = request.FILES.get('foto')

    Viaje.objects.create(
        destino=destino,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        departamento=departamento,
        requiere_anticipo=requiere_anticipo,
        foto=foto
    )
    messages.success(request, 'Viaje guardado correctamente.')
    return redirect('viaje_lista')


@login_required
def reporte(request):
    return render(request, 'reporte.html')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


