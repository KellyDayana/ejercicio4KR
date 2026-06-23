from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def inicio(request):
    return render(request, 'inicio.html')


@login_required
def viaje_lista(request):
    return render(request, 'listadoViajes.html')


@login_required
def viaje_crear(request):
    return render(request, 'nuevoViaje.html')


@login_required
def reporte(request):
    return render(request, 'reporte.html')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

