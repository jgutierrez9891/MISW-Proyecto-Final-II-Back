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

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    id_empresa = db.Column(db.Integer)

class ProyectoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        include_relationships = False
        load_instance = True

class Ficha_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(2000))
    id_proyecto = db.Column(db.Integer)

class Ficha_trabajoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ficha_trabajo
        include_relationships = False
        load_instance = True