from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from modelos.modelos import db, Candidato, Representante, Empresa
    
class VistaLogInCandidato(Resource):

    def post(self):
        candidato = Candidato.query.filter(Candidato.usuario == request.json["usuario"],
                                           Candidato.clave == request.json["clave"]).first()
        
        if candidato is None:
            return {"mensaje": "Autenticación fallida"}, 404
        else:
            token_de_acceso = create_access_token(identity=candidato.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "info_candidato": {
                    "usuario": candidato.usuario,
                    "nombre": candidato.nombre,
                    "email": candidato.email,
                    "id": candidato.id}
            }
            
    
class VistaLogInEmpresa(Resource):
        
    def post(self):
        
        if request.json.get('usuario') is None or request.json.get('clave') is None:
            return {"status_code": 400, "message": "Debe ingresar todos los campos"}, 400
        
        representante = Representante.query.filter(Representante.usuario == request.json["usuario"],
                                                   Representante.clave == request.json["clave"]).first()
        
        if representante is None:
            return {"mensaje": "Autenticación fallida"}, 404
        else:
            empresa = Empresa.query.filter(Empresa.id == representante.id_empresa).first()
            token_de_acceso = create_access_token(identity=representante.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso,
                    "info_representante":{
                        "usuario":representante.usuario,
                        "tipo_doc":representante.tipo_doc,
                        "num_doc":representante.num_doc,
                        "nombre":representante.nombre,
                        "id_representante":representante.id
                    },
                    "info_empresa":{
                        "nombre":empresa.nombre,
                        "id_empresa":empresa.id
                    }}