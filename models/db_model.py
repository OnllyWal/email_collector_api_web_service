from flask_sqlalchemy import SQLAlchemy
from flaskapi import db

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
    origin_address = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, tipo, from_name, from_complete_name, endereco, titulo, corpo, anexos, origin_name, origin_address, status):
        self.tipo = tipo
        self.from_name = from_name
        self.from_complete_name = from_complete_name
        self.endereco = endereco
        self.titulo = titulo
        self.corpo = corpo
        self.anexos = anexos
        self.origin_name = origin_name
        self.origin_address = origin_address
        self.status = status

def push_emails(dados):
    email = Emaildb(
        tipo=dados['tipo'],
        from_name=dados['from_name'],
        from_complete_name=dados['from_complete_name'],
        endereco=dados['endereco'],
        titulo=dados['titulo'],
        corpo=dados['corpo'],
        anexos=",".join(dados['anexos']),  # Armazenando anexos como uma string separada por vírgulas
        origin_name=dados['origin_name'],
        origin_address=dados['origin_address'],
        status="Armazenado"
    )

    db.session.add(email)
    db.session.commit()

def pull_emails():
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
            "origin_address": email.origin_address,
            "status": email.status
        })
    return email_list

def update_emails_db(email_id, dados):
    email = Emaildb.query.get(email_id)
    
    if email:
        # Atualizar os campos do email com os novos dados
        email.tipo = dados['tipo']
        email.from_name = dados['from_name']
        email.from_complete_name = dados['from_complete_name']
        email.endereco = dados['endereco']
        email.titulo = dados['titulo']
        email.corpo = dados['corpo']
        email.anexos = dados['anexos']  # Armazenando anexos como uma string separada por vírgulas
        email.origin_name = dados['origin_name']
        email.origin_address = dados['origin_address']
        email.status = dados['status']  # Atualizando o status, caso seja necessário
        
        # Commit para salvar as mudanças no banco
        db.session.commit()
        return {"message": "Email atualizado com sucesso!"}, 200
    else:
        # Se o email não for encontrado
        return {"error": "Email não encontrado"}, 404

