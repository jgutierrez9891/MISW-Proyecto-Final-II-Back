from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from modelos import db, candidato, candidatoSchema, entrevista, entrevistaSchema, empresa, empresaSchema
from servicios import SaveCandidate
import re

candidato_schema = candidatoSchema(many=True)
candidato_schema_single = candidatoSchema()

entrevista_schema = entrevistaSchema(many=True)
entrevista_schema_single = entrevistaSchema()

empresa_schema = empresaSchema(many=True)
empresa_schema_single = empresaSchema()
    
class VistaCrearCandidato(Resource):

    def post(self):

        #Check if some field is empty
        if request.json["tipo_doc"] == "" or request.json["num_doc"] == "" or request.json["nombre"] == "" or request.json["usuario"] == "" or request.json["clave"] == "" or request.json["telefono"] == "" \
        or request.json["email"] == "" or request.json["pais"] == "" or request.json["ciudad"] == "" or request.json["aspiracion_salarial"] == "" or request.json["fecha_nacimiento"] == "" \
        or request.json["idiomas"] == "":

            return {"status_code": 400, "message": "Debe ingresar todos los campos"}, 400
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not(re.fullmatch(regex, request.json["email"])):
            return {"status_code": 400, "message": "El formato del correo es inválido"}, 400

        candidato_documento = candidato.query.filter(candidato.num_doc == request.json["num_doc"]).first()
        db.session.commit()
        candidato_usuario = candidato.query.filter(candidato.usuario == request.json["usuario"]).first()
        db.session.commit()
        candidato_correo = candidato.query.filter(candidato.email == request.json["email"]).first()
        db.session.commit()

        if candidato_documento is not None:
            return {"status_code": 409, "message": "El documento ingresado ya existe"}, 409
        elif candidato_usuario is not None:
            return {"status_code": 409, "message": "El usuario ingresado ya existe"}, 409
        elif candidato_correo is not None:
            return {"status_code": 409, "message": "El correo ingresado ya existe"}, 409


        data = request.json
        response = SaveCandidate(
            data['tipo_doc'],
            data['num_doc'],
            data['nombre'],
            data['usuario'],
            data['clave'],
            data['telefono'],
            data['email'],
            data['pais'],
            data['ciudad'],
            data['aspiracion_salarial'],
            data['fecha_nacimiento'],
            data['idiomas'],
            )
        return {"id":response.id, "status_code": 200, "message": "Candidato creado exitosamente"}
    
class VistaHistorialEntrevistas(Resource):
    
    def get(self):

        #Check if some field is empty
        if request.args.get('id_candidato') is None:
            return {"status_code": 400, "message": "Debe ingresar todos los campos"}, 400

        entrevistas_candidato = entrevista.query.filter(entrevista.id_candidato == request.args.get("id_candidato")).all()
        db.session.commit()

        listOfItems = []
        
        for entrevista_item in entrevistas_candidato:
            empresaNombre = empresa.query.filter(empresa.id == entrevista_item.id_empresa).all()
            db.session.commit()
            newEntrevistaFormat = {"id_entrevista":entrevista_item.id, "fecha_entrevista":entrevista_item.fecha, "estado":entrevista_item.estado, "empresa":empresaNombre[0].nombre}
            listOfItems.append(newEntrevistaFormat)

        return {"response":listOfItems, "status_code": 200}
    

class ping(Resource):
    
    def get(self):
        return "pong", 200