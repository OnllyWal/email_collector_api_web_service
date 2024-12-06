from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Criação do objeto db (compartilhado em toda a aplicação)
db = SQLAlchemy()

def create_app():
    # Criação e configuração da aplicação Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://avnadmin:AVNS_PbDFe9GkvFNPPTDFDJG@proposervice-walcandeia-bd.g.aivencloud.com:20761/defaultdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = '/home/wal/APIPropos/email_collector_api_web_service/uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicialização do banco de dados
    db.init_app(app)

    # Registro das rotas
    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app
