from flask import Blueprint, request, jsonify
from models.db_model import pull_emails, push_emails
from flaskapi import db
import os

app_routes = Blueprint('app_routes', __name__)

# Lista para armazenar os objetos enviados pelo POST
emails = []

@app.routes.route('/upload', methods=['POST'])
def post_files():
    try:
        files = request.files.getlist('file')
        file_urls = save_files(files, current_app.config['UPLOAD_FOLDER'])
        
        if not file_urls:
            return jsonify({"error": "Nenhum arquivo válido enviado"}), 400
        return jsonify({"message": "Arquivos salvos com sucesso!", "urls": file_urls}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.routes.route('/download/<filename>', methods=['GET'])
def get_files:
    try:
        file_path = get_path(current_app.config['UPLOAD_FOLDER'], filename)
        if not file_path:
            return jsonify({"error":"Arquivo não encontrado"}), 404
        
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app_routes.route('/emails', methods=['POST'])
def post_emails():
    try:
        dados = request.get_json()  # Obtém os dados JSON enviados no corpo da requisição
        push_emails(dados)  # Adiciona o e-mail ao banco de dados
        return jsonify({"message": "E-mail adicionado com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.routes.route('/emails/<int:email_id>' methods=['PUT'])
def update_email(email_id):
    try:
        update_data = request.json
        for email in emails:
            if email["id"] == email_id:
                email.update(update_data)
                return jsonify({"message": "E-mail atualizado com sucesso!"}), 200
    
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
