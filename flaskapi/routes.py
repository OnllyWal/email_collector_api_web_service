from flask import Blueprint, request, jsonify
from models.db_model import pull_emails, push_emails
from flaskapi import db

app_routes = Blueprint('app_routes', __name__)

# Lista para armazenar os objetos enviados pelo POST
emails = []

@app_routes.route('/emails', methods=['POST'])
def post_emails():
    try:
        dados = request.get_json()  # Obtém os dados JSON enviados no corpo da requisição
        push_emails(dados)  # Adiciona o e-mail ao banco de dados
        return jsonify({"message": "E-mail adicionado com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Rota para retornar todos os emails
@app_routes.route('/emails', methods=['GET'])
def get_emails():
    try:
        emails_list = pull_emails()
        return jsonify(emails_list)  # Retorna os e-mails como um JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app_routes.route('/')
def index():
    return "Conectado ao banco de dados PostgreSQL no Aiven!"
