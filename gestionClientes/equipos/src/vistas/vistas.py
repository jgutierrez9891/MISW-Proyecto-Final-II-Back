from flask import json, request
from flask_restful import Resource
from modelos.modelos import Candidatos_hoja_trabajo, Empleado, Empleado_evaluacion, Empleado_ficha_trabajo, EmpleadoSchema, Hoja_trabajo, Rol, Habilidad, Rol_ficha_trabajo, RolHabilidad, Ficha_trabajoSchema, ProyectoSchema, RolSchema, db, Proyecto, Ficha_trabajo
from flask_jwt_extended import jwt_required

ficha_schema = Ficha_trabajoSchema()
empleado_schema = EmpleadoSchema()
rol_schema = RolSchema()
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
        
        if proyecto_fecha_fin and proyecto_fecha_fin != "":
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
        
        if(proyecto_fecha_fin is None or proyecto_fecha_fin == ""):
            proyecto_fecha_fin = None
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
                empleado_count = Empleado_ficha_trabajo.query.filter(Empleado_ficha_trabajo.id_ficha_trabajo == ficha.id).count()
                ficha_data = ficha_schema.dump(ficha)
                ficha_data['miembros'] = empleado_count
                fichas_list.append(ficha_data)
            return {"status_code": 200, "fichas": fichas_list}, 200
        else:
            return {"status_code": 204, "message": "No se encontraron fichas de trabajo para la empresa con id "+str(empresa_id)}, 204
class VistaConsultarRol(Resource):

    @jwt_required()
    def get(self):
        id_equipo = request.args.get("equipo_id")

        if id_equipo is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar el id del equipo"}, 400
        
        roles_equipo = Rol_ficha_trabajo.query.filter(Rol_ficha_trabajo.id_ficha_trabajo == id_equipo).all()

        roles = Rol.query.all()
        db.session.commit()
        
        if roles is not None and len(roles) > 0:
            roles_list = []
            for rol in roles:
                rol_data = rol_schema.dump(rol)
                is_included = any(rol.id_rol == r.id_rol for r in roles_equipo)
                rol_data['is_included'] = is_included
                roles_list.append(rol_data)
            return {"status_code": 200, "roles": roles_list}, 200
        else:
            return {"status_code": 204, "message": "No se encontraron roles para el equipo con id "+str(id_equipo)}, 204

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
        
        
        
class VistaActualizarRol(Resource):
    
    @jwt_required()
    def put(self):
        
        id_rol = request.json.get("id_rol")
        titulo_rol = request.json.get("titulo_rol")
        descripcion_rol = request.json.get("descripcion_rol")
        lista_habilidades_blandas = request.json.get("lista_habilidades_blandas")
        lista_habilidades_tecnicas = request.json.get("lista_habilidades_tecnicas")

        if id_rol is None or titulo_rol is None or descripcion_rol is None or lista_habilidades_blandas is None or lista_habilidades_tecnicas is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar los datos esperados"}, 400
        
        rol = Rol.query.filter(Rol.id_rol == id_rol).first()
        
        if rol is None:
            return {"status_code": 404, "message": "No se encontro el Rol Esperado"}, 404
                
        for id in lista_habilidades_blandas:
            idt = Habilidad.query.filter(Habilidad.id_habilidad == id).first()
            if idt is None:
                return {"status_code": 404, "message": "No se encontro una de las habilidades Esperadas"}, 404
            
        for id in lista_habilidades_tecnicas:
            idt = Habilidad.query.filter(Habilidad.id_habilidad == id).first()
            if idt is None:
                return {"status_code": 404, "message": "No se encontro una de las habilidades Esperadas"}, 404
            
        deleteHabilidadRol = RolHabilidad.query.filter(RolHabilidad.id_rol == id_rol).delete()
        
        for id in lista_habilidades_blandas:
            habilidad = RolHabilidad(id_rol = id_rol,
                                      id_habilidad = id)
            db.session.add(habilidad)
            
        for id in lista_habilidades_tecnicas:
            habilidad = RolHabilidad(id_rol = id_rol,
                                      id_habilidad = id)
            db.session.add(habilidad)
        
        rol_updating = Rol.query.filter(Rol.id_rol == id_rol).first()
        rol_updating.nombre = titulo_rol
        rol_updating.descripcion = descripcion_rol
        db.session.commit()
    
        return {"status_code": 200, "Mensaje": "Rol Actualizado con Exito"}, 200

