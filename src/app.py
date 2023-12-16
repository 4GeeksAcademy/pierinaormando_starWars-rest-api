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
from models import db, User, Planet
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
    print(user_id)
    user = User.query.get(user_id)
    serialized_user = user.serialize()
    return jsonify({'msg': 'El usuario obtenido es:', 'results': serialized_user}), 200

#get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    serialized_all_planets = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify({'msg': 'Planetas obtenidos:', 'results': serialized_all_planets}), 200

#get one planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    print(planet_id)
    planet = Planet.query.get(planet_id)
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
    new_planet = Planet()
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
    """ if "diameter" not in body:
        return jsonify({'msg': 'El campo diameter es obligatorio'})
    if "climate" not in body:
        return jsonify({'msg': 'El campo climate es obligatorio'}) """
    planet = Planet.query.get(planet_id)
    planet.name = body['name']
    """ planet.diameter = body['diameter']
    planet.climate = body['climate'] """
    db.session.commit()
    return jsonify({'msg': 'El nombre del planeta se actualizó con éxito'})

#delete planet
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'El planeta se eliminó con éxito'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
