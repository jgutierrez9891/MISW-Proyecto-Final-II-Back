from flask import request
from flask_restful import Resource
from modelos.modelos import db, Representante, Empresa
import re
    
class VistaRegistroEmpresa(Resource):

    def post(self):
        empresa_tipo_doc = request.json.get("empresa_tipo_doc")
        empresa_num_doc = request.json.get("empresa_num_doc")
        empresa_nombre = request.json.get("empresa_nombre")
        empresa_email = request.json.get("empresa_email")
        empresa_telefono = request.json.get("empresa_telefono")

        representante_tipo_doc = request.json.get("representante_tipo_doc")
        representante_num_doc = request.json.get("representante_num_doc")
        representante_nombre = request.json.get("representante_nombre")
        representante_email = request.json.get("representante_email")
        representante_telefono = request.json.get("representante_telefono")
        representante_usuario = request.json.get("representante_usuario")
        representante_clave = request.json.get("representante_clave")

        if empresa_tipo_doc is None or empresa_num_doc is None or empresa_nombre is None or empresa_email is None or empresa_telefono is None or representante_tipo_doc is None or representante_num_doc is None or representante_nombre is None or representante_nombre is None or representante_email is None or representante_telefono is None or representante_usuario is None or representante_clave is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar todos los datos de la empresa y representante"}, 400
        
        if empresa_tipo_doc == "" or empresa_num_doc == "" or empresa_nombre == "" or empresa_email == "" or empresa_telefono == "" or representante_tipo_doc == "" or representante_num_doc == "" or representante_nombre == "" or representante_nombre == "" or representante_email == "" or representante_telefono == "" or representante_usuario == "" or representante_clave == "":
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar todos los datos de la empresa y representante"}, 400
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not(re.fullmatch(regex, empresa_email)):
            return {"status_code": 400, "message": "El formato del correo de empresa es inválido"}, 400
        
        if not(re.fullmatch(regex, representante_email)):
            return {"status_code": 400, "message": "El formato del correo de representante es inválido"}, 400

        empresa_actual = Empresa.query.filter(Empresa.tipo_doc == empresa_tipo_doc, Empresa.num_doc == empresa_num_doc).first()
        db.session.commit()
        empresa_correo = Empresa.query.filter(Empresa.email == empresa_email).first()
        db.session.commit()
        representante_actual = Representante.query.filter(Representante.tipo_doc == representante_tipo_doc, Representante.num_doc == representante_num_doc).first()
        db.session.commit()
        representante_correo = Representante.query.filter(Representante.email == representante_email).first()
        db.session.commit()
        representante_usuario_actual = Representante.query.filter(Representante.usuario == representante_usuario).first()
        db.session.commit()

        if empresa_actual is not None:
            return {"status_code": 409, "message": "La empresa ingresada ya existe"}, 409

        if empresa_correo is not None:
            return {"status_code": 409, "message": "El correo de empresa ingresado ya existe"}, 409
    
        if representante_actual is not None:
            return {"status_code": 409, "message": "El representante ingresado ya existe"}, 409
        
        if representante_correo is not None:
            return {"status_code": 409, "message": "El correo de representante ingresado ya existe"}, 409
        
        if representante_usuario_actual is not None:
            return {"status_code": 409, "message": "El usuario ingresado ya existe"}, 409

        empresa = Empresa(tipo_doc = empresa_tipo_doc,
                              num_doc = empresa_num_doc,
                              nombre = empresa_nombre,
                              email = empresa_email,
                              telefono = empresa_telefono)
        try:
            db.session.add(empresa)
            db.session.commit()
        except Exception as err:
            print("VA A RETORNAR 500 POR ERROR: "+str(err))
            return {"status_code": 500, "message": "Error creando empresa"}, 500
        
        empresa = Empresa.query.filter(Empresa.tipo_doc == empresa_tipo_doc,
                                           Empresa.num_doc == empresa_num_doc).first()
        if empresa is None:
            print("No existe la empresa")
            return {"status_code": 500, "message": "Error creando empresa"}, 500
        else:           
            representante = Representante(tipo_doc = representante_tipo_doc,
                                        num_doc = representante_num_doc,
                                        nombre = representante_nombre,
                                        email = representante_email,
                                        telefono = representante_telefono,
                                        usuario = representante_usuario,
                                        clave = representante_clave,
                                        id_empresa = empresa.id)
            try:
                db.session.add(representante)
                db.session.commit()
                return {"status_code": 200, "message": "Empresa y representante creados exitosamente"}, 200
            except Exception as err:
                print("VA A RETORNAR 500 POR ERROR: "+str(err))
                return {"status_code": 500, "message": "Error creando representante"}, 500
        
        