class VistaAsociarEquipoRol(Resource):

    def _get_rol_and_equipo(self, idRol, id_equipo):
        rol = Rol.query.filter(Rol.id_rol == idRol).first()
        equipo = Ficha_trabajo.query.filter(Ficha_trabajo.id == id_equipo).first()
        return rol, equipo

    def _perform_operation(self, idRol, id_equipo, operation):
        if idRol is None or id_equipo is None:
            return {"status_code": 400, "message": "Información incompleta. Asegúrese de enviar los datos esperados"}, 400

        rol, equipo = self._get_rol_and_equipo(idRol, id_equipo)

        if rol is None:
            return {"status_code": 404, "message": "No se encontró el Rol esperado"}, 404

        if equipo is None:
            return {"status_code": 404, "message": "No se encontró el equipo esperado"}, 404

        rol_ficha = Rol_ficha_trabajo.query.filter(Rol_ficha_trabajo.id_rol == idRol, Rol_ficha_trabajo.id_ficha_trabajo == id_equipo).first()

        if operation == 'add':
            if rol_ficha is not None:
                return {"status_code": 409, "message": "Rol ya está asociado a equipo"}, 409
            try:
                db.session.add(Rol_ficha_trabajo(id_ficha_trabajo=id_equipo, id_rol=idRol))
                db.session.commit()
                return {"status_code": 200, "Mensaje": "Rol asociado con Éxito"}, 200
            except Exception as err:
                print("VA A RETORNAR 500 POR ERROR: " + str(err))
                return {"status_code": 500, "message": "Error asociando el rol al equipo"}, 500

        elif operation == 'delete':
            if rol_ficha is None:
                return {"status_code": 404, "message": "No se encontró rol asociado a equipo"}, 404
            try:
                db.session.delete(rol_ficha)
                db.session.commit()
                return {"status_code": 200, "Mensaje": "Rol desasociado con Éxito"}, 200
            except Exception as err:
                print("VA A RETORNAR 500 POR ERROR: " + str(err))
                return {"status_code": 500, "message": "Error desasociando el rol del equipo"}, 500

    @jwt_required()
    def post(self):
        idRol = request.json.get("id_rol")
        id_equipo = request.json.get("id_equipo")
        return self._perform_operation(idRol, id_equipo, 'add')

    @jwt_required()
    def delete(self):
        idRol = request.args.get("id_rol")
        id_equipo = request.args.get("id_equipo")
        return self._perform_operation(idRol, id_equipo, 'delete')

    
class VistaConsultarHabilidades(Resource):
    
    @jwt_required()
    def get(self):
        
        habilidades = Habilidad.query.filter().all()
        habilidad_list = []
        for habilidad in habilidades:
            habilidadTmp = {
                "id_habilidad":habilidad.id_habilidad,
                "habilidad":habilidad.habilidad,
                "tipo":habilidad.tipo
            }
            habilidad_list.append(habilidadTmp)
        return {"status_code": 200, "habilidades": habilidad_list}, 200

class VistaHojasTrabajo(Resource):

    @jwt_required()
    def get(self, id_proyecto):
        # validate existing project
        print('id_proyecto')
        print(id_proyecto)
        proyecto = Proyecto.query.filter(Proyecto.id == id_proyecto).first()
        if proyecto is None:
            return {"status_code": 404, "message": "No se encontró el proyecto"}, 404
        hojasDetrabajo = Hoja_trabajo.query.filter(Hoja_trabajo.id_proyecto== id_proyecto).all()
        hojasTmp =[]
        for hoja in hojasDetrabajo:
            hojadTmp = {
                "id":hoja.id,
                "nombre_trabajo":hoja.nombre_trabajo,
                "descripcion_candidato_ideal":hoja.descripcion_candidato_ideal
            }
            hojasTmp.append(hojadTmp)
        return {"status_code": 200, "hojasDetrabajo": hojasTmp}, 200
class VistaCandidatosHojas(Resource):

    @jwt_required()
    def get(self, id_proyecto, id_hoja):
        print('id_hoja')
        print(id_hoja)
        hoja = Hoja_trabajo.query.filter(Hoja_trabajo.id == id_hoja).first()
        if hoja is None:
            return {"status_code": 404, "message": "No se encontró la hoja de trabajo"}, 404

        candidatos_hoja = Candidatos_hoja_trabajo.query.filter(Candidatos_hoja_trabajo.id_hoja_trabajo == id_hoja).all()
        candidatosTmp = []

        for ch in candidatos_hoja:
            candidato = Empleado.query.filter(Empleado.id == ch.id_candidato).first()
            if candidato is not None:
                habilidades_list = [h.to_dict() for h in candidato.habilidades]
                
                candTmp = empleado_schema.dump(candidato)
                candTmp["habilidades"] = habilidades_list
                candidatosTmp.append(candTmp)

        return {"status_code": 200, "candidatos": candidatosTmp}, 200
    
class VistaEvaluarCandidato(Resource):

    @jwt_required()
    def post(self, id_candidato):
        print('id_candidato')
        print(id_candidato)
        candidato = Empleado.query.filter(Empleado.id == id_candidato).first()
        if candidato is None:
            return {"status_code": 404, "message": "No se encontró el candidato"}, 404

        evaluaciontext = request.json.get("evaluacion")
        puntajejson = request.json.get("puntaje")
        evaluacion = Empleado_evaluacion( evaluacion= evaluaciontext,
                                         puntaje = puntajejson,
                                         empleado_id= id_candidato
                                         )
        print("json content")
        print(evaluacion)
        print(puntajejson)

        db.session.add(evaluacion)
        db.session.commit()
        return {"status_code": 201, "candidatos": id_candidato}, 201

    

        
        
class ping(Resource):
    
    def get(self):
        return "pong", 200
        