import json
import datetime
from unittest import TestCase
import mysql.connector
from faker import Faker
from app import app, sqlpass, test


class TestRegistro(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        self.datos_registro_OK = {
            "empresa_tipo_doc": "NIT",
            "empresa_num_doc": str(self.data_factory.random_int(min=111111, max=999999)),
            "empresa_nombre": self.data_factory.company(),
            "empresa_email": self.data_factory.email(),
            "empresa_telefono": self.data_factory.phone_number(),
            "representante_tipo_doc": "CC",
            "representante_num_doc": str(self.data_factory.random_int(min=111111, max=999999)),
            "representante_nombre": self.data_factory.first_name()+' '+self.data_factory.last_name(),
            "representante_email": self.data_factory.email(),
            "representante_telefono": self.data_factory.phone_number(),
            "representante_usuario": self.data_factory.first_name()+'.'+self.data_factory.last_name(),
            "representante_clave": self.data_factory.first_name()+str(self.data_factory.random_int(min=100, max=999))
        }
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
        
    def tearDown(self) -> None:
        sql = "DELETE FROM empresas.representante WHERE usuario=%s"
        val = (self.datos_registro_OK["representante_usuario"], )
        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.empresa WHERE tipo_doc=%s and num_doc=%s"
        val = ("NIT", self.datos_registro_OK["empresa_num_doc"], )
        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

        return super().tearDown()

    def test_1_registro_OK(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 200)
        self.assertEqual(respuesta_registro["message"], "Empresa y representante creados exitosamente")
    
    def test_2_registro_ERROR_email_empresa(self):
        self.datos_registro_OK["empresa_email"] = self.data_factory.company()
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 400)
        self.assertEqual(respuesta_registro["message"], "El formato del correo de empresa es inválido")
    
    def test_3_registro_ERROR_email_representante(self):
        self.datos_registro_OK["representante_email"] = self.data_factory.company()
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 400)
        self.assertEqual(respuesta_registro["message"], "El formato del correo de representante es inválido")
    
    def test_4_registro_ERROR_empresa_existe(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 409)
        self.assertEqual(respuesta_registro["message"], "La empresa ingresada ya existe")
    
    def test_5_registro_ERROR_correo_empresa_existe(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        self.datos_registro_OK["empresa_tipo_doc"] = "RUT"
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 409)
        self.assertEqual(respuesta_registro["message"], "El correo de empresa ingresado ya existe")

    def test_6_registro_ERROR_representante_existe(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        self.datos_registro_OK["empresa_tipo_doc"] = "RUT"
        self.datos_registro_OK["empresa_email"] = self.data_factory.email()
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 409)
        self.assertEqual(respuesta_registro["message"], "El representante ingresado ya existe")
    
    def test_7_registro_ERROR_correo_representante_existe(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        self.datos_registro_OK["empresa_tipo_doc"] = "RUT"
        self.datos_registro_OK["empresa_email"] = self.data_factory.email()
        self.datos_registro_OK["representante_tipo_doc"] = "PAS"
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 409)
        self.assertEqual(respuesta_registro["message"], "El correo de representante ingresado ya existe")
    
    def test_8_registro_ERROR_usuario_existe(self):
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        self.datos_registro_OK["empresa_tipo_doc"] = "RUT"
        self.datos_registro_OK["empresa_email"] = self.data_factory.email()
        self.datos_registro_OK["representante_tipo_doc"] = "PAS"
        self.datos_registro_OK["representante_email"] = self.data_factory.email()
        solicitud_registro = self.client.post("/empresa/registro",
                            data=json.dumps(self.datos_registro_OK),
                            headers={'Content-Type': 'application/json'})
        respuesta_registro = json.loads(solicitud_registro.get_data())
        self.assertEqual(solicitud_registro.status_code, 409)
        self.assertEqual(respuesta_registro["message"], "El usuario ingresado ya existe")