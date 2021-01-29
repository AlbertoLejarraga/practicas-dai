# Práctica 10

Esta práctica es una práctica libre basada en Javascript.

Se desarrollan dos aspectos:

* Análisis descriptivo de los datos
Se generan una serie de gráficos con la librería [ChartJS](https://www.chartjs.org/) sobre los distintos pokemons de la base de datos.
Los ficheros afectados, principalmente, son:
    * [Fichero .js donde se general los gráficos](https://github.com/AlbertoLejarraga/practicas-dai/tree/main/practica/app/static/js/practica10.js)
    * [Fichero html base](https://github.com/AlbertoLejarraga/practicas-dai/tree/main/practica/app/templates/practica10.html)

* Notificaciones de salida de un pokemon
Según la base de datos utilizada, cada pokemon sale a una hora determinada. Se desarrolla un sistema de notificaciones a la hora en la que un pokemon sale y se le puede cazar. Esto solo funciona en navegadores basados en Chromium. Los ficheros son:
    * [ServiceWorker](https://github.com/AlbertoLejarraga/practicas-dai/tree/main/practica/app/static/js/service-worker.js)
    * [Gestor de notificaciones](https://github.com/AlbertoLejarraga/practicas-dai/tree/main/practica/app/static/js/notificaciones.js)
    * [Fichero de la práctica 4](https://github.com/AlbertoLejarraga/practicas-dai/tree/main/practica/app/templates/practica4.html) sobre el que se añade un símbolo para activar las notificaciones. En la página debe haber un solo pokemon,utilizando para ello los filtros adecuados.
