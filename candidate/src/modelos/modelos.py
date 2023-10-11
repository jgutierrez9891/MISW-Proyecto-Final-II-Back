from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(50))
    num_doc = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    usuario = db.Column(db.String(50))
    clave = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    email = db.Column(db.String(100))
    pais = db.Column(db.String(50))
    ciudad = db.Column(db.String(50))
    aspiracion_salarial = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.DateTime)
    idiomas = db.Column(db.String(200))

class candidatoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = candidato
        include_relationships = True
        load_instance = True

