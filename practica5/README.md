# Práctica 5 de la asignatura
Se añade al sitio la posibilidad de ser consultado mediante llamadas a una API REST.
Los métodos son los siguientes:
### GET
  * Se aceptan los parámetros "name", "type", "egg" y "evolution" para filtrar los resultados devueltos
  * Por otro lado se permite la paginación de los resultados mediante el uso de los parámetros "page" y "per_page"
  * URL: ~/api/pokemons
  * Ejemplo: ~/api/pokemons?page=2&per_page=3&name=bulbasaur
### POST
  * Se requiere la recepción de un JSON con las siguientes claves:
    * "name"
    * "img"
    * "type"
    * "height"
    * "weight"
    * "candy"
    * "candy_count"
    * "egg"
    * "spawn_chance"
    * "avg_spawns"
    * "spawn_time"
    * "multipliers"
    * "weaknesses"
  * Permite también que se incluya las siguientes:
    * "next_evolution"
    * "prev_evolution"
  * URL: ~/api/pokemons
### PUT
  * Se recibe el id del pokemon y los datos a modificar en formato JSON.
  * URL: ~/api/pokemons/\<id>
### DELETE
  * Se recibe el id del pokemon
  * URL: ~/api/pokemons/\<id>
