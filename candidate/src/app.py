from flask import Flask
from flask_restful import Api
from modelos import db
from vistas import (VistaCrearCandidato, ping)
import os

sqlpass = os.getenv("SQL_PASSWORD")
app = Flask(__name__)

test = os.getenv('IF_TEST')

if test:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+sqlpass+'@34.27.118.190:3306/candidatos'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCrearCandidato, '/candidato/create')
api.add_resource(ping, '/candidato/ping')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)