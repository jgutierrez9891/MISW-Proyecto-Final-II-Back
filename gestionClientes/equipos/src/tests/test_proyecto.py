import json
from datetime import datetime, timedelta
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test


class TestProyecto(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='empresas',
            user='root',
            password=sqlpass)

        sql = "insert into empresas.representante (tipo_doc, num_doc, nombre, email, telefono, usuario, clave, id_empresa) values ('CC','1023456789','Mauricio Peña', 'mauricio.pena@softwareia.com', '3123456789','maupena', 'miclave123', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo in(1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.empleado_ficha_trabajo WHERE id_ficha_trabajo in (1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.ficha_trabajo WHERE id in (1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        # sql = "DELETE FROM empresas.proyecto WHERE id in(1,2)"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        # sql = "insert into empresas.proyecto (id, titulo, fecha_inicio, fecha_fin, id_empresa) values (1, '"+self.data_factory.company()+"', '2023-01-01', '2023-01-30', 1);"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        # sql = "insert into empresas.proyecto (id, titulo, fecha_inicio, fecha_fin, id_empresa) values (2, '"+self.data_factory.company()+"', '2023-02-01', '2023-03-30', 1);"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        sql = "DELETE FROM empresas.candidatos_hoja_trabajo WHERE id_hoja_trabajo in(1,2,3,4)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.hoja_trabajo WHERE id in(1,2,3,4)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (3, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 2);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (4, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 2);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (1, 10);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (1, 20);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (2, 30);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (2, 40);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.token_de_acceso = create_access_token(identity=123)

        
    def tearDown(self) -> None:
        # sql = "DELETE FROM empresas.ficha_trabajo"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        # sql = "DELETE FROM empresas.candidatos_hoja_trabajo"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        # sql = "DELETE FROM empresas.hoja_trabajo"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        # sql = "DELETE FROM empresas.proyecto"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()
        return super().tearDown()

    def test_0_ping(self):
        solicitud_ping = self.client.get("/equipos/ping",)
        self.assertEqual(solicitud_ping.status_code, 200)
    
    def test_1_crear_proyecto_minimo_OK(self):
        fakeFechaInicio = self.data_factory.date_time_between(datetime.now()+timedelta(hours = 1))
        fecha_inicio = datetime(fakeFechaInicio.year,fakeFechaInicio.month,fakeFechaInicio.day, fakeFechaInicio.hour, fakeFechaInicio.minute, fakeFechaInicio.second) 
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d")
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_creacion = json.loads(solicitud_creacion_proyecto.get_data())
        self.assertEqual(solicitud_creacion_proyecto.status_code, 200)
        self.assertEqual(respuesta_creacion["message"], "Proyecto creado satisfactoriamente")

    def test_2_crear_proyecto_total_OK(self):
        fakeFechaInicio = self.data_factory.date_time_between(datetime.now()+timedelta(hours = 1))
        fecha_inicio = datetime(fakeFechaInicio.year,fakeFechaInicio.month,fakeFechaInicio.day, fakeFechaInicio.hour, fakeFechaInicio.minute, fakeFechaInicio.second) 
        fakeFechaFin= self.data_factory.date_time_between(fakeFechaInicio+timedelta(hours = 1))
        fecha_fin = datetime(fakeFechaFin.year,fakeFechaFin.month,fakeFechaFin.day, fakeFechaFin.hour, fakeFechaFin.minute, fakeFechaFin.second)
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                                        "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                                        "equipos": [
                                            {
                                                "id": 1
                                            },
                                            {
                                                "id": 2
                                            }
                                        ]
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_creacion = json.loads(solicitud_creacion_proyecto.get_data())
        self.assertEqual(solicitud_creacion_proyecto.status_code, 200)
        self.assertEqual(respuesta_creacion["message"], "Proyecto creado satisfactoriamente")

    def test_3_crear_proyecto_ERROR_datos_incompletos(self):
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_creacion = json.loads(solicitud_creacion_proyecto.get_data())
        self.assertEqual(solicitud_creacion_proyecto.status_code, 400)
        self.assertEqual(respuesta_creacion["message"], "Información incompleta. Asegúrese de enviar todos los datos de la empresa y representante")
    
    def test_4_crear_proyecto_ERROR_fechas(self):
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                        "fecha_inicio": "2023-01-01",
                                        "fecha_fin": "2022-01-01",
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_creacion = json.loads(solicitud_creacion_proyecto.get_data())
        self.assertEqual(solicitud_creacion_proyecto.status_code, 400)
        self.assertEqual(respuesta_creacion["message"], "La fecha de finalización del proyecto no puede ser menor a la fecha de inicio")
    
    def test_5_crear_proyecto_ERROR_equipo_no_existe(self):
        fakeFechaInicio = self.data_factory.date_time_between(datetime.now()+timedelta(hours = 1))
        fecha_inicio = datetime(fakeFechaInicio.year,fakeFechaInicio.month,fakeFechaInicio.day, fakeFechaInicio.hour, fakeFechaInicio.minute, fakeFechaInicio.second) 
        fakeFechaFin= self.data_factory.date_time_between(fakeFechaInicio+timedelta(hours = 1))
        fecha_fin = datetime(fakeFechaFin.year,fakeFechaFin.month,fakeFechaFin.day, fakeFechaFin.hour, fakeFechaFin.minute, fakeFechaFin.second)
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                                        "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                                        "equipos": [
                                            {
                                                "id": 1
                                            },
                                            {
                                                "id": 3000
                                            }
                                        ]
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_creacion_proyecto.status_code, 400)

    
    def test_6_crear_proyecto_ERROR_equipo_inconsistente(self):
        fakeFechaInicio = self.data_factory.date_time_between(datetime.now()+timedelta(hours = 1))
        fecha_inicio = datetime(fakeFechaInicio.year,fakeFechaInicio.month,fakeFechaInicio.day, fakeFechaInicio.hour, fakeFechaInicio.minute, fakeFechaInicio.second) 
        fakeFechaFin= self.data_factory.date_time_between(fakeFechaInicio+timedelta(hours = 1))
        fecha_fin = datetime(fakeFechaFin.year,fakeFechaFin.month,fakeFechaFin.day, fakeFechaFin.hour, fakeFechaFin.minute, fakeFechaFin.second)
        datos_creacion_proyecto_OK = {
                                        "id_empresa": 1, 
                                        "titulo": self.data_factory.company(),
                                        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                                        "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                                        "equipos": [
                                            {
                                                "nombre": 1
                                            },
                                            {
                                                "nombre": 2
                                            }
                                        ]
                                    }
        solicitud_creacion_proyecto = self.client.post("/proyecto/crear",
                                        data=json.dumps(datos_creacion_proyecto_OK),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_creacion_proyecto.status_code, 400)
    
    def test_7_consultar_proyectos_OK_con_datos(self):
        solicitud_consulta_proyectos = self.client.get("/proyectos/consultar?id_empresa=1",
                                                       headers={"Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_consulta = json.loads(solicitud_consulta_proyectos.get_data())
        self.assertEqual(solicitud_consulta_proyectos.status_code, 200)
        self.assertGreater(len(respuesta_consulta["proyectos"]), 0)
    
    def test_8_consultar_proyectos_ERROR_sin_datos(self):
        solicitud_consulta_proyectos = self.client.get("/proyectos/consultar?id_empresa=156",
                                                       headers={"Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta_proyectos.status_code, 404)
    
    def test_9_consultar_proyectos_ERROR_sin_parametro(self):
        solicitud_consulta_proyectos = self.client.get("/proyectos/consultar",
                                                       headers={"Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta_proyectos.status_code, 400)