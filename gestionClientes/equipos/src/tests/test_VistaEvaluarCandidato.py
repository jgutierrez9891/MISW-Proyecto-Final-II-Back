# from datetime import datetime
# import json
# from unittest import TestCase
# from flask_jwt_extended import create_access_token
# from app import app, sqlpass, test
# import mysql.connector

# class TestVistaEvaluarCandidato(TestCase):

#     def setUp(self):
#         if test:
#             app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
#             self.connection = mysql.connector.connect(host='0.0.0.0',
#             database='candidatos',
#             user='root',
#             password='root')
#             self.connection = mysql.connector.connect(host='0.0.0.0',
#             database='empleados',
#             user='root',
#             password='root')
#             self.connection = mysql.connector.connect(host='0.0.0.0',
#             database='empresas',
#             user='root',
#             password='root')

#         else:
#             self.connection = mysql.connector.connect(host='34.27.118.190',
#             database='candidatos',
#             user='root',
#             password=sqlpass)
    
#         self.client = app.test_client()
#         self.token_de_acceso = create_access_token(identity=123)
#         self.headers ={'Content-Type': 'application/json',
#                        "Authorization" : "Bearer "+str(self.token_de_acceso)}

#     # def tearDown(self):


#     def test_post_evaluar_candidato_success(self):
#         data = {
#             "evaluacion": "Good",
#             "puntaje": 90
#         }
#         response = self.client.post('/proyectos/evaluacion/31', data=json.dumps(data), headers=self.headers)
#         self.assertEqual(response.status_code, 201)
#         data = json.loads(response.data)
#         self.assertEqual(data['status_code'], 201)
#         self.assertEqual(data['candidatos'], 31)

#     def test_post_evaluar_candidato_candidato_not_found(self):
#         data = {
#             "evaluacion": "Good",
#             "puntaje": 90
#         }
#         response = self.client.post('/proyectos/evaluacion/200004', data=json.dumps(data), headers=self.headers)
#         self.assertEqual(response.status_code, 404)
#         data = json.loads(response.data)
#         self.assertEqual(data['status_code'], 404)
#         self.assertEqual(data['message'], 'No se encontró el candidato')


