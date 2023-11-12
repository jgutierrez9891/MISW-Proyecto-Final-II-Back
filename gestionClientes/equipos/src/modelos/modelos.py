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

class Ficha_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(2000))
    id_empresa = db.Column(db.Integer)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))

class Empleado(db.Model):
    __bind_key__ = "empleados"
    id = db.Column(db.Integer, primary_key=True)
    tipo_doc = db.Column(db.String(50))
    num_doc = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    usuario = db.Column(db.String(50))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    ciudad = db.Column(db.String(50))
    fecha_nacimiento= db.Column(db.Date)
    idiomas = db.Column(db.String(200))
    estado = db.Column(db.String(50))
    fecha_evaluacion = db.Column(db.Date)
    evaluaciones = db.Column(db.Integer)
    habilidades = db.relationship('EmpleadoHabilidad', back_populates='empleado')

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('id', 
                  'tipo_doc', 
                  'num_doc', 
                  'nombre',
                  'usuario',
                  'telefono',
                  'email',
                  'pais',
                  'ciudad',
                  'fecha_nacimiento',
                  'idiomas',
                  'fecha_evaluacion',
                  'evaluaciones',
                  'habilidades'
                  )
        include_relationships = True
        load_instance = True

    # habilidades = fields.List(fields.Nested(HabilidadesempSchema()))

class Habilidadesemp(db.Model):
    __bind_key__ = "empleados"
    id = db.Column(db.Integer, primary_key=True)
    habilidad = db.Column(db.String(50), nullable=False, unique=True)
    empleados = db.relationship('EmpleadoHabilidad', back_populates='habilidad')

class EmpleadoHabilidad(db.Model):
    __bind_key__ = "empleados"
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    habilidad_id = db.Column(db.Integer, db.ForeignKey('habilidadesemp.id'), nullable=False)

    empleado = db.relationship('Empleado', back_populates='habilidades')
    habilidad = db.relationship('Habilidadesemp', back_populates='empleados')

    def to_dict(self):
        return {
            'id': self.habilidad.id,
            'habilidad': self.habilidad.habilidad, 
        }

class Empleado_ficha_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ficha_trabajo = db.Column(db.Integer, db.ForeignKey('ficha_trabajo.id'))
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id'))
    
class Rol_ficha_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ficha_trabajo = db.Column(db.Integer, db.ForeignKey('ficha_trabajo.id'))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol'))

class Ficha_trabajoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'id_empresa', 'id_proyecto')
        include_relationships = True
        load_instance = True
    

class Hoja_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_trabajo = db.Column(db.String(100))
    descripcion_candidato_ideal = db.Column(db.String(5000))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))

class Empleado_evaluacion(db.Model):
    __bind_key__ = "empleados"
    id = db.Column(db.Integer, primary_key=True)
    evaluacion = db.Column(db.String(1000))
    puntaje = db.Column(db.Integer)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'))

class Hoja_trabajoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre_trabajo', 'descripcion_candidato_ideal', 'id_proyecto')
        include_relationships = True
        load_instance = True

class Candidatos_hoja_trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_hoja_trabajo = db.Column(db.Integer, db.ForeignKey('hoja_trabajo.id'))
    id_candidato = db.Column(db.Integer)

class Candidatos_hoja_trabajoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_hoja_trabajo', 'id_candidato')
        include_relationships = True
        load_instance = True 

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    id_empresa = db.Column(db.Integer)
    fichas_trabajo = db.relationship('Ficha_trabajo', cascade='all, delete, delete-orphan')
    hojas_trabajo = db.relationship('Hoja_trabajo', cascade='all, delete, delete-orphan')

class ProyectoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'titulo', 'fecha_inicio', 'fecha_fin', 'id_empresa', 'fichas_trabajo', 'hojas_trabajo')
        include_relationships = True
        load_instance = True
 
    fichas_trabajo = fields.List(fields.Nested(Ficha_trabajoSchema()))
    hojas_trabajo = fields.List(fields.Nested(Hoja_trabajoSchema()))

#ROL
class Rol(db.Model):
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60))
    descripcion = db.Column(db.String(250))

class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = False
        load_instance = True
        
        
#HABILIDAD
class Habilidad(db.Model):
    id_habilidad = db.Column(db.Integer, primary_key=True)
    habilidad = db.Column(db.String(60))
    tipo = db.Column(db.String(60))

class HabilidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Habilidad
        include_relationships = False
        load_instance = True
        
        

#ROL_HABILIDAD
class RolHabilidad(db.Model):
    id_asoc = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer)
    id_habilidad = db.Column(db.Integer)

class RolHabilidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RolHabilidad
        include_relationships = False
        load_instance = True
