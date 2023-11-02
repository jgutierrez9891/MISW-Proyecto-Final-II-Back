import enum
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


class entrevista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_candidato = db.Column(db.String(50))
    fecha = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    id_empresa = db.Column(db.Integer)

class entrevistaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = entrevista
        include_relationships = True
        load_instance = True

class tipoHabilidad(enum.Enum):
    TECNOLOGIA = "Tecnologia"
    LENGUAJE = "Lenguaje"
    ROL = "Rol"

class infoTecnica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(tipoHabilidad))
    valor = db.Column(db.String(50))
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id'))

class infoTecnicaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = infoTecnica
        include_relationships = True
        load_instance = True
        
#EMPRESA
class empresa(db.Model):
    __bind_key__ = "empresas"
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(50))
    num_doc = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    nombre = db.Column(db.String(100))

class empresaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = empresa
        include_relationships = False
        load_instance = True