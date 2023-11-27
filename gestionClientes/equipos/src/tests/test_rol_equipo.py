import json
from unittest import TestCase
from flask_jwt_extended import  create_access_token
from app import db, app, sqlpass, test
import mysql.connector

class TestRolEquipo(TestCase):

    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empleados',
            user='root',
            password='root')

        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='candidatos',
            user='root',
            password=sqlpass)
    
        self.client = app.test_client()
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}

        sql_crear = "INSERT INTO empresas.empresa (id, tipo_doc, num_doc, nombre, email, telefono) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (101, "Test", "Test", "Test", "Test", "Test")
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) VALUES (%s, %s, %s, %s)"
        val = (401, "Ficha 4", "Ficha 4", 101)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) VALUES (%s, %s, %s, %s)"
        val = (101, "Ficha 4", "Ficha 4", 101)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

    def tearDown(self):
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo=1 AND id_rol=2"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo in(401,101)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.ficha_trabajo WHERE id_empresa=101"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.empresa WHERE id=101"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        return super().tearDown()

    def test_1_detallar_rol_OK(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)

    def test_2_detallar_rol_400(self):
        post_request = self.client.put("/equipos/rol",
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        
    def test_3_detallar_rol_404_rol_no_encontrado(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":-1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
        
    def test_4_detallar_rol_404_habilidad_blanda_no_encontrada(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1058],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
        
    def test_5_detallar_rol_404_habilidad_tecnica_no_encontrada(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[1058]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
       
    def test_6_obtener_habilidades(self):
        get_request = self.client.get("/equipos/habilidad", 
        json={},headers=self.headers)
        self.assertEqual(get_request.status_code, 200)

    def test_7_add_rol_to_equipo_success(self):
        data = {"id_rol": 4, "id_equipo": 401}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers ,data=json.dumps(data),
                                 content_type='application/json')
        #print(json.loads(response.data)["message"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol asociado con Éxito")

    # def test_add_rol_to_equipo_duplicate(self):
    #     data = {"id_rol": 5, "id_equipo": 401}
    #     response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
    #     self.assertEqual(response.status_code, 409)

    def test_8_add_rol_to_equipo_missing_data(self):
        data = {"id_rol": 1} 
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_9_add_rol_to_equipo_rol_not_found(self):
        data = {"id_rol": 300, "id_equipo": 101}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_10_add_rol_to_equipo_equipo_not_found(self):
        data = {"id_rol": 1, "id_equipo": 300}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_11_delete_rol_from_equipo_success(self):
        data = {"id_rol": 4, "id_equipo": 101}
        self.client.post("/equipos/rol/asociar",headers=self.headers ,data=json.dumps(data),
                                 content_type='application/json')
        params = {"id_rol": 4, "id_equipo": 101}
        response = self.client.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        #print(json.loads(response.data)["message"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol desasociado con Éxito")

    def test_12_delete_rol_from_equipo_not_found(self):
        params = {"id_rol": 300, "id_equipo": 101}
        response = self.client.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_13_delete_rol_from_equipo_missing_params(self):
        response = self.client.delete("/equipos/rol/asociar",headers=self.headers)
        self.assertEqual(response.status_code, 400)
