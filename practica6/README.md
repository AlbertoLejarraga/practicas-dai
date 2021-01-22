# Práctica 6 de la asignatura
Se desarrolla una aplicación web sobre una biblioteca, permitiendo la gestión básica de usuarios, autores, libros y préstamos.
Se utiliza el framework web django, PostgreSQL para la base de datos y como framework css Bootstrap

# Práctica 7 de la asignatura
En esta práctica se añade la posibilidad de realizar login para llevar a cabo los préstamos de libros y otras funciones en función del tipo de usuario, ya sea miembro de administración o un cliente de la librería, utilizando para ello la librería de autenticación nativa de Django.

# Práctica 9 de la asignatura
En esta práctica se despliega la aplicación en un servidor de "producción" utilizando como tal nginx.

### Primer inicio de sesión
 * Un miembro del staff (o root) da de alta a un usuario con sus datos y una password genérica
 * El usuario intenta iniciar sesión y pulsa en recordar contraseña.
 * Recibe un correo con un link (sale en la terminal) e introduce la nueva contraseña y se loguea.

### Usuarios actuales
  * 00000000C - Customer_PWD1 - usuarioCliente@gmail.com
  * 1111111s - Staff_PWD1 - usuarioStaff@gmail.com

### Permisos de los usuarios
  * Los usuarios del grupo clientes pueden consultar los libros y prestárselos a ellos mismos, si están disponibles, y siempre por 30 días desde la fecha actual.
  * Los usuarios del grupo staff pueden llevar a cabo cualquier acción en el sitio
