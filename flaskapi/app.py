from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Lista para armazenar os objetos enviados pelo POST
emails = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://avnadmin:AVNS_PbDFe9GkvFNPPTDFDJG@proposervice-walcandeia-bd.g.aivencloud.com:20761/defaultdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Emaildb(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    from_name = db.Column(db.String(100))
    from_complete_name = db.Column(db.String(200))
    endereco = db.Column(db.String(100))
    titulo = db.Column(db.String(200))
    corpo = db.Column(db.Text)
    anexos = db.Column(db.Text)
    origin_name = db.Column(db.String(100))
    origin_address = db.Column(db.String(100))  # Poderia ser um campo JSON ou apenas uma string (separada por vírgulas, por exemplo)

    def __init__(self, tipo, from_name, from_complete_name, endereco, titulo, corpo, anexos, origin_name, origin_adress):
        self.tipo = tipo
        self.from_name = from_name
        self.from_complete_name = from_complete_name
        self.endereco = endereco
        self.titulo = titulo
        self.corpo = corpo
        self.anexos = anexos
        self.origin_name = origin_name
        self.origin_address = origin_adress

with app.app_context():
    db.create_all() 

def add_email_to_db(dados):
    email = Emaildb(
        tipo=dados['tipo'],
        from_name=dados['from_name'],
        from_complete_name=dados['from_complete_name'],
        endereco=dados['endereco'],
        titulo=dados['titulo'],
        origin_name= dados['origin_name'],
        origin_adress= dados['origin_address'],
        corpo=dados['corpo'],
        anexos=",".join(dados['anexos'])  # Armazenando anexos como uma string separada por vírgulas
    )

    db.session.add(email)
    db.session.commit()

# Rota para receber o POST e salvar o objeto
@app.route('/emails', methods=['POST'])
def adicionar_email():
    try:
        dados = request.get_json()  # Obtém os dados JSON enviados no corpo da requisição
        add_email_to_db(dados)  # Adiciona o e-mail ao banco de dados
        return jsonify({"message": "E-mail adicionado com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Rota para retornar todos os emails
@app.route('/emails', methods=['GET'])
def listar_emails():
    try:
        emails = Emaildb.query.all()  # Recupera todos os e-mails do banco de dados
        email_list = []
        for email in emails:
            email_list.append({
                "id": email.id,
                "tipo": email.tipo,
                "from_name": email.from_name,
                "from_complete_name": email.from_complete_name,
                "endereco": email.endereco,
                "titulo": email.titulo,
                "corpo": email.corpo,
                "anexos": email.anexos.split(","),  # Converte a string de anexos de volta para uma lista
                "origin_name": email.origin_name,
                "origin_adress": email.origin_address
            })
        return jsonify(email_list)  # Retorna os e-mails como um JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/')
def index():
    return "Conectado ao banco de dados PostgreSQL no Aiven!"
