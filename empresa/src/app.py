from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from modelos.modelos import db
from vistas.vistas import (VistaRegistroEmpresa)
import os
sqlpass = os.getenv("SQL_PASSWORD")
test = os.getenv('IF_TEST')

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "http://localhost:4201"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+sqlpass+'@34.27.118.190:3306/empresas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)

api = Api(app)
api.add_resource(VistaRegistroEmpresa, '/empresa/registro')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    