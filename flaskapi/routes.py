from flask import Blueprint, request, jsonify, current_app
from models.db_model import pull_emails, push_emails, update_emails_db
from models.files_model import save_files, get_file_path
from flask import send_from_directory

app_routes = Blueprint('app_routes', __name__)

# Lista para armazenar os objetos enviados pelo POST
emails = []

@app_routes.route('/upload', methods=['POST'])
def post_files():
    try:
        files = request.files.getlist('file')
        file_urls = save_files(files, current_app.config['UPLOAD_FOLDER'])
        
        if not file_urls: 
            return jsonify({"error":"Nenhum arquivo válido enviado"}), 400
        return jsonify({"message":"Arquivos salvos com sucesso!", "urls":file_urls}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app_routes.route('/download/<filename>', methods=['GET'])
def get_files(filename):
    try:
        file_path = get_file_path(current_app.config['UPLOAD_FOLDER'], filename)
        if not file_path:
            current_app.logger.error(f"Arquivo não encontrado: {filename}")
            return jsonify({"error":"Arquivo não encontrado"}), 404
        
        current_app.logger.info(f"Enviando arquivo: {file_path}")
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    
    except Exception as e:
        current_app.logger.error(f"Erro ao processar o arquivo {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app_routes.route('/emails', methods=['POST'])
def post_emails():
    try:
        dados = request.get_json()  # Obtém os dados JSON enviados no corpo da requisição
        push_emails(dados)  # Adiciona o e-mail ao banco de dados
        return jsonify({"message": "E-mail adicionado com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app_routes.route('/emails/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    try:
        print(email_id)
        update_data = request.get_json()
        emails_list = pull_emails()
        if not update_data:
            
            return jsonify({"error":"Nenhum dado enviado"}), 400
        email= next((email for email in emails_list if email["id"] == email_id), None)
        print(email)
        if not email:
            return jsonify({"error":"Email não encontrado"}), 404
        
        update_emails_db(email_id, update_data)
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
