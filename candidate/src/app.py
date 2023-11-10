from flask import Flask
from flask_restful import Api
from modelos import db
from vistas import (VistaCrearCandidato, VistaHistorialEntrevistas, VistaInformacionTecnica, 
                    VistaConsultarCandidato, VistaConsultarCandidatosDisponibles, 
                    VistaInformacionLaboral, ping)
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
sqlpass = os.getenv("SQL_PASSWORD")
app = Flask(__name__)
test = os.getenv('IF_TEST')
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

CORS(app, origins=["http://localhost:4200", "http://localhost:4201", "http://localhost:8000", "https://micro-web-kdbo2knypq-uc.a.run.app", "http://localhost", "https://localhost"])
if(os.path.isdir('/cloudsql/')):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{sqlpass}@/candidatos?unix_socket=/cloudsql/proyecto-final-01-399101:us-central1:abcjobs'
    app.config['SQLALCHEMY_BINDS'] = {
            "empresas": f'mysql+pymysql://root:{sqlpass}@/empresas?unix_socket=/cloudsql/proyecto-final-01-399101:us-central1:abcjobs'
        }
else:
    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
        app.config['SQLALCHEMY_BINDS'] = {
            "empresas": "mysql+pymysql://root:root@0.0.0.0:3306/empresas"
        }
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{sqlpass}@34.27.118.190:3306/candidatos'
        app.config['SQLALCHEMY_BINDS'] = {
        "empresas": "mysql+pymysql://root:"+sqlpass+"@34.27.118.190:3306/empresas"
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCrearCandidato, '/candidato/create')
api.add_resource(VistaHistorialEntrevistas, '/candidato/historialEntrevistas')
api.add_resource(VistaInformacionTecnica, '/candidato/infoTecnica')
api.add_resource(VistaConsultarCandidato, '/candidato/detalle')
api.add_resource(VistaConsultarCandidatosDisponibles, '/candidatos/disponibles')
api.add_resource(VistaInformacionLaboral, '/candidato/infoLaboral')
api.add_resource(ping, '/candidato/ping')

jwt = JWTManager(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)