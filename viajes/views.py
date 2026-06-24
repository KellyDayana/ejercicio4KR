import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Viaje, Recibo
from django.contrib.auth.models import User

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
    if request.method == 'POST':
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
    viajes = Viaje.objects.all()
    datos_viajes = []

    total_global_hospedaje = 0
    total_global_alimentacion = 0
    total_global = 0

    PRESUPUESTO_BASE = 500  # presupuesto base por viaje en dólares

    for viaje in viajes:
        recibos = Recibo.objects.filter(viaje=viaje)
        total = sum(r.monto for r in recibos)
        hospedaje = sum(r.monto for r in recibos if r.tipo_gasto == 'hospedaje')
        alimentacion = sum(r.monto for r in recibos if r.tipo_gasto == 'alimentacion')

        total_global += total
        total_global_hospedaje += hospedaje
        total_global_alimentacion += alimentacion

        excede = total > PRESUPUESTO_BASE
        excedente = total - PRESUPUESTO_BASE if excede else 0

        datos_viajes.append({
            'viaje': viaje,
            'total': total,
            'excede_presupuesto': excede,
            'excedente': excedente,
            'presupuesto_base': PRESUPUESTO_BASE,
        })

    pct_hospedaje = round((total_global_hospedaje / total_global * 100), 1) if total_global > 0 else 0
    pct_alimentacion = round((total_global_alimentacion / total_global * 100), 1) if total_global > 0 else 0

    return render(request, 'reporte.html', {
        'datos_viajes': datos_viajes,
        'total_global': total_global,
        'pct_hospedaje': pct_hospedaje,
        'pct_alimentacion': pct_alimentacion,
        'total_global_hospedaje': total_global_hospedaje,
        'total_global_alimentacion': total_global_alimentacion,
        'presupuesto_base': PRESUPUESTO_BASE,
    })

@login_required
def editar_viaje(request, id):
    viaje = Viaje.objects.get(id=id)
    return render(request, 'editarViaje.html', {'viaje': viaje})

@login_required
def procesar_edicion_viaje(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def registro_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        clave_confirm = request.POST.get('password_confirm')
        
        if clave != clave_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
            
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'registro.html')
            
        # Crear el nuevo usuario de Django
        User.objects.create_user(username=usuario, email=correo, password=clave)
        messages.success(request, 'Cuenta creada con éxito. Ahora puedes iniciar sesión.')
        return redirect('login')
        
    return render(request, 'registro.html')