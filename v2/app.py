# app.py
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from database import db
from items_controller import init_app

app = Flask(__name__)
CORS(app)  # Permite todas as origens
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Inicia o Swagger
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# Inicializa as rotas do controlador
init_app(app)

if __name__ == '__main__':
    app.run(debug=True)