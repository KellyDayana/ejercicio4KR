import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Viaje, Recibo


def inicio(request):
    return render(request, 'inicio.html')


@login_required
def viaje_lista(request):
    viajes = Viaje.objects.all()
    return render(request, 'listadoViajes.html', {'viajes': viajes})


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


@login_required
def editar_viaje(request, id):
    viaje = Viaje.objects.get(id=id)
    return render(request, 'editarViaje.html', {'viaje': viaje})


@login_required
def procesar_edicion_viaje(request):
    id = request.POST['id']
    viaje = Viaje.objects.get(id=id)
    viaje.destino = request.POST['destino']
    viaje.fecha_inicio = request.POST['fecha_inicio']
    viaje.fecha_fin = request.POST['fecha_fin']
    viaje.estado = request.POST['estado']
    viaje.departamento = request.POST['departamento']
    viaje.requiere_anticipo = 'requiere_anticipo' in request.POST

    nueva_foto = request.FILES.get('foto')
    if nueva_foto:
        if viaje.foto and os.path.isfile(viaje.foto.path):
            os.remove(viaje.foto.path)
        viaje.foto = nueva_foto

    viaje.save()
    messages.success(request, 'Viaje actualizado correctamente.')
    return redirect('viaje_lista')


@login_required
def eliminar_viaje(request, id):
    viaje = Viaje.objects.get(id=id)
    if viaje.foto:
        if os.path.isfile(viaje.foto.path):
            os.remove(viaje.foto.path)
    viaje.delete()
    messages.success(request, 'Viaje eliminado correctamente.')
    return redirect('viaje_lista')


@login_required
def listado_recibos(request, viaje_id):
    return render(request, 'listadoRecibos.html')


@login_required
def nuevo_recibo(request, viaje_id):
    viaje = Viaje.objects.get(id=viaje_id)
    return render(request, 'nuevoRecibo.html', {'viaje': viaje})


@login_required
def guardar_recibo(request, viaje_id):
    viaje = Viaje.objects.get(id=viaje_id)
    concepto = request.POST['concepto']
    monto = request.POST['monto']
    fecha_emision = request.POST['fecha_emision']
    tipo_gasto = request.POST['tipo_gasto']
    pdf = request.FILES.get('pdf')

    Recibo.objects.create(
        viaje=viaje,
        concepto=concepto,
        monto=monto,
        fecha_emision=fecha_emision,
        tipo_gasto=tipo_gasto,
        pdf=pdf
    )
    messages.success(request, 'Recibo guardado correctamente.')
    return redirect('listado_recibos', viaje_id=viaje_id)


@login_required
def editar_recibo(request, id):
    return render(request, 'editarRecibo.html')


@login_required
def procesar_edicion_recibo(request):
    return redirect('viaje_lista')


@login_required
def eliminar_recibo(request, id):
    return redirect('viaje_lista')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


