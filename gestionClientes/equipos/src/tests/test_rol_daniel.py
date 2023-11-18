# import json
# from unittest import TestCase
# import mysql.connector
# from faker import Faker
# from flask_jwt_extended import create_access_token
# from app import app, sqlpass, test


# class TestRol(TestCase):

#     def setUp(self):
#         self.client = app.test_client()
#         self.data_factory = Faker()
#         self.token_de_acceso = create_access_token(identity=123)
#         self.headers ={'Content-Type': 'application/json',
#                        "Authorization" : "Bearer "+str(self.token_de_acceso)}
    
#     def test_1_detallar_rol_OK(self):
#         post_request = self.client.put("/equipos/rol", 
#         json={
#             "id_rol":1,
#             "titulo_rol":"rol prueba",
#             "descripcion_rol":"descripcion prueba 1",
#             "lista_habilidades_blandas":[1],
#             "lista_habilidades_tecnicas":[2]
#         },headers=self.headers)
#         self.assertEqual(post_request.status_code, 200)

#     def test_2_detallar_rol_400(self):
#         post_request = self.client.put("/equipos/rol",
#         json={
#             "id_rol":1,
#             "titulo_rol":"rol prueba",
#             "descripcion_rol":"descripcion prueba 1",
#             "lista_habilidades_blandas":[1]
#         },headers=self.headers)
#         self.assertEqual(post_request.status_code, 400)
        
#     def test_3_detallar_rol_404_rol_no_encontrado(self):
#         post_request = self.client.put("/equipos/rol", 
#         json={
#             "id_rol":-1,
#             "titulo_rol":"rol prueba",
#             "descripcion_rol":"descripcion prueba 1",
#             "lista_habilidades_blandas":[1],
#             "lista_habilidades_tecnicas":[2]
#         },headers=self.headers)
#         self.assertEqual(post_request.status_code, 404)
        
#     def test_4_detallar_rol_404_habilidad_blanda_no_encontrada(self):
#         post_request = self.client.put("/equipos/rol", 
#         json={
#             "id_rol":1,
#             "titulo_rol":"rol prueba",
#             "descripcion_rol":"descripcion prueba 1",
#             "lista_habilidades_blandas":[1058],
#             "lista_habilidades_tecnicas":[2]
#         },headers=self.headers)
#         self.assertEqual(post_request.status_code, 404)
        
#     def test_5_detallar_rol_404_habilidad_tecnica_no_encontrada(self):
#         post_request = self.client.put("/equipos/rol", 
#         json={
#             "id_rol":1,
#             "titulo_rol":"rol prueba",
#             "descripcion_rol":"descripcion prueba 1",
#             "lista_habilidades_blandas":[1],
#             "lista_habilidades_tecnicas":[1058]
#         },headers=self.headers)
#         self.assertEqual(post_request.status_code, 404)
       
#     def test_6_obtener_habilidades(self):
#         get_request = self.client.get("/equipos/habilidad", 
#         json={},headers=self.headers)
#         self.assertEqual(get_request.status_code, 200)
                
#     def tearDown(self) -> None:
#         return super().tearDown()