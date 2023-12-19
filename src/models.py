from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

#informacion cuando se hace print en el admin
    def __repr__(self):
        return 'User ID: {} - Name: {}'.format(self.id, self.name)

#convertir de clase a objeto
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)

#informacion cuando se hace print
    def __repr__(self):
        return 'Planet {}'.format(self.name)

#convertir de clase a objeto
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter
        }

class Characters(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return 'Character {}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender
        }

class Vehicles(db.Model):
    __tablename__='vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return 'Vehicle {}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "passengers": self.passengers
        }

class FavoritePlanets(db.Model):
    __tablename__='favoriteplanets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    planet_relationship = db.relationship(Planets)

    def __repr__(self):
        return 'User ID: {} - Planet ID: {}'.format(self.user_id, self.planet_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavoriteCharacters(db.Model):
    __tablename__='favoritecharacters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    character_relationship = db.relationship(Characters)

    def __repr__(self):
        return 'User ID: {} - Character ID: {}'.format(self.user_id, self.character_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoriteVehicles(db.Model):
    __tablename__='favoritevehicles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    vehicle_relationship = db.relationship(Vehicles)

    def __repr__(self):
        return 'User ID: {} - Vehicle ID: {}'.format(self.user_id, self.vechicle_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }