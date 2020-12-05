from app import model
from flask_restful import reqparse, abort, Api, Resource
from flask import request
parserGet = reqparse.RequestParser()
parserGet.add_argument('page', 0, type=int, help="Página a mostrar")
parserGet.add_argument('per_page', model.MAX_ELEMS, type=int, help="Número de elementos por página")
parserGet.add_argument('nombre', type=str, help="Nombre del pokemon")
parserGet.add_argument('tipo', type=str, help="Tipo de pokemon")
parserGet.add_argument('tipoHuevo', type=str, help="Tipo de huevo")
parserGet.add_argument('evolucion', type=str, help="Número de evolución")

parserPost = reqparse.RequestParser()
parserPost.add_argument("name", type=str, required=True, help="El campo name no puede ser vacío.", location='json')
parserPost.add_argument("img", type=str, required=True, help="El campo img no puede ser vacío.", location='json')
parserPost.add_argument("type", type=list, required=True, help="El campo type no puede ser vacío.", location='json')
parserPost.add_argument("height", type=float, required=True, help="El campo height no puede ser vacío.", location='json')
parserPost.add_argument("weight", type=float, required=True, help="El campo weight no puede ser vacío.", location='json')
parserPost.add_argument("candy", type=str, required=True, help="El campo candy no puede ser vacío.", location='json')
parserPost.add_argument("candy_count", type=int, required=True, help="El campo candy_count no puede ser vacío.", location='json')
parserPost.add_argument("egg", type=str, required=True, help="El campo egg no puede ser vacío.", location='json')
parserPost.add_argument("spawn_chance", type=float, required=True, help="El campo spawn_chance no puede ser vacío.", location='json')
parserPost.add_argument("avg_spawns", type=float, required=True, help="El campo avg_spawns no puede ser vacío.", location='json')
parserPost.add_argument("spawn_time", type=str, required=True, help="El campo spawn_time no puede ser vacío.", location='json')
parserPost.add_argument("multipliers", type=float, required=True, help="El campo multipliers no puede ser vacío.", location='json')
parserPost.add_argument("weaknesses", type=list, required=True, help="El campo weaknesses no puede ser vacío.", location='json')
parserPost.add_argument("next_evolution", type=str, location='json')
parserPost.add_argument("prev_evolution", type=str, location='json')

parserPut = reqparse.RequestParser()
parserPut.add_argument("name", type=str, location='json')
parserPut.add_argument("img", type=str, location='json')
parserPut.add_argument("height", type=float, location='json')
parserPut.add_argument("weight", type=float, location='json')
parserPut.add_argument("candy", type=str, location='json')
parserPut.add_argument("candy_count", type=int, location='json')
parserPut.add_argument("egg", type=str, location='json')
parserPut.add_argument("spawn_chance", type=float, location='json')
parserPut.add_argument("avg_spawns", type=float, location='json')
parserPut.add_argument("spawn_time", type=str, location='json')

class Pokemon(Resource):
    def get(self):
        #opcion de paginar o no y filtrar por nombre, tipo, tipo de huevo y evolución
        args = parserGet.parse_args()
        datos = model.obtenerPokemons(args, args["per_page"], args["page"])
        json = [{k:v for k,v in documento.items() if k != "_id"} for documento in datos]
        return json
    def post(self):
        args = parserPost.parse_args()
        #se modifican algunos campos
        args["multipliers"] = [args["multipliers"]]
        args["height"] = str(args["height"]) + " m"
        args["weight"] = str(args["weight"]) + " kg"
        if args["next_evolution"] is None: args.pop("next_evolution")
        if args["prev_evolution"] is None: args.pop("prev_evolution")

        resul = model.addPokemon(args)

        if resul[0]:#si todo es correcto se retorna el id, si no se retorna un error
            return resul[1]
        else:
            return {"Error": "No ha podido insertarse el pokemon"}

class PokemonID(Resource):
    def delete(self, id):
        if model.borrarPokemonID(id):
            return {"Resultado": "Borrado correcto", "id":id}
        else:
            return {"Error": "No se ha podido eliminar el pokemon"}
    def put(self, id):
        args = parserPut.parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        #se modifica y se obtienen los datos modificados
        resulMod = model.modificarPokemonID(id, args)
        if resulMod is True:
            datos = model.obtenerPokemonID(id)
            datos.pop("_id")
            return datos

        else:
            return {"Error": "No se ha podido modificar el pokemon"}
