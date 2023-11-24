from http.client import NOT_FOUND
from flask import request, make_response
from flask_restful import Resource
from modelos import db, infoAcademica, candidato, candidatoSchema, entrevista, entrevistaSchema, empresa, empresaSchema, infoTecnica, infoTecnicaSchema, infoLaboral, ResultadoPruebaTecnicaSchema, ResultadoPruebaTecnica
from servicios import SaveCandidate, SaveInfoTecnica, save_info_laboral
from flask_jwt_extended import jwt_required
import re
import json

candidato_schema = candidatoSchema(many=True)
candidato_schema_single = candidatoSchema()

entrevista_schema = entrevistaSchema(many=True)
entrevista_schema_single = entrevistaSchema()

empresa_schema = empresaSchema(many=True)
empresa_schema_single = empresaSchema()

infoTecnica_schema = infoTecnicaSchema(many=True)
infoTecnica_schema_single = infoTecnicaSchema()

resultadoPruebaTecnica_schema = ResultadoPruebaTecnicaSchema(many=True)
resultadoPruebaTecnica_schema_single = ResultadoPruebaTecnicaSchema()

MENSAJE_CREACION_OK = 'Informacion registrada exitosamente'
MENSAJE_TODOS_DATOS = 'Ingrese todos los campos requeridos'
MENSAJE_CAMPO_VACIO = 'Campo requerido se encuentra vacío'
MENSAJE_CANDIDATO_NO_EXISTE = 'El id_candidato ingresado no existe'
    
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
            
            return {"status_code": 400, "message": MENSAJE_TODOS_DATOS}, 400
        
        elif tipo_doc == "" or num_doc == "" or nombre == "" or usuario == "" or "clave" == "" or telefono == "" \
        or email == "" or pais == "" or ciudad == "" or aspiracion_salarial == "" or fecha_nacimiento == "" \
        or idiomas == "":

            return {"status_code": 400, "message": MENSAJE_CAMPO_VACIO}, 400
        
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
            return {"status_code": 400, "message": MENSAJE_TODOS_DATOS}, 400
        
        elif tipo == "" or valor == "" or id_candidato == "":
            return {"status_code": 400, "message": MENSAJE_CAMPO_VACIO}, 400
        
        candidato_id = candidato.query.filter(candidato.id == id_candidato).first()
        db.session.commit()

        if candidato_id is None:
            return {"status_code": 409, "message": MENSAJE_CANDIDATO_NO_EXISTE}, 409

        data = request.json
        response = SaveInfoTecnica(
            data['tipo'],
            data['valor'],
            data['id_candidato'],
            )
        return {"id":response.id, "status_code": 201, "message": MENSAJE_CREACION_OK}, 201
    
    @jwt_required()
    def get(self):

        id_candidato = infoTecnica.query.filter(infoTecnica.id_candidato == request.args.get("id_candidato")).all()
        db.session.commit()

        print("El id_candidato es: " + str(id_candidato))

        listOfItems = []
        
        for infoTecnica_item in id_candidato:
            infoTecnicaFormat = {"tipo":infoTecnica_item.tipo, "valor":infoTecnica_item.valor, "id_candidato":infoTecnica_item.id_candidato}
            listOfItems.append(infoTecnicaFormat)

        return {"response":listOfItems, "status_code": 200}

class VistaConsultarCandidato(Resource):

    @jwt_required()
    def get(self):

        if request.args.get('id_candidato') is None:
            return {"status_code": 400, "message": "Debe ingresar el id del candidato"}, 400

        #Get id from params and query from db to save it
        id_candidato = candidato.query.filter(candidato.id == request.args.get("id_candidato")).first()
        db.session.commit()

        print ("id_candidato" + str(id_candidato))

        #Get info candidate from db
        candidatoItems = [elem.__dict__ for elem in db.session.query(candidato).filter(candidato.id == id_candidato.id).all()]

        infoCandidatoResponse = {"tipo_doc":candidatoItems[0]['tipo_doc'], "num_doc":candidatoItems[0]['num_doc'], "nombre":candidatoItems[0]['nombre'],
                                 "usuario":candidatoItems[0]['usuario'], "clave":candidatoItems[0]['clave'], "telefono":candidatoItems[0]['telefono'],
                                 "email":candidatoItems[0]['email'], "pais":candidatoItems[0]['pais'], "ciudad":candidatoItems[0]['ciudad'],
                                 "aspiracion_salarial":candidatoItems[0]['aspiracion_salarial'], "fecha_nacimiento":str(candidatoItems[0]['fecha_nacimiento']),
                                 "idiomas":candidatoItems[0]['idiomas']}

        return {"response":infoCandidatoResponse, "status_code": 200}


