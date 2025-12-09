from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumnos, ComentarioContacto
from .forms import ComentarioContactoForm
import datetime
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages

def registros(request):
    alumnos = Alumnos.objects.all()
    return render(request, "registros/principal.html", {'alumnos': alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultarComentario')
    form = ComentarioContactoForm()
    return render(request,'registros/contacto.html',{'form': form})

def contacto(request):
    return render(request,"registros/contacto.html")

def consultarComentario(request):
    comentarios = ComentarioContacto.objects.all()
    # CORREGIDO: El nombre ahora coincide con tu archivo en la carpeta (consultarContacto.html)
    return render(request, "registros/consultarContacto.html", {'comentarios': comentarios})

def eliminarComentarioContacto(request, id, confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('consultarComentario')
    return render(request, confirmacion, {'object':comentario})

def consultarComentarioIndividual(request, id):
    # Usamos get_object_or_404 para mayor seguridad
    comentario = get_object_or_404(ComentarioContacto, id=id)
    return render(request, "registros/formEditarComentario.html", {'comentario':comentario})

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    
    if form.is_valid():
        form.save()
        return redirect('consultarContacto')
        
    return render(request, "registros/formEditarComentario.html", {'comentario': comentario, 'form': form})

def consultar1(request):
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera",
    "turno", "imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})
def consultar6(request):
    fechaInicio = datetime.date(2022, 7, 1)
    fechaFin = datetime.date(2022, 7, 13)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion,
            archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})