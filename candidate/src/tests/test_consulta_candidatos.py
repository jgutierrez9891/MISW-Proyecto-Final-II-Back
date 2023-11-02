from unittest import TestCase
from faker import Faker
from app import app, sqlpass, test
from modelos import db
import mysql.connector
import random
from flask_jwt_extended import create_access_token

class TestConsultaCandidatos(TestCase):
    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')

        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='candidatos',
            user='root',
            password=sqlpass)
        
        self.client = app.test_client()
        fake = Faker()
        #Token de autenticación
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
        #self.tipo = random.choice(["TECNOLOGIA","LENGUAJE","ROL"])
        self.valor = fake.word()

        #Data para crear usuario de prueba
        self.tipo_doc = random.choice(["cc","ce","pass"])
        self.num_doc = "123456789"
        self.nombre = fake.name()
        self.usuario = fake.lexify(text = '??????')
        self.clave = fake.lexify(text = '??????')
        self.telefono = fake.msisdn()
        self.email = fake.email()
        self.pais = fake.country()
        self.city = fake.city()
        self.aspiracion_salarial = fake.random_number()
        self.fecha_nacimiento = fake.date()
        self.idiomas = random.choice(['español','inglés','alemán','francés','portuges','italiano'])

        sql_crear = "INSERT INTO candidatos.candidato (id,tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (100, self.tipo_doc, self.num_doc, self.nombre, self.usuario, self.clave, self.telefono, self.email, self.pais, self.city, self.aspiracion_salarial, self.fecha_nacimiento, self.idiomas, 'DISPONIBLE')
        #Crear el candidato en BD
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO candidatos.info_tecnica (tipo, valor, id_candidato) VALUES (%s, %s, %s)"
        val = (random.choice(["TECNOLOGIA","LENGUAJE","ROL"]), fake.lexify(text = '??????'), 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO candidatos.info_tecnica (tipo, valor, id_candidato) VALUES (%s, %s, %s)"
        val = (random.choice(["TECNOLOGIA","LENGUAJE","ROL"]), fake.lexify(text = '??????'), 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO candidatos.infoAcademica (tipo, valor, ano_finalizacion, id_candidato) VALUES (%s, %s, %s, %s)"
        val = (random.choice(["UNIVERSITARIA","TECNOLÓGICA","TÉCNICA"]), fake.lexify(text = '??????'), fake.lexify(text = '????'), 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO candidatos.infoAcademica (tipo, valor, ano_finalizacion, id_candidato) VALUES (%s, %s, %s, %s)"
        val = (random.choice(["UNIVERSITARIA","TECNOLÓGICA","TÉCNICA"]), fake.lexify(text = '??????'), fake.lexify(text = '????'), 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()


        self.token_de_acceso = create_access_token(identity=123)
    
    def tearDown(self):
        sql = "DELETE FROM candidatos.info_tecnica"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM candidatos.infoAcademica"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM candidatos.candidato WHERE id = 100"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM candidatos.candidato WHERE estado = 'DISPONIBLE'"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        
    def test_1_consultar_con_datos(self):
        solicitud_consulta_candidatos = self.client.get("/candidatos/disponibles",
                                                       headers={"Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta_candidatos.status_code, 200)
        self.assertGreater(len(solicitud_consulta_candidatos.json["candidatos"]), 0)