class VistaConsultarCandidatosDisponibles(Resource):
    
    @jwt_required()
    def get(self):

        candidatos = candidato.query.filter(candidato.estado == "DISPONIBLE").all()
        db.session.commit()
        
        if candidatos is not None and len(candidatos) > 0:
            resultado = candidato_schema.dump(candidatos)
            return {"status_code": 200, "candidatos": resultado}, 200
        else:
            return {"status_code": 404, "message": "No se encontraron candidatos disponibles"}, 404

class VistaResultadosEntrevistas(Resource):

    @jwt_required()
    def get(self):
        #Check for required values not be empty
        if request.args.get('tipo_doc') is None:
            return {"status_code": 400, "message": "Debe ingresar el tipo de doc del candidato"}, 400
        elif request.args.get('num_doc') is None:
            return {"status_code": 400, "message": "Debe ingresar el doc del candidato"}, 400
        elif request.args.get('id_empresa') is None:
            return {"status_code": 400, "message": "Debe ingresar el id de la empresa"}, 400
        
        #Get id from params
        entrevistas_candidato = entrevista.query.filter(candidato.tipo_doc == request.args.get("tipo_doc"), candidato.num_doc == request.args.get("num_doc")).all()
        db.session.commit()

        if entrevistas_candidato == []:
            return {"status_code": 409, "message": "No existen datos para el documento ingresado"}, 409
        
        nombre_candidato = candidato.query.filter(candidato.tipo_doc == request.args.get("tipo_doc")
                                                          and candidato.num_doc == request.args.get("num_doc")).first()
        

        listOfItems = []

        for infoEntrevista_item in entrevistas_candidato:
                if str(infoEntrevista_item.id_empresa) == request.args.get("id_empresa") and infoEntrevista_item.estado.lower() == "finalizada":
                    infoEntrevista = {"id_entrevista":infoEntrevista_item.id, "nombre_entrevista":infoEntrevista_item.nombre_entrevista,
                                      "fecha":infoEntrevista_item.fecha, "nombre_candidato":nombre_candidato.nombre, "resultado":infoEntrevista_item.resultado}
                    listOfItems.append(infoEntrevista)

        if listOfItems == []:
            return {"status_code": 200, "message":"El candidato seleccionado no tiene entrevistas finalizadas"}, 200
        
        else:
            return {"message":listOfItems, "status_code": 200}        
   

class VistaInformacionLaboral(Resource):

    @jwt_required()
    def post(self):

        cargo = request.json.get("cargo")
        ano_inicio = request.json.get("ano_inicio")
        ano_fin = request.json.get("ano_fin")
        empresa = request.json.get("empresa")
        descripcion = request.json.get("descripcion")
        id_candidato = request.json.get("id_candidato")

        if cargo is None or ano_inicio is None or ano_inicio is None or ano_fin is empresa or id_candidato is None:
            return {"status_code": 400, "message": MENSAJE_TODOS_DATOS}, 400
        
        elif cargo == "" or ano_inicio == "" or ano_fin == "" or empresa == "" or id_candidato == "":
            return {"status_code": 400, "message": MENSAJE_CAMPO_VACIO}, 400
        
        candidato_id = candidato.query.filter(candidato.id == id_candidato).first()
        db.session.commit()

        if candidato_id is None:
            return {"status_code": 409, "message": MENSAJE_CANDIDATO_NO_EXISTE}, 409

        response = save_info_laboral(
            cargo,
            ano_inicio,
            ano_fin,
            empresa,
            descripcion if descripcion is not None else "",
            id_candidato
            )
        return {"id":response.id, "status_code": 201, "message": MENSAJE_CREACION_OK}, 201
    
    @jwt_required()
    def get(self):

        info_laboral_candidato = infoLaboral.query.filter(infoLaboral.id_candidato == request.args.get("id_candidato")).all()
        db.session.commit()

        if info_laboral_candidato is None or len(info_laboral_candidato) == 0:
            return {"status_code": 404, "message": "No se encontró información laboral para el candidato"}, 404

        list_of_items = []
        
        for info_laboral_item in info_laboral_candidato:
            info_laboral_format = {"cargo":info_laboral_item.cargo, "ano_inicio":info_laboral_item.ano_inicio, "ano_fin":info_laboral_item.ano_fin, "empresa":info_laboral_item.empresa, "descripcion":info_laboral_item.descripcion}
            list_of_items.append(info_laboral_format)

        return {"response":list_of_items, "status_code": 200}

