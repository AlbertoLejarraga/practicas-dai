from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('biblioteca', views.biblioteca, name='biblioteca'),
  path('biblioteca/libros', views.libros, name='libros'),
  path('biblioteca/libros/nuevo', views.libroNuevo, name='libroNuevo'),
  path('biblioteca/libros/eliminar', views.eliminarLibro, name='eliminarLibro'),
  path('biblioteca/libros/modificar/<int:pk>', views.modificarLibro, name='modificarLibro'),
  path('biblioteca/prestamos', views.prestamos, name='prestamos'),
  path('biblioteca/prestamos/nuevo/<int:pk>', views.prestarLibro, name='prestarLibro'),
  path('biblioteca/prestamos/cambiarEstado/<int:pk>/<str:estadoActual>', views.cambiarEstadoPrestamo, name='cambiarEstadoPrestamo'),
  path('biblioteca/prestamos/borrar/<int:pk>', views.borrarPrestamo, name='borrarPrestamo'),
  path('biblioteca/prestamos/modificar/<int:pk>', views.modificarPrestamo, name='modificarPrestamo'),
  path('biblioteca/usuarios', views.usuarios, name='usuarios'),
  path('biblioteca/usuarios/eliminar', views.eliminarUsuario, name='eliminarUsuario'),
  path('biblioteca/usuarios/modificar/<int:pk>', views.modificarUsuario, name='modificarUsuario'),
  path('biblioteca/autores', views.autores, name='autores'),
  path('biblioteca/autores/eliminar', views.eliminarAutor, name='eliminarAutor'),
]
