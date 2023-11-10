from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from modelos.modelos import db, Candidato, Representante, Empresa
import base64
import requests 
    
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
            
            
            
class CambioContraseña(Resource):
        
    def post(self):
        
        if request.json is None:
            return {"status_code": 400, "message": "Debe ingresar todos los campos"}, 400
        
        if request.json.get('email') is None:
            return {"status_code": 400, "message": "Debe ingresar todos los campos"}, 400
        
        representante = Representante.query.filter(Representante.email == request.json["email"]).first()
        
        if representante is None:
            candidato = Candidato.query.filter(Candidato.email == request.json["email"]).first()
            if candidato is None:
                return {"status_code": 404, "message": "No se encontro el correo"}, 404
            else:
                try:
                    request_response = requests.post("https://api.mailgun.net/v3/sandbox430d3da59f4642aab1e69fa5e3b1aa46.mailgun.org/messages",
                    auth=("api",base64.b64decode("MmU2YzkwNWI1ZmE0MzIzYzE1ZTQ2MjU3ZjEzOTE1ZmMtOGM5ZTgyZWMtMjdmZjViZjM=").decode('utf-8')),
                    data={"from":"danielmailguntest@gmail.com","to":representante.email,"subject":"Cambio de contraseña","text":"Su contraseña fue cambiada exitosamente."})
                    return {"status_code": 200,"mensaje": "Correo enviado Exitosamente"},200
                except Exception as e:
                    return {"status_code": 500, "message": "No se pudo enviar el correo"}, 500
        else:
            try:
                request_response = requests.post("https://api.mailgun.net/v3/sandbox430d3da59f4642aab1e69fa5e3b1aa46.mailgun.org/messages",
                auth=("api",base64.b64decode("MmU2YzkwNWI1ZmE0MzIzYzE1ZTQ2MjU3ZjEzOTE1ZmMtOGM5ZTgyZWMtMjdmZjViZjM=").decode('utf-8')),
                data={"from":"danielmailguntest@gmail.com","to":representante.email,"subject":"Cambio de contraseña","text":"Su contraseña fue cambiada exitosamente."})
                return {"status_code": 200,"mensaje": "Correo enviado Exitosamente"},200
            except Exception as e:
                return {"status_code": 500, "message": "No se pudo enviar el correo"}, 500

class ping(Resource):
    
    def get(self):
        return "pong", 200