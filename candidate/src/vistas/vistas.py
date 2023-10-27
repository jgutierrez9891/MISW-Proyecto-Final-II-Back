from http.client import NOT_FOUND
from flask import request
from flask_restful import Resource
from modelos import db, candidato, candidatoSchema, entrevista, entrevistaSchema, empresa, empresaSchema, infoTecnica, infoTecnicaSchema
from servicios import SaveCandidate, SaveInfoTecnica
from flask_jwt_extended import jwt_required
import re

candidato_schema = candidatoSchema(many=True)
candidato_schema_single = candidatoSchema()

entrevista_schema = entrevistaSchema(many=True)
entrevista_schema_single = entrevistaSchema()

empresa_schema = empresaSchema(many=True)
empresa_schema_single = empresaSchema()

infoTecnica_schema = infoTecnicaSchema(many=True)
infoTecnica_schema_single = infoTecnicaSchema()
    
class VistaCrearCandidato(Resource):

    def post(self):

        tipo_doc = request.json.get("tipo_doc")
        num_doc = request.json.get("num_doc")
        nombre = request.json.get("nombre")
        usuario = request.json.get("usuario")
        clave = request.json.get("clave")
        telefono = request.json.get("telefono")
        email = request.json.get("email")
        pais = request.json.get("pais")
        ciudad = request.json.get("ciudad")
        aspiracion_salarial = request.json.get("aspiracion_salarial")
        fecha_nacimiento = request.json.get("fecha_nacimiento")
        idiomas = request.json.get("idiomas")

        if tipo_doc is None or num_doc is None or nombre is None or usuario is None or clave is None \
            or telefono is None or email is None or pais is None or ciudad is None or aspiracion_salarial is None\
            or fecha_nacimiento is None or idiomas is None:
            
            return {"status_code": 400, "message": "Ingrese todos los campos requeridos"}, 400
        
        elif tipo_doc == "" or num_doc == "" or nombre == "" or usuario == "" or "clave" == "" or telefono == "" \
        or email == "" or pais == "" or ciudad == "" or aspiracion_salarial == "" or fecha_nacimiento == "" \
        or idiomas == "":

            return {"status_code": 400, "message": "Campo requerido se encuentra vacío"}, 400
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not(re.fullmatch(regex, email)):
            return {"status_code": 400, "message": "El formato del correo es inválido"}, 400

        candidato_documento = candidato.query.filter(candidato.num_doc == num_doc).first()
        db.session.commit()
        candidato_usuario = candidato.query.filter(candidato.usuario == usuario).first()
        db.session.commit()
        candidato_correo = candidato.query.filter(candidato.email == email).first()
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
    

#Vista que guarda la información técnica de un candidato
class VistaInformacionTecnica(Resource):

    @jwt_required()
    def post(self):

        tipo = request.json.get("tipo")
        valor = request.json.get("valor")
        id_candidato = request.json.get("id_candidato")

        if tipo is None or valor is None or id_candidato is None:
            return {"status_code": 400, "message": "Ingrese todos los campos requeridos"}, 400
        
        elif tipo == "" or valor == "" or id_candidato == "":
            return {"status_code": 400, "message": "Campo requerido se encuentra vacío"}, 400
        
        candidato_id = candidato.query.filter(candidato.id == id_candidato).first()
        db.session.commit()

        if candidato_id is None:
            return {"status_code": 409, "message": "El id_candidato ingresado no existe"}, 409

        data = request.json
        response = SaveInfoTecnica(
            data['tipo'],
            data['valor'],
            data['id_candidato'],
            )
        return {"id":response.id, "status_code": 201, "message": "Informacion registrada exitosamente"}, 201


class ping(Resource):
    
    def get(self):
        return "pong", 200