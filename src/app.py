"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Vehicles, FavoritePlanets, FavoriteCharacters, FavoriteVehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#get all user
@app.route('/user', methods=['GET'])
def get_all_user():
    all_users = User.query.all()
    serialized_all_users = list(map(lambda user: user.serialize(), all_users))
    return jsonify({'msg': 'Los usuarios obtenidos son:', 'results': serialized_all_users}), 200

#get one user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    serialized_user = user.serialize()
    return jsonify({'msg': 'El usuario obtenido es:', 'results': serialized_user}), 200

#create user
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    if "email" not in body:
        return jsonify({'msg': 'El campo email es obligatorio'})
    if "password" not in body:
        return jsonify({'msg': 'El campo password es obligatorio'})
    if "is_active" not in body:
        return jsonify({'msg': 'El campo is active es obligatorio'})
    new_user = User()
    new_user.name = body['name']
    new_user.email = body['email']
    new_user.password = body['password']
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'Usuario creado con éxito'})

#delete user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'El usuario se eliminó con éxito'})

#get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    serialized_all_planets = list(map(lambda planets: planets.serialize(), all_planets))
    return jsonify({'msg': 'Planetas obtenidos:', 'results': serialized_all_planets}), 200

#get one planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    print(planet_id)
    planet = Planets.query.get(planet_id)
    serialized_planet = planet.serialize()
    return jsonify({'msg': 'El planeta obtenido es:', 'results': serialized_planet}), 200

#add planet
@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    if "diameter" not in body:
        return jsonify({'msg': 'El campo diameter es obligatorio'})
    if "climate" not in body:
        return jsonify({'msg': 'El campo climate es obligatorio'})
    new_planet = Planets()
    new_planet.name = body['name']
    new_planet.diameter = body['diameter']
    new_planet.climate = body['climate']
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'msg': 'Planeta creado con éxito'})
  
#edit planet name
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    planet = Planets.query.get(planet_id)
    planet.name = body['name']
    db.session.commit()
    return jsonify({'msg': 'El nombre del planeta se actualizó con éxito'})

#delete planet
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'El planeta se eliminó con éxito'})

#get all characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Characters.query.all()
    serialized_all_characters = list(map(lambda characters: characters.serialize(), all_characters))
    return jsonify({'msg': 'Personajes obtenidos:', 'results': serialized_all_characters}), 200

#get one character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    serialized_character = character.serialize()
    return jsonify({'msg': 'El personaje obtenido es:', 'results': serialized_character}), 200

#add character
@app.route('/characters', methods=['POST'])
def create_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    if "description" not in body:
        return jsonify({'msg': 'El campo description es obligatorio'})
    if "gender" not in body:
        return jsonify({'msg': 'El campo gender es obligatorio'})
    new_character = Characters()
    new_character.name = body['name']
    new_character.diameter = body['description']
    new_character.climate = body['gender']
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'Personaje creado con éxito'})
  
#edit character name
@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    character = Characters.query.get(character_id)
    character.name = body['name']
    db.session.commit()
    return jsonify({'msg': 'El nombre del personaje se actualizó con éxito'})

#delete character
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'El personaje se eliminó con éxito'})

#get all vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicles.query.all()
    serialized_all_vehicless = list(map(lambda vehicles: vehicles.serialize(), all_vehicles))
    return jsonify({'msg': 'Vehiculos obtenidos:', 'results': serialized_all_vehicless}), 200

#get one vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    serialized_vehicle = vehicle.serialize()
    return jsonify({'msg': 'El vehiculo obtenido es:', 'results': serialized_vehicle}), 200

#add vehicle
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    if "description" not in body:
        return jsonify({'msg': 'El campo description es obligatorio'})
    if "model" not in body:
        return jsonify({'msg': 'El campo model es obligatorio'})
    new_vehicle = Characters()
    new_vehicle.name = body['name']
    new_vehicle.diameter = body['description']
    new_vehicle.climate = body['model']
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'msg': 'Vehiculo creado con éxito'})
  
#edit vehicle name
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if "name" not in body:
        return jsonify({'msg': 'El campo name es obligatorio'})
    vehicle = Vehicles.query.get(vehicle_id)
    vehicle.name = body['name']
    db.session.commit()
    return jsonify({'msg': 'El nombre del vehiculo se actualizó con éxito'})

#delete vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'msg': 'El vehiculo se eliminó con éxito'})

#get favorites planets
@app.route('/favoritePlanets/user/<int:user_id>', methods=['GET'])
def get_favorite_planets(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El Usuario con ID {} no existe'.format(user_id)}), 404
    favorite_planets = db.session.query(FavoritePlanets, Planets).join(Planets).filter(FavoritePlanets.user_id == user_id).all()
    favorite_planets_serialize = []
    for favorite_item, planet_item in favorite_planets:
        favorite_planets_serialize.append({'planet': planet_item.serialize()})
    return jsonify({'Los Planetas Favoritos son': favorite_planets_serialize, 'El usuario al que corresponde': user.serialize()}), 200

#add favorites planets
@app.route('/favoritePlanets/user/<int:user_id>', methods=['POST'])
def create_favorite_planets(user_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    favorite = FavoritePlanets(**body, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'El Planeta se agregó a favoritos'})
  
  #get favorites characters
@app.route('/favoriteCharacters/user/<int:user_id>', methods=['GET'])
def get_favorite_characters(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El Usuario con ID {} no existe'.format(user_id)}), 404
    favorite_characters = db.session.query(FavoriteCharacters, Characters).join(Characters).filter(FavoriteCharacters.user_id == user_id).all()
    favorite_characters_serialize = []
    for favorite_item, character_item in favorite_characters:
        favorite_characters_serialize.append({'character': character_item.serialize()})
    return jsonify({'Los Personajes Favoritos son': favorite_characters_serialize, 'El usuario al que corresponde': user.serialize()}), 200

#add favorites characters
@app.route('/favoriteCharacters/user/<int:user_id>', methods=['POST'])
def create_favorite_characters(user_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    favorite = FavoriteCharacters(**body, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'El Personaje se agregó a favoritos'})

  #get favorites vehicles
@app.route('/favoriteVehicles/user/<int:user_id>', methods=['GET'])
def get_favorite_vehicles(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El Usuario con ID {} no existe'.format(user_id)}), 404
    favorite_vehicles = db.session.query(FavoriteVehicles, Vehicles).join(Vehicles).filter(FavoriteVehicles.user_id == user_id).all()
    favorite_vehicles_serialize = []
    for favorite_item, vehicle_item in favorite_vehicles:
        favorite_vehicles_serialize.append({'character': vehicle_item.serialize()})
    return jsonify({'Los Vehiculos Favoritos son': favorite_vehicles_serialize, 'El usuario al que corresponde': user.serialize()}), 200

#add favorites vehicles
@app.route('/favoriteVehicles/user/<int:user_id>', methods=['POST'])
def create_favorite_vehicles(user_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    favorite = FavoriteVehicles(**body, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'El Vehiculo se agregó a favoritos'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
