from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(10))
    num_doc = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

class EmpresaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        include_relationships = False
        load_instance = True
    
class Representante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(10))
    num_doc = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    usuario = db.Column(db.String(50))
    clave = db.Column(db.String(50))
    id_empresa = db.Column(db.Integer)

class RepresentanteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        include_relationships = False
        load_instance = True