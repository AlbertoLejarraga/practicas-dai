//modo noche
$(document).ready(function() {
  //se pone en todos los label y select el texto oscuro(para que funcione después la búsqueda)
  $('label').each(function(){
    $(this).addClass("text-dark")
  })
  $('select').each(function(){
    $(this).addClass("text-dark")
  })
  //se comprueba si hubiera cookie de color para cambiarlo si fuera necesario
  var temaActual = readCookie("temaActual")
  if (temaActual){//si existe la cookie y ademas esta es noche, se cambian los colores, si es dia o no existe se deja tal cual
    if (temaActual=="noche"){
      cambiarColores()
    }
  }
  //cada vez que se haga click en el boton
  $('#botonNoche').click(function(){
    //se cambia la cookie del tema
    if ($('body').hasClass("bg-light")){
      document.cookie = "temaActual=noche"
    }else{
      document.cookie = "temaActual=dia"
    }
    //se cambian los colores
    cambiarColores()

  })
})
//de https://stackoverflow.com/a/1599291
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
//Función para cambiar los colores de la página entre noche y dia
function cambiarColores(){
  //se intercambian los colores del cuerpo
  $('body').toggleClass('bg-light bg-dark')
  $('body').toggleClass('text-light text-dark')
  //se intercambian los colores de los div si no pertenecen al footer
  $('div').each(function(){
    if(! ($('#footer').has($(this)).length)){
      $(this).toggleClass('bg-light bg-dark')
      $(this).toggleClass('text-light text-dark')
    }
  })
  //se intercambian los colores de los label y los selects
  $('label').toggleClass('text-light text-dark')
  $('select').toggleClass('text-light text-dark')
  //se cambian manualmente los colores y el fondo del input type text de búsqueda, nombre.
  if ($('#nombre').attr('style') && $('#nombre').attr('style').includes("#343A40"))//si tiene el fondo oscuro hay que ponerlo claro y el texto blanco
    $('#nombre').attr('style', "color: #343A41; background-color: #fff !important")
  else
    $('#nombre').attr('style', "color: #fff; background-color: #343A40 !important")
}



//llamadas a la api
$(document).ready(function() {
  nuevaBusqueda()
  $('#nombre').on("keyup", function(){
    nuevaBusqueda()
  })
  $('#tipo, #tipoHuevo, #evolucion').on("change", function(){
    nuevaBusqueda()
  })

})

function nuevaBusqueda(){
  //función que hace la llamada a ajax
  //se obtienen los filtros
  filtros = {
    'name': $('#nombre').val(),
    'type': $('#tipo').val(),
    'egg': $('#tipoHuevo').val(),
    'evolution': $('#evolucion').val()
  }
  $.ajax({
    url : "/api/pokemons",
    type : 'GET',
    data : filtros,
    dataType : 'json',
    success : function(json){
      montarContenido(json)

    },
    error : function(xhr, status){
      alert("error:" + xhr + status)
    }
  })
}

function montarContenido(json){
  if (jQuery.isEmptyObject(json)){
    $("#tablaContP8").html("No hay pokemons con estos filtros")
  }else{
    //tras montar el contenido se cambia el color si fuera necesario
    var temaActual = readCookie("temaActual")
    clasesTema = " bg-light text-dark "
    textoTema = ""
    if (temaActual){//si existe la cookie y ademas esta es noche, se cambian los colores, si es dia o no existe se deja tal cual
      if (temaActual=="noche"){
        clasesTema = " bg-dark text-light "
        textoTema = "text-light"
      }
    }
    stringHtml = ""
    $.each(json, function(i,pokemon){
      stringHtml +=
      `<div class="card ${clasesTema} mb-1 mr-1" style="width: 12rem;">
        <h5 class="card-title text-center">${pokemon.num}-${pokemon.name}</h5>
        <img class="card-img" src="${pokemon.img}" alt="${pokemon.name}">
        <div class="card-body ${clasesTema} ">
          <div class="collapse-content ${clasesTema} ">
            <p class="card-text collapse  text-left" id="contenido-${pokemon.num}">
              <b>Tipo:</b>`
      for (i in pokemon.type){
        stringHtml += pokemon.type[i]
        if (i !== pokemon.type.length - 1){
          stringHtml += ","
        }else{
          stringHtml += "."
        }
      }
              stringHtml += `<br>
              <b>Altura:</b> ${pokemon.height}<br>
              <b>Peso:</b> ${pokemon.weight}<br>
              <b>Huevo:</b> ${pokemon.egg}<br>
              <b>Probabilidad de aparición:</b> ${pokemon.spawn_chance}<br>
              <b>Hora de aparición:</b> ${pokemon.spawn_time}<br>
              <b>Debilidades: </b>`
      for (i in pokemon.weaknesses){
        stringHtml += pokemon.weaknesses[i]
        if (i != pokemon.weaknesses.length - 1){
          stringHtml += ", "
        }else{
          stringHtml += "."
        }
      }
      stringHtml+=`<br>
              <b>Evolución:</b> ${pokemon.evolucion}<br>`
      if (pokemon.prev_evolution){
        stringHtml += `<b>Evolucionado de: </b>`
        for (i in pokemon.prev_evolution){
          stringHtml += `<a href="#contenido-${pokemon.prev_evolution[i].num}" data-toggle="collapse">${pokemon.prev_evolution[i].name}</a>`
          if (i != pokemon.prev_evolution.length - 1){
            stringHtml += ", "
          }else{
            stringHtml += "."
          }
        }
        stringHtml+=`<br>`
      }

      if (pokemon.next_evolution){
        stringHtml += `<b>Evoluciona a: </b>`
        for (i in pokemon.next_evolution){
          stringHtml += `<a href="#contenido-${pokemon.next_evolution[i].num}" data-toggle="collapse">${pokemon.next_evolution[i].name}</a>`
          if (i != pokemon.next_evolution.length - 1){
            stringHtml += ", "
          }else{
            stringHtml += "."
          }
        }
      }
      stringHtml+=`<br>
            </p>
            <a class="btn  p-1 my-1 mr-0 mml-1 collapsed" data-toggle="collapse" href="#contenido-${pokemon.num}" aria-expanded="false" aria-controls="collapseContent"><i class="fas fa-info-circle"></i></a>
            <button type="button" class=" btn botonEliminar" data-id="${pokemon.id}" data-name="${pokemon.name}"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>`

    })
    $("#tablaContP8").html(stringHtml)
  }
  //se establece un onclick para el botón de eliminar
  $(".botonEliminar").on("click",function(e){
    if (confirm("Estás seguro de querer eliminar al pokemon " + $(this).data("name") + "?"))
      eliminarPokemon(parseInt($(this).data("id")))
  })
}
function eliminarPokemon(id){
  //función que hace la llamada a ajax
  $.ajax({
    url : "/api/pokemons/" + id,
    type : 'DELETE',
    dataType: "text",
    success : function(respuesta){
      nuevaBusqueda()
      alert(respuesta.toString())
    },
    error : function(xhr, status){
      alert(xhr.responseText);
    }
  })
}
