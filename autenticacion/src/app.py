from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from modelos import db
from vistas import (VistaLogInCandidato, VistaLogInEmpresa)
import os
sqlpass = os.getenv("SQL_PASSWORD")
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+sqlpass+'@34.27.118.190:3306/candidatos'
app.config['SQLALCHEMY_BINDS'] = {
    "empresas": {"url": "mysql+pymysql://root:'+'sqlpass'+'@34.27.118.190:3306/empresas"},
    "empleados": {"url": "mysql+pymysql://root:'+'sqlpass'+'@34.27.118.190:3306/empleados"},
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

app_context = app.app_context()
app_context.push()

db.init_app(app)
# db.create_all()

api = Api(app)
api.add_resource(VistaLogInCandidato, '/autenticacion/candidatos/login')
api.add_resource(VistaLogInEmpresa, '/autenticacion/empresas/login')

jwt = JWTManager(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    