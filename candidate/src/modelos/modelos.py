import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow
from enum import Enum

db = SQLAlchemy()
ma = Marshmallow()

class tipoHabilidad(str, Enum):
    TECNOLOGIA = "Tecnologia"
    LENGUAJE = "Lenguaje"
    ROL = "Rol"
    
class infoTecnica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(tipoHabilidad))
    valor = db.Column(db.String(50))
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id'))

class infoTecnicaSchema(ma.Schema):
    class Meta:
        fields = ("id", "valor", "id_candidato")
        include_relationships = True
        load_instance = True    

class infoAcademica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    valor = db.Column(db.String(50))
    ano_finalizacion = db.Column(db.String(4))
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id'))

class infoAcademicaSchema(ma.Schema):
    class Meta:
        fields = ("id", "tipo", "valor", "ano_finalizacion", "id_candidato")
        include_relationships = True
        load_instance = True

class infoLaboral(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50))
    ano_inicio = db.Column(db.Integer)
    ano_fin = db.Column(db.Integer)
    empresa = db.Column(db.String(50))
    descripcion = db.Column(db.String(5000))
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id'))

class infoLaboralSchema(ma.Schema):
    class Meta:
        fields = ("id", "cargo", "ano_inicio", "ano_fin", "empresa", "descripcion", "id_candidato")
        include_relationships = True
        load_instance = True

class candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(50))
    num_doc = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    usuario = db.Column(db.String(50))
    clave = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    email = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    ciudad = db.Column(db.String(50))
    aspiracion_salarial = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.DateTime)
    idiomas = db.Column(db.String(200))
    fecha_ultima_evaluacion = db.Column(db.DateTime)
    promedio_evaluaciones = db.Column(db.Float)
    estado = db.Column(db.String(50))
    habilidades_tecnicas = db.relationship('infoTecnica', cascade='all, delete, delete-orphan')
    info_academica = db.relationship('infoAcademica', cascade='all, delete, delete-orphan')
    info_laboral = db.relationship('infoLaboral', cascade='all, delete, delete-orphan')

class candidatoSchema(ma.Schema):
    class Meta:
        fields = ("id", "tipo_doc", "num_doc", "nombre", "usuario", "clave", "telefono", "email", "pais", "ciudad", "aspiracion_salarial", "fecha_nacimiento", "idiomas", "fecha_ultima_evaluacion", "promedio_evaluaciones", "estado", "habilidades_tecnicas", "info_academica")
        include_relationships = True
        load_instance = True
    habilidades_tecnicas = fields.List(fields.Nested(infoTecnicaSchema()))
    info_academica = fields.List(fields.Nested(infoAcademicaSchema()))
    info_laboral = fields.List(fields.Nested(infoLaboralSchema()))

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