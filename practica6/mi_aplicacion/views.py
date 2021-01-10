from django.shortcuts import render, HttpResponse
from mi_aplicacion.models import Autor, Libro, Usuario, Prestamo
from mi_aplicacion.forms import formAddLibro, formCrearAutor, formCrearUsuario, formPrestamo
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
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

@permission_required('mi_aplicacion.modificar_libros')
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

@permission_required('mi_aplicacion.modificar_libros')
def eliminarLibro(request):
    if request.method == "POST":
        Libro.objects.filter(id=int(request.POST['id'])).delete()
        messages.add_message(request, messages.SUCCESS, 'Libro eliminado.')
        return HttpResponseRedirect("/biblioteca/libros")
    else:
        raise Http404

@permission_required('mi_aplicacion.modificar_libros')
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

@permission_required('mi_aplicacion.modificar_usuarios')
def usuarios(request):
    if request.method == "POST":
        form = formCrearUsuario(request.POST)
        if form.is_valid():
            form.save()
            #se inserta en la tabla usuarios de django
            user = User.objects.create_user(request.POST["dni"], request.POST["email"], request.POST["dni"]+"A")
            user.first_name = request.POST["nombre"]
            user.last_name = request.POST["apellidos"]
            user.save()
            if request.POST["tipo"] == "s":
                grupo = Group.objects.get(name="STAFF")
            else:
                grupo = Group.objects.get(name="CLIENTE")
            grupo.user_set.add(user)

    usuarios = Usuario.objects.all()
    context = {"usuarios":usuarios, "formCrearUsuario":formCrearUsuario}
    return render(request, 'usuarios.html', context)

@permission_required('mi_aplicacion.modificar_usuarios')
def eliminarUsuario(request):
    if request.method == "POST":
        usuarioBorrar = Usuario.objects.get(id=int(request.POST['id']))
        usuarioDjango = User.objects.get(username=usuarioBorrar.dni)
        usuarioDjango.delete()
        usuarioBorrar.delete()
        return HttpResponseRedirect("/biblioteca/usuarios")
    else:
        raise Http404

@permission_required('mi_aplicacion.modificar_usuarios')
def modificarUsuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)

    if request.method == "POST":
        form = formCrearUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            #se modifica el grupo si fuera necesario
            user = User.objects.get(username=request.POST['dni'])
            grupoStaff = Group.objects.get(name="STAFF")
            grupoCliente = Group.objects.get(name="CLIENTE")
            user.groups.remove(grupoStaff)
            user.groups.remove(grupoCliente)
            if request.POST["tipo"] == "s":
                grupoStaff.user_set.add(user)
            else:
                grupoCliente.user_set.add(user)


            messages.add_message(request, messages.SUCCESS, 'Usuario modificado correctamente')
        else:
            messages.add_message(request, messages.WARNING, 'No se ha modificado. Algún dato es erróneo.')

        return HttpResponseRedirect("/biblioteca/usuarios")
    else:
        form = formCrearUsuario(instance=usuario)
        form.dniReadonly()
        context = {"formModUsuario": form}
        return render(request, 'modificarUsuario.html', context)

@permission_required('mi_aplicacion.modificar_autor')
def autores(request):
    if request.method == "POST":
        form = formCrearAutor(request.POST)
        if form.is_valid():
            form.save()
    autores = Autor.objects.all()
    context = {"autores":autores, "formCrearAutor":formCrearAutor}
    return render(request, 'autores.html', context)

@permission_required('mi_aplicacion.modificar_autor')
def eliminarAutor(request):
    if request.method == "POST":
        Autor.objects.filter(id=int(request.POST['id'])).delete()
        messages.add_message(request, messages.SUCCESS, 'Autor eliminado')
        return HttpResponseRedirect("/biblioteca/autores")
    else:
        raise Http404

@permission_required('mi_aplicacion.modificar_prestamo')
def prestamos(request):
    prestamos = Prestamo.objects.all().order_by('fecha')
    context = {"prestamos":prestamos}

    return render(request, 'prestamos.html', context)

@login_required
def prestarLibro(request, pk):
    if request.method == "POST":
        libroAPrestar = Prestamo.objects.filter(libro_id=int(request.POST["libro"])).filter(estado="a")
        #si está vacio es que no está prestado
        if not libroAPrestar.exists():


            if not request.user.has_perm('mi_aplicacion.modificar_prestamo'):
                usuarioLogado = Usuario.objects.get(dni=User.objects.get(username=request.user.username)).id
                post_values = request.POST.copy()
                post_values["usuario"] = usuarioLogado
                form = formPrestamo(post_values)
            else:
                form = formPrestamo(request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.add_message(request, messages.ERROR,  str(form))
            messages.add_message(request, messages.SUCCESS, 'Libro prestado correctamente')
            return HttpResponseRedirect("/biblioteca/libros")
        else:
            messages.add_message(request, messages.WARNING, 'El libro se encuentra prestado actualmente')
            return HttpResponseRedirect("/biblioteca/libros")
    else:
        libroAPrestar = Prestamo.objects.filter(libro_id=int(pk)).filter(estado="a")
        #si está vacio es que no está prestado
        if not libroAPrestar.exists():
            form = formPrestamo()
            form.setLibroInicial(pk)
            if not request.user.has_perm('mi_aplicacion.modificar_prestamo'):
                #si el usuario no es staff no debe poder modificar el usuario, debe aparecer el suyo
                form.paraClientes()
            context = {"id":pk, "formPrestamo":form}
            return render(request, 'prestamoNuevo.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'El libro se encuentra prestado actualmente')
            return HttpResponseRedirect("/biblioteca/libros")

@permission_required('mi_aplicacion.modificar_prestamo')
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

@permission_required('mi_aplicacion.modificar_prestamo')
def borrarPrestamo(request, pk):
    try:
        Prestamo.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Borrado correcto')
        return HttpResponseRedirect("/biblioteca/prestamos")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, 'El préstamo ' + str(pk) + ' no existe')
        return HttpResponseRedirect("/biblioteca/prestamos")

@permission_required('mi_aplicacion.modificar_prestamo')
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
