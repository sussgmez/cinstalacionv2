from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import InstalacionForm, InstalacionUpdateForm, LoginForm
from .models import Tecnico, Instalacion
import csv, io

import datetime

# Create your views here.
@login_required
def redirect_agenda(request):
    return redirect('agenda')

@login_required
def agenda(request):
    context = {}
    context['today'] = datetime.datetime.now().strftime("%Y-%m-%d")
    if (request.method == "GET"):
        try:
            context['date'] = request.GET['date']
        except:
            context['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, "agenda/agenda.html", context)

@login_required
def tecnicos_json(request):
    json = serializers.serialize('json', Tecnico.objects.all())
    return HttpResponse(json)

@login_required
def instalaciones_json(request):
    json = serializers.serialize('json', Instalacion.objects.filter(status=0) | Instalacion.objects.filter(status=1))
    return HttpResponse(json)

@login_required
def guardar(request):
    if request.method == "POST":
        text = request.POST['datos-insts'].split(';')
        for line in text:
            datos = line.split('|')
            instalacion = Instalacion.objects.get(pk=datos[0])
            print(datos[4])
            if datos[4] == '0':
                instalacion.status = datos[4]
                instalacion.tecnico = None
                instalacion.fecha = None
                instalacion.hora = None
            elif datos[4] == '1':
                instalacion.status = datos[4]
                instalacion.tecnico = Tecnico.objects.get(pk = datos[1])
                fecha = datos[2].split('-')
                instalacion.fecha = datetime.datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]))
                instalacion.hora = datos[3] 

            elif datos[4] == '2':
                instalacion.status = datos[4]

            instalacion.save()
            
    return redirect('agenda')

@login_required
def create_instalacion(request):
    context = {}
    if request.method == "POST":
        form = InstalacionForm(request.POST)

        if form.is_valid():
            Instalacion.objects.create(
                pk= request.POST['nro_contrato'],
                nombre_cliente= request.POST['nombre_cliente'],
                direccion= request.POST['direccion'],
                numero_telefono1= request.POST['numero_telefono1'],
                numero_telefono2= request.POST['numero_telefono2'],
                plan= request.POST['plan'],
                prioridad= request.POST['prioridad'],
                tiempo_estimado= request.POST['tiempo_estimado'],
                observaciones= request.POST['observaciones']
            )
            return redirect('agenda')
    else:
        form = InstalacionForm()
    
    context['form'] = form
    return render(request, "agenda/create_instalacion.html", context=context)

@login_required
def update_instalacion(request, nro_contrato):
    context = {}
    if request.method == "POST":
        form = InstalacionUpdateForm(request.POST)

        if form.is_valid():
            instalacion = Instalacion.objects.get(pk = nro_contrato)
            
            instalacion.nombre_cliente = request.POST['nombre_cliente']
            instalacion.direccion = request.POST['direccion']
            instalacion.numero_telefono1 = request.POST['numero_telefono1']
            instalacion.numero_telefono2 = request.POST['numero_telefono2']
            instalacion.plan = request.POST['plan']
            instalacion.prioridad = int(request.POST['prioridad'])
            instalacion.tiempo_estimado = int(request.POST['tiempo_estimado'])
            instalacion.observaciones = request.POST['observaciones']

            instalacion.save()

            return redirect('agenda')
    else:
        instalacion = Instalacion.objects.get(pk=nro_contrato)
        form = InstalacionUpdateForm(instance=instalacion)
    
    context['form'] = form
    return render(request, "agenda/update_instalacion.html", context=context)

def login_view(request):
    form = LoginForm()
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('agenda')
        else:
            errors_msg = ['Nombre de usuario o Contraseña incorrecto']
            return render(request, 'login.html', context={'form':form, 'errors_msg':errors_msg})
    else:
        return render(request, 'login.html', context={'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required
def charge_csv(request):
    if request.method == "POST":
        content = io.StringIO(request.FILES['csv'].read().decode('utf-8'))
        reader = csv.reader(content)

        next(reader)

        for datos in reader:
            nombre_w_datos_extras = datos[1].split('-')

            nro_contrato = datos[0]
            nombre = nombre_w_datos_extras[0].casefold().title()
            
            numero_telefono1 = datos[5]
            if numero_telefono1 == "0":
                numero_telefono1 = None

            numero_telefono2 = datos[6]
            if numero_telefono2 == "0":
                numero_telefono2 = None
            
            direccion = datos[7].casefold().capitalize()
            plan = datos[8]

            if plan == "BASICO PLUS":
                plan = "BP"
            elif plan == "BASICO":
                plan = "BA"
            elif plan == "BRONCE":
                plan = "BR"
            elif plan == "PLATA":
                plan = "PL"
            elif plan == "ORO":
                plan = "OR"
            elif plan == "EMPRENDEDOR":
                plan = "EMP"
            elif plan == "PRODUCTIVO":
                plan = "PRD"
            elif plan == "PRODUCTIVO PRO":
                plan = "PRDP"
            elif plan == "VISIONARIO PRO":
                plan = "VISP"

            observaciones = ""
            try:
                observaciones = nombre_w_datos_extras[1]
            except:
                pass

            try:
                Instalacion.objects.get_or_create(
                    nro_contrato=nro_contrato,
                    nombre_cliente=nombre,
                    numero_telefono1=numero_telefono1,
                    numero_telefono2=numero_telefono2,
                    direccion=direccion,
                    plan=plan,
                    observaciones=observaciones
                )
            except:
                pass


    return redirect("agenda")