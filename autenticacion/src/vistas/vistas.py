from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from modelos.modelos import db, Candidato
    
class VistaLogInCandidato(Resource):

    def post(self):
        candidato = Candidato.query.filter(Candidato.usuario == request.json["usuario"],
                                             Candidato.clave == request.json["clave"]).first()
        
        if candidato is None:
            return {"mensaje": "Autenticación fallida"}, 404
        else:
            token_de_acceso = create_access_token(identity=candidato.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}