$(document).ready(function(){
  //al cargar el documento se genera el número a adivinar y se inicializan los intentos a 10
  numeroAdivinar = Math.floor(Math.random() * 100) + 1
  intentos = 10
  $("#intentos").text("Quedan 10 intentos")
  $("#botonProbar").click(function(){
    //al pulsar el boton se comprueba el número introducido
    numIntro = parseInt($("#numIntro").val())
    if (numIntro === numeroAdivinar){
      $("#cuerpoModal").html('<img src="https://img.icons8.com/bubbles/200/000000/trophy.png"><br>Enhorabuena!!! Has acertado!!!')
      $("#divBotonModal").html('<button type="button" class="btn btn-secondary" data-dismiss="modal" onClick="window.location.reload();">Volver a jugar</button>')
    }else if (numIntro < numeroAdivinar){
      $("#cuerpoModal").text("El número buscado es mayor")
    }else{
      $("#cuerpoModal").text("El número buscado es menor")
    }
    //se modifican los intentos restantes
    intentos -= 1
    $("#intentos").text("Quedan " + intentos + " intentos")
    if (numIntro !== numeroAdivinar && intentos <= 0){
      $("#cuerpoModal").html(`<img width="256" height="256" src="https://img.icons8.com/ios/452/loser.png">
                              <br>Has agotado el número de intentos, el número buscado era ` + numeroAdivinar)
      $("#divBotonModal").html('<button type="button" class="btn btn-secondary" data-dismiss="modal" onClick="window.location.reload();">Volver a jugar</button>')
    }
    $("#modalAdivinar").modal();
  });
});
