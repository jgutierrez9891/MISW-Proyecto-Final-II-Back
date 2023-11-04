from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from modelos.modelos import db
from vistas.vistas import (VistaAsociarEquipoRol, VistaConsultarFichas, VistaConsultarProyectos, VistaConsultarRol, VistaCrearProyecto, ping)
from vistas.vistas import (VistaActualizarRol, VistaConsultarFichas, VistaCrearProyecto, ping)
import os
sqlpass = os.getenv("SQL_PASSWORD")
if sqlpass is None:
    sqlpass = ''
test = os.getenv('IF_TEST')
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "http://localhost:4201", "http://localhost:8000", "https://micro-web-kdbo2knypq-uc.a.run.app", "http://localhost", "https://localhost"])

if(os.path.isdir('/cloudsql/')):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+sqlpass+'@/empresas?unix_socket=/cloudsql/proyecto-final-01-399101:us-central1:abcjobs'
else:
    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+sqlpass+'@34.27.118.190:3306/empresas'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1440)

app_context = app.app_context()
app_context.push()

db.init_app(app)

api = Api(app)
api.add_resource(VistaCrearProyecto, '/proyecto/crear')
api.add_resource(VistaConsultarFichas, '/equipos/consultar')
api.add_resource(VistaConsultarProyectos, '/proyectos/consultar')
api.add_resource(VistaActualizarRol, '/equipos/rol')
api.add_resource(VistaConsultarRol, '/equipos/rol')
api.add_resource(VistaAsociarEquipoRol, '/equipos/rol/asociar')
api.add_resource(ping, '/equipos/ping')

jwt = JWTManager(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8083))
    app.run(debug=True, host='0.0.0.0', port=port)
    