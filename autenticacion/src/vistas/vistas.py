from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from modelos import db, Candidato, Representante


    
class VistaLogInCandidato(Resource):

    def post(self):
        candidato = Candidato.query.filter(Candidato.usuario == request.json["usuario"],
                                             Candidato.clave == request.json["clave"]).first()
        
        if candidato is None:
            return {"mensaje": "Autenticación fallida"}, 404
        else:
            token_de_acceso = create_access_token(identity=candidato.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
        
        
        
class VistaLogInEmpresa(Resource):
    
    def post(self):
        representante = Representante.query.filter(Representante.email == request.json["usuario"],
                                             Representante.clave == request.json["clave"]).first()
        
        if representante is None:
            return {"mensaje": "Autenticación fallida"}, 404
        else:
            token_de_acceso = create_access_token(identity=representante.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}