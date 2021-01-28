//llamadas a la api
var graficoAMostrar = ""
$(document).ready(function() {
  nuevaBusqueda()
  $('#nombre').on("keyup", function(){
    nuevaBusqueda()
  })
  $('#listaPoks').on("change", function(){
    pokemonAnadido()
  })
  $("#botonTodos").on("click", function(){
    seleccionarTodosPok()
  })
  $("#botonNinguno").on("click", function(){
    quitarTodaSeleccion()
  })
  comprobarEstiloListado()
  $("#linkTipo, #linkPeso, #linkAltura, #linkTipoHuevo").on("click", function(){
    graficoAMostrar = $(this).prop("id")
    actualizarGrafico()
  })

})
var ultimoJSONPok = null
function nuevaBusqueda(){
  //función que hace la llamada a ajax para devovler los pokemons
  $.ajax({
    url : "/api/pokemons",
    type : 'GET',
    data : {'name': $('#nombre').val()},
    dataType : 'json',
    success : function(json){
      ultimoJSONPok = json
      montarSelect(json)
    },
    error : function(xhr, status){
      alert("error:" + xhr + status)
    }
  })
}
function montarSelect(json){
  //Función que monta el selector de pokemons
  //por cada pokemon un option
  stringHtml = ""
  $.each(json, function(i,pokemon){
    stringHtml += `<option value="${pokemon.num}-${pokemon.name}" id="${pokemon.id}">${pokemon.num}-${pokemon.name}</option>`
  })
  $("#listaPoks").html(stringHtml)
}
var listaPokAnadidos = []
var listaIdAnadidos = []
function pokemonAnadido(){
  //función que modifica la lista de pokemons añadidos
  pokAnadido = $("#listaPoks").find(":selected").text()
  idPok = $("#listaPoks").find(":selected").attr("id")
  indiceLista = listaIdAnadidos.indexOf(String(idPok))
  if (indiceLista == -1){
    listaPokAnadidos.push(pokAnadido)
    listaIdAnadidos.push(String(idPok))
    html = `<li id="listaAnadidos${idPok}">${pokAnadido}<button type="button" class="btn" id="btn${idPok}" data-id="${idPok}"><i class="fas fa-times"></i></button></li>`
    $("#pokSeleccionados").append(html)
    $(`#btn${idPok}`).on("click", function(e){
      idBorrar = $(this).data("id")
      $(`#listaAnadidos${idBorrar}`).remove()
      indiceBorrar = listaIdAnadidos.indexOf(String(idPok))
      listaPokAnadidos.splice(indiceBorrar,1)
      listaIdAnadidos.splice(indiceBorrar,1)
    })
  }
  comprobarEstiloListado()
  actualizarGrafico()
}
function seleccionarTodosPok(){
  listaPokAnadidos = []
  listaIdAnadidos = []
  $.each(ultimoJSONPok, function(i, pokemon){
    listaPokAnadidos.push(`${pokemon.num}-${pokemon.name}`)
    listaIdAnadidos.push(String(pokemon.id))
  })
  html = ""
  for (i=0;i<listaIdAnadidos.length;i++){
    html += `<li id="listaAnadidos${listaIdAnadidos[i]}">${listaPokAnadidos[i]}<button type="button" id="btn${listaIdAnadidos[i]}" class="btn" data-id="${listaIdAnadidos[i]}" onclick="quitarPokemon(${listaIdAnadidos[i]})"><i class="fas fa-times"></i></button></li>`
  }
  $("#pokSeleccionados").html(html)
  comprobarEstiloListado()
  actualizarGrafico()
}
function quitarPokemon(idBorrar){
    $(`#listaAnadidos${idBorrar}`).remove()
    indiceBorrar = listaIdAnadidos.indexOf(String(idBorrar))
    listaPokAnadidos.splice(indiceBorrar,1)
    listaIdAnadidos.splice(indiceBorrar,1)
    comprobarEstiloListado()
    actualizarGrafico()
}
function quitarTodaSeleccion(){
  listaPokAnadidos = []
  listaIdAnadidos = []
  $("#pokSeleccionados").html("")
  comprobarEstiloListado()
  actualizarGrafico()
}
function comprobarEstiloListado(){
  //Función para tachar uno u otro gráfico en función del número de pokemons seleccionados
  if (listaIdAnadidos.length <=8){
    $("#linkTipo").css({"text-decoration": "none"});
    $("#linkTipoHuevo").css({"text-decoration": "line-through"});

  }else{
    $("#linkTipo").css({"text-decoration": "line-through"});
    $("#linkTipoHuevo").css({"text-decoration": "none"});

  }
}
var datosSeleccionados = []
var myChart = null;
var colores = ["#FF0000", "#00FF00", "#0000FF", "#FBFF00", "#00FFF7", "FF00E8", "D35400", "4B4B4B"]
function actualizarGrafico(){
  //función que llama a la correspondiente para actualizar el gráfico según la selección
  //primero se actualiza la variable de datos seleccionados
  datosSeleccionados = []
  $.each(ultimoJSONPok, function(i, pokemon){
    if(listaIdAnadidos.indexOf(String(pokemon.id)) !== -1){
      datosSeleccionados.push(pokemon)
    }
  })
  switch (graficoAMostrar){
    case "linkTipo": graficoTipo();break;
    case "linkPeso": graficoPeso();break;
    case "linkAltura": graficoAltura();break;
    case "linkTipoHuevo": graficoTipoHuevo();break;
  }
    if (myChart != null) myChart.destroy()
}
function obtenerDatosTipo(){
  //función que recorre el ultimo json y obtiene los datos necesarios
  labels = []
  datasets = []
  $.each(datosSeleccionados, function(i, pokemon){
    //primero se obtienen las labels(si no están en la lista se introducen)
    $.each(pokemon.type, function(i, type){
      if (labels.indexOf(type) == -1){
        labels.push(type)
      }
    })
    $.each(pokemon.weaknesses, function(i, weakness){
      if (labels.indexOf(weakness)==-1){
        labels.push(weakness)
      }
    })
  })
  $.each(datosSeleccionados, function(i, pokemon){
    //ahora se generan los datasets
    dataset = {label:pokemon.name, borderWidth:1, data:[], borderColor: colores[i], backgroundColor: colores[i]+"20", pointBackgroundColor:colores[i]}
    $.each(labels, function(i,label){
      //para las etiquetas detectadas, se da 1 si el pokemon es fuerte en eso, 0.5 si ni fuerte ni debil y 0 si debil
      if(pokemon.type.indexOf(label) != -1){
        dataset.data.push(1)
      }else if (pokemon.weaknesses.indexOf(label) != -1){
        dataset.data.push(0)
      }else{
        dataset.data.push(0.5)
      }
    })
    datasets.push(dataset)
  })
  return {labels:labels, datasets:datasets}
}
function graficoTipo(){
  //Seobtienen los datos de tipo
  datos = obtenerDatosTipo()
  $("#canvas").remove()
  $("#divCanvas").append('<canvas id="canvas" width="400" height="300" style="width: 100%; height:30rem">')
  var ctx = document.getElementById('canvas');
  var myChart = new Chart(ctx, {
      type: 'radar',
      data: {
          labels: datos.labels,
          datasets: datos.datasets,
      },
      options: {
        scale: {
          angleLines: {
              display: false
          },
          ticks: {
            beginAtZero: true
          }
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    return  data.datasets[tooltipItem.datasetIndex].label + "-" + data.labels[tooltipItem.index];
                }
            }
        }
      }
  });

}
function obtenerDatosPeso(){
  //función que recorre el ultimo json y obtiene los datos necesarios
  labels = []
  datasets = []
  $.each(datosSeleccionados, function(i, pokemon){
    //primero se obtienen las labels(si no están en la lista se introducen)
      if (labels.indexOf(pokemon.name) == -1){
        labels.push(pokemon.name)
      }
  })
  datasets.push({label:"Peso(kg)", backgroundColor:colores[1]+"20", borderColor:colores[1], borderWidth:1, data:[]})
  $.each(datosSeleccionados, function(i, pokemon){
    //ahora los datasets
    datasets[0].data.push(pokemon.weight.split(" ")[0])
  })
  return {labels:labels, datasets:datasets}
}
function graficoPeso(){
  //Se obtienen los datos de peso
  datos = obtenerDatosPeso()
  $("#canvas").remove()
  $("#divCanvas").append('<canvas id="canvas" width="400" height="300" style="width: 100%; height:30rem">')
  var ctx = document.getElementById('canvas');
  var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: datos.labels,
          datasets: datos.datasets,
      },
      options: {
        scales: {
            xAxes: [{
                gridLines: {
                    offsetGridLines: true
                },
                ticks: {
                  beginAtZero: true
                }
            }]
        }
      }
  });
}
function obtenerDatosAltura(){
  //función que recorre el ultimo json y obtiene los datos necesarios
  labels = []
  datasets = []
  $.each(datosSeleccionados, function(i, pokemon){
    //primero se obtienen las labels(si no están en la lista se introducen)
      if (labels.indexOf(pokemon.name) == -1){
        labels.push(pokemon.name)
      }
  })
  datasets.push({label:"Altura(m)", backgroundColor:colores[0]+"20", borderColor:colores[0], borderWidth:1, data:[]})
  $.each(datosSeleccionados, function(i, pokemon){
    //ahora los datasets
    datasets[0].data.push(pokemon.height.split(" ")[0])
  })
  return {labels:labels, datasets:datasets}
}
function graficoAltura(){
  //Se obtienen los datos de peso
  datos = obtenerDatosAltura()
  $("#canvas").remove()
  $("#divCanvas").append('<canvas id="canvas" width="400" height="300" style="width: 100%; height:30rem">')
  var ctx = document.getElementById('canvas');
  var myChart = new Chart(ctx, {
      type: 'horizontalBar',
      data: {
          labels: datos.labels,
          datasets: datos.datasets,
      },
      options: {
        scales: {
            xAxes: [{
                gridLines: {
                    offsetGridLines: true
                }
            }]
        }
      }
  });
}
function obtenerDatosTipoHuevo(){
  //función que recorre el ultimo json y obtiene los datos necesarios
  labels = ["Not in Eggs", "2 km", "5 km", "10 km"]
  datasets = []
  datasets.push({label:"Tipo de huevo",
                  backgroundColor:[colores[0], colores[1], colores[2], colores[3]],
                  borderColor:"#000000",
                  borderWidth:1,
                  data:[0,0,0,0]})
  $.each(datosSeleccionados, function(i, pokemon){
    //ahora los datasets
    switch (pokemon.egg){
      case "Not in Eggs": datasets[0].data[0]++; break;
      case "2 km": datasets[0].data[1]++; break;
      case "5 km": datasets[0].data[2]++; break;
      case "10 km": datasets[0].data[3]++; break;
    }
  })
  return {labels:labels, datasets:datasets}
}
function graficoTipoHuevo(tipo="doughnut"){
  datos = obtenerDatosTipoHuevo()
  if($("#botonSemicirculo")){
    $("#botonSemicirculo").remove()
    $("#botonTarta").remove()
  }
  $("#canvas").remove()
  $("#divCanvas").append(`<button type="button" class="btn btn-secondary" id="botonTarta">Tarta/Donut</button>`)
  if (tipo=="doughnut"){
    $("#divCanvas").append(`<button type="button" class="btn btn-secondary" id="botonSemicirculo">Semi/Circulo</button> `)
  }
  $("#divCanvas").append('<canvas id="canvas" width="400" height="300" style="width: 100%; height:30rem"><br><br>')
  var ctx = document.getElementById('canvas');
  var myChart = new Chart(ctx, {
      type: tipo,
      data: {
          labels: datos.labels,
          datasets: datos.datasets,
      },
      options: {
        responsive: true,
				legend: {
					position: 'top',
				},
				animation: {
					animateScale: true,
					animateRotate: true
				}
      }
  });

  //modificado a partir de view-source:https://www.chartjs.org/samples/latest/charts/doughnut.html
  $("#botonSemicirculo").on("click", function(){
    if (myChart.options.circumference === Math.PI) {
				myChart.options.circumference = 2 * Math.PI;
				myChart.options.rotation = -Math.PI / 2;
			} else {
				myChart.options.circumference = Math.PI;
				myChart.options.rotation = -Math.PI;
			}
      myChart.update()
  })

  $("#botonTarta").on("click", function(){
    if (tipo=="doughnut") graficoTipoHuevo("pie")
    else graficoTipoHuevo()
  })

}
