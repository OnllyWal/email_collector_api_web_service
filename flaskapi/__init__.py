from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criação do objeto db (compartilhado em toda a aplicação)
db = SQLAlchemy()

def create_app():
    # Criação e configuração da aplicação Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://avnadmin:AVNS_PbDFe9GkvFNPPTDFDJG@proposervice-walcandeia-bd.g.aivencloud.com:20761/defaultdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização do banco de dados
    db.init_app(app)

    # Registro das rotas
    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app
