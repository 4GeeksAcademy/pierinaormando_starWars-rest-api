from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__:'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#informacion cuando se hace print
    def __repr__(self):
        return 'Usuario con id {} y nombre {}'.format(self.id, self.nombre)

#convertir de clase a objeto
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__:'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)

#informacion cuando se hace print
    def __repr__(self):
        return '<Planets %r>' % self.name

#convertir de clase a objeto
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter
        }