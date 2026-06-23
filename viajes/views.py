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
    viaje = Viaje.objects.get(id=viaje_id)
    recibos = Recibo.objects.filter(viaje=viaje)
    total_gastado = sum(r.monto for r in recibos)

    hospedaje = sum(r.monto for r in recibos if r.tipo_gasto == 'hospedaje')
    alimentacion = sum(r.monto for r in recibos if r.tipo_gasto == 'alimentacion')

    porcentaje_hospedaje = round((hospedaje / total_gastado * 100), 1) if total_gastado > 0 else 0
    porcentaje_alimentacion = round((alimentacion / total_gastado * 100), 1) if total_gastado > 0 else 0

    return render(request, 'listadoRecibos.html', {
        'viaje': viaje,
        'recibos': recibos,
        'total_gastado': total_gastado,
        'porcentaje_hospedaje': porcentaje_hospedaje,
        'porcentaje_alimentacion': porcentaje_alimentacion,
    })


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
    recibo = Recibo.objects.get(id=id)
    return render(request, 'editarRecibo.html', {'recibo': recibo})


@login_required
def procesar_edicion_recibo(request):
    id = request.POST['id']
    recibo = Recibo.objects.get(id=id)
    recibo.concepto = request.POST['concepto']
    recibo.monto = request.POST['monto']
    recibo.fecha_emision = request.POST['fecha_emision']
    recibo.tipo_gasto = request.POST['tipo_gasto']

    nuevo_pdf = request.FILES.get('pdf')
    if nuevo_pdf:
        if recibo.pdf and os.path.isfile(recibo.pdf.path):
            os.remove(recibo.pdf.path)
        recibo.pdf = nuevo_pdf

    recibo.save()
    messages.success(request, 'Recibo actualizado correctamente.')
    return redirect('listado_recibos', viaje_id=recibo.viaje.id)


@login_required
def eliminar_recibo(request, id):
    recibo = Recibo.objects.get(id=id)
    viaje_id = recibo.viaje.id
    if recibo.pdf:
        if os.path.isfile(recibo.pdf.path):
            os.remove(recibo.pdf.path)
    recibo.delete()
    messages.success(request, 'Recibo eliminado correctamente.')
    return redirect('listado_recibos', viaje_id=viaje_id)


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


