from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from modelos import db, candidato, candidatoSchema
from servicios import SaveCandidate

candidato_schema = candidatoSchema(many=True)
candidato_schema_single = candidatoSchema()
    
class VistaCrearCandidato(Resource):

    def post(self):
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
        return candidato_schema_single.dump(response)