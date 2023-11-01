from flask import json, request
from flask_restful import Resource
from modelos.modelos import Ficha_trabajoSchema, Hoja_trabajo, ProyectoSchema, db, Proyecto, Ficha_trabajo
from flask_jwt_extended import jwt_required

ficha_schema = Ficha_trabajoSchema()
proyectos_schema = ProyectoSchema(many=True)
    
class VistaCrearProyecto(Resource):

    @jwt_required()
    def post(self):
        empresa_id = request.json.get("id_empresa")
        proyecto_titulo = request.json.get("titulo")
        proyecto_fecha_inicio = request.json.get("fecha_inicio")
        proyecto_fecha_fin = request.json.get("fecha_fin")
        proyecto_equipos = request.json.get("equipos")

        if empresa_id is None or empresa_id is None or proyecto_titulo is None or proyecto_titulo is None or proyecto_fecha_inicio is None or proyecto_fecha_inicio is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar todos los datos de la empresa y representante"}, 400
        
        if proyecto_fecha_fin:
            if proyecto_fecha_fin < proyecto_fecha_inicio:
                return {"status_code": 400, "message": "La fecha de finalización del proyecto no puede ser menor a la fecha de inicio"}, 400
        
        if proyecto_equipos is not None and len(proyecto_equipos) > 0: 
            for equipo in proyecto_equipos:
                if "id" not in equipo or equipo["id"] is None:
                    return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar todos los datos de los equipos"}, 400
                else:
                    equipo_tmp = Ficha_trabajo.query.filter(Ficha_trabajo.id == equipo["id"]).first()
                    db.session.commit()
                    if(equipo_tmp is None):
                        return {"status_code": 400, "message": "El equipo con id "+str(equipo["id"])+" no existe"}, 400
        
        proyecto_actual = Proyecto.query.filter(Proyecto.titulo == proyecto_titulo, Proyecto.id_empresa == empresa_id).first()
        db.session.commit()
        if proyecto_actual is not None:
            return {"status_code": 409, "message": "El proyecto ingresado ya existe"}, 409
        
        proyecto = Proyecto(titulo = proyecto_titulo,
                            fecha_inicio = proyecto_fecha_inicio,
                            fecha_fin = proyecto_fecha_fin,
                            id_empresa = empresa_id)
        
        try:
            db.session.add(proyecto)
            db.session.commit()
        except Exception as err:
            print("VA A RETORNAR 500 POR ERROR: "+str(err))
            return {"status_code": 500, "message": "Error creando proyecto"}, 500
        
        proyecto = Proyecto.query.filter(Proyecto.titulo == proyecto_titulo, Proyecto.id_empresa == empresa_id).first();
        db.session.commit()

        try:
            if proyecto_equipos is not None:
                for equipo in proyecto_equipos:
                    equipo_tmp = Ficha_trabajo.query.filter(Ficha_trabajo.id == equipo["id"]).first()
                    db.session.commit()
                    equipo_tmp.id_proyecto = proyecto.id
                    db.session.commit()
        except Exception as err:
            print("VA A RETORNAR 500 POR ERROR: "+str(err))
            return {"status_code": 500, "message": "Error asignando proyectos"}, 500

        return {"status_code": 200, "message": "Proyecto creado satisfactoriamente"}, 200

class VistaConsultarFichas(Resource):

    @jwt_required()
    def get(self):
        empresa_id = request.args.get("id_empresa")

        if empresa_id is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar el id de la empresa"}, 400
        
        fichas = Ficha_trabajo.query.filter(Ficha_trabajo.id_empresa == empresa_id).all()
        db.session.commit()
        
        if fichas is not None and len(fichas) > 0:
            fichas_list = []
            for ficha in fichas:
                fichas_list.append(ficha_schema.dump(ficha))
            return {"status_code": 200, "fichas": fichas_list}, 200
        else:
            return {"status_code": 204, "message": "No se encontraron fichas de trabajo para la empresa con id "+str(empresa_id)}, 204

class VistaConsultarProyectos(Resource):

    @jwt_required()
    def get(self):
        empresa_id = request.args.get("id_empresa")

        if empresa_id is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar el id de la empresa"}, 400
        
        proyectos = Proyecto.query.filter(Proyecto.id_empresa == empresa_id).all()
        db.session.commit()
        
        if proyectos is not None and len(proyectos) > 0:
            resultado = proyectos_schema.dump(proyectos)
            return {"status_code": 200, "proyectos": resultado}, 200
        else:
            return {"status_code": 404, "message": "No se encontraron registros para la empresa con id "+str(empresa_id)}, 404
        
        
class ping(Resource):
    
    def get(self):
        return "pong", 200
        