from django.shortcuts import render, HttpResponse
from mi_aplicacion.models import Autor, Libro, Usuario, Prestamo
from mi_aplicacion.forms import formAddLibro, formCrearAutor, formCrearUsuario, formPrestamo
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def index(request):
    return render(request,'base.html', {})

def biblioteca(request):
    context = {"var1": "variable número 1", "var2":"variable numero 2"}   # Aquí van la las variables para la plantilla
    return render(request,'base.html', context)
def libros(request):
    #se obtienen los libros almacenados
    libros = Libro.objects.all()
    context = {"libros":libros,
                "formAddLibro": formAddLibro}
    return render(request, 'libros.html', context)

def libroNuevo(request):
    if request.method == "POST":
        form = formAddLibro(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Libro insertado correctamente')
        else:
            messages.add_message(request, messages.WARNING, 'No se ha modificado. Algún dato es erróneo.')
    else:
        raise Http404
    return HttpResponseRedirect("/biblioteca/libros")

def eliminarLibro(request):
    if request.method == "POST":
        Libro.objects.filter(id=int(request.POST['id'])).delete()
        messages.add_message(request, messages.SUCCESS, 'Libro eliminado.')
        return HttpResponseRedirect("/biblioteca/libros")
    else:
        raise Http404
def modificarLibro(request, pk):
    libro = Libro.objects.get(pk=pk)
    form = formAddLibro(instance=libro)
    if request.method == "POST":
        form = formAddLibro(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Libro modificado correctamente')
        else:
            messages.add_message(request, messages.WARNING, 'No se ha modificado. Algún dato es erróneo.')

        return HttpResponseRedirect("/biblioteca/libros")
    else:

        context = {"formAddLibro": form}
        return render(request, 'modificarLibro.html', context)

def usuarios(request):
    if request.method == "POST":
        form = formCrearUsuario(request.POST)
        if form.is_valid():
            form.save()
    usuarios = Usuario.objects.all()
    context = {"usuarios":usuarios, "formCrearUsuario":formCrearUsuario}
    return render(request, 'usuarios.html', context)

def eliminarUsuario(request):
    if request.method == "POST":
        Usuario.objects.filter(id=int(request.POST['id'])).delete()
        return HttpResponseRedirect("/biblioteca/usuarios")
    else:
        raise Http404
def modificarUsuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)

    if request.method == "POST":
        form = formCrearUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Usuario modificado correctamente')
        else:
            messages.add_message(request, messages.WARNING, 'No se ha modificado. Algún dato es erróneo.')

        return HttpResponseRedirect("/biblioteca/usuarios")
    else:
        form = formCrearUsuario(instance=usuario)
        context = {"formModUsuario": form}
        return render(request, 'modificarUsuario.html', context)

def autores(request):
    if request.method == "POST":
        form = formCrearAutor(request.POST)
        if form.is_valid():
            form.save()
    autores = Autor.objects.all()
    context = {"autores":autores, "formCrearAutor":formCrearAutor}
    return render(request, 'autores.html', context)
def eliminarAutor(request):
    if request.method == "POST":
        Autor.objects.filter(id=int(request.POST['id'])).delete()
        messages.add_message(request, messages.SUCCESS, 'Autor eliminado')
        return HttpResponseRedirect("/biblioteca/autores")
    else:
        raise Http404

def prestamos(request):
    prestamos = Prestamo.objects.all().order_by('fecha')
    context = {"prestamos":prestamos}

    return render(request, 'prestamos.html', context)
def prestarLibro(request, pk):
    if request.method == "POST":
        form = formPrestamo(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.add_message(request, messages.ERROR,  str(form))
        messages.add_message(request, messages.SUCCESS, 'Libro prestado correctamente')
        return HttpResponseRedirect("/biblioteca/prestamos")
    else:
        libroAPrestar = Prestamo.objects.filter(libro_id=int(pk)).filter(estado="a")
        #si está vacio es que no está prestado
        if not libroAPrestar.exists():
            form = formPrestamo()
            form.setLibroInicial(pk)
            context = {"id":pk, "formPrestamo":form}
            return render(request, 'prestamoNuevo.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'El libro se encuentra prestado actualmente')
            return HttpResponseRedirect("/biblioteca/libros")
def cambiarEstadoPrestamo(request, pk, estadoActual):
    try:
        prestamo = Prestamo.objects.get(pk=pk)
        if estadoActual=="a":
            prestamo.estado = "f"
        elif estadoActual=="f":
            prestamo.estado = "a"
        prestamo.save()
        return HttpResponseRedirect("/biblioteca/prestamos")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, 'El préstamo ' + str(pk) + ' no existe')
        return HttpResponseRedirect("/biblioteca/prestamos")
def borrarPrestamo(request, pk):
    try:
        Prestamo.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Borrado correcto')
        return HttpResponseRedirect("/biblioteca/prestamos")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, 'El préstamo ' + str(pk) + ' no existe')
        return HttpResponseRedirect("/biblioteca/prestamos")
def modificarPrestamo(request, pk):
    prestamo = Prestamo.objects.get(pk=pk)

    if request.method == "POST":
        form = formPrestamo(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Préstamo modificado correctamente')
        else:
            messages.add_message(request, messages.WARNING, 'No se ha modificado. Algún dato es erróneo.')

        return HttpResponseRedirect("/biblioteca/prestamos")
    else:
        form = formPrestamo(instance=prestamo)
        context = {"formModPrestamo": form}
        return render(request, 'modificarPrestamo.html', context)
