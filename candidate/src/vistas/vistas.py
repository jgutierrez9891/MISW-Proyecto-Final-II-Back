from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from modelos import db, candidato, candidatoSchema
from servicios import SaveCandidate
import re

candidato_schema = candidatoSchema(many=True)
candidato_schema_single = candidatoSchema()
    
class VistaCrearCandidato(Resource):

    def post(self):

        #Check if some field is empty
        if request.json["tipo_doc"] == "" or request.json["num_doc"] == "" or request.json["nombre"] == "" or request.json["usuario"] == "" or request.json["clave"] == "" or request.json["telefono"] == "" \
        or request.json["email"] == "" or request.json["pais"] == "" or request.json["ciudad"] == "" or request.json["aspiracion_salarial"] == "" or request.json["fecha_nacimiento"] == "" \
        or request.json["idiomas"] == "":

            return {"status_code": 401, "message": "Debe ingresar todos los campos"}, 401
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not(re.fullmatch(regex, request.json["email"])):
            return {"status_code": 402, "message": "El formato del correo es inválido"}, 402

        candidato_documento = candidato.query.filter(candidato.num_doc == request.json["num_doc"]).first()
        db.session.commit()
        candidato_usuario = candidato.query.filter(candidato.usuario == request.json["usuario"]).first()
        db.session.commit()
        candidato_correo = candidato.query.filter(candidato.email == request.json["email"]).first()
        db.session.commit()

        if candidato_documento is not None:
            return {"status_code": 402, "message": "El documento ingresado ya existe"}, 402
        elif candidato_usuario is not None:
            return {"status_code": 402, "message": "El usuario ingresado ya existe"}, 402
        elif candidato_correo is not None:
            return {"status_code": 402, "message": "El correo ingresado ya existe"}, 402


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
        return {"id":response.id, "status_code": "200", "message": "Candidato creado exitosamente"}
    

class ping(Resource):

    def get(self):
        return "pong", 200