class VistaConsultarPruebas(Resource):

    @jwt_required()
    def get(self, doc_empleado):
        print("doc_empleado")
        print(doc_empleado)
        
        candid = candidato.query.filter(candidato.num_doc == doc_empleado).first()
        if candid is None:
            return {"status_code": 404, "message": "Candidato no encontrado"}, 404

        pruebas = ResultadoPruebaTecnica.query.filter(ResultadoPruebaTecnica.candidato_id == candid.id).all()

        if pruebas is not None and len(pruebas)>0:
            return {"status_code": 200, "pruebas": resultadoPruebaTecnica_schema.dump(pruebas)}, 200
        else:
            return make_response('',204)
        
#Vista que guarda la información técnica de un candidato
class VistaInformacionAcademica(Resource):

    @jwt_required()
    def post(self):
        
        institucion = request.json.get("institucion")
        titulo = request.json.get("titulo")
        fecha_inicio = request.json.get("fecha_inicio")
        fecha_fin = request.json.get("fecha_fin")
        id_candidato = request.json.get("id_candidato")

        if institucion is None or titulo is None or fecha_inicio is None or fecha_fin is None or id_candidato is None:
            return {"status_code": 400, "message": MENSAJE_TODOS_DATOS}, 400
        
        elif institucion == "" or titulo == "" or fecha_inicio == "" or fecha_fin == "" or id_candidato == "":
            return {"status_code": 400, "message": MENSAJE_CAMPO_VACIO}, 400
        
        candidato_id = candidato.query.filter(candidato.id == id_candidato).first()
        db.session.commit()

        if candidato_id is None:
            return {"status_code": 409, "message": MENSAJE_CANDIDATO_NO_EXISTE}, 409


        new_infoAcademica = infoAcademica(
            institucion = request.json.get("institucion"),
            titulo = request.json.get("titulo"),
            fecha_inicio = request.json.get("fecha_inicio"),
            fecha_fin = request.json.get("fecha_fin"),
            id_candidato = request.json.get("id_candidato"),
        )
        
        db.session.add(new_infoAcademica)
        db.session.commit()
        return {"id":new_infoAcademica.id, "status_code": 201, "message": MENSAJE_CREACION_OK}, 201
    
    
    @jwt_required()
    def get(self):
        
        id_candidato = request.args.get("id_candidato")

        if id_candidato is None:
            return {"status_code": 400, "message": MENSAJE_TODOS_DATOS}, 400
        
        elif id_candidato == "":
            return {"status_code": 400, "message": MENSAJE_CAMPO_VACIO}, 400
        
        candidate = candidato.query.filter(candidato.id == id_candidato).first()
        db.session.commit()

        if candidate is None:
            return {"status_code": 409, "message": MENSAJE_CANDIDATO_NO_EXISTE}, 409



        infoAcademicaList = infoAcademica.query.filter(infoAcademica.id_candidato == id_candidato).all()
        db.session.commit()

        listOfItems = []
        
        for infoAcademica_item in infoAcademicaList:
            infoAcademicaFormat = {"institucion":infoAcademica_item.institucion, 
                                   "titulo":infoAcademica_item.titulo, 
                                   "fecha_inicio":infoAcademica_item.fecha_inicio, 
                                   "fecha_fin":infoAcademica_item.fecha_fin, 
                                   "id_candidato":infoAcademica_item.id_candidato}
            listOfItems.append(infoAcademicaFormat)
        return {"response":listOfItems, "status_code": 200}

class ping(Resource):
    
    def get(self):
        return "pong", 200