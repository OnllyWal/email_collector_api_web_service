import requests
import logging

url = "http://127.0.0.1:5000/emails"

def enviar_email(obj, tipo):
        """Envia um email formatado como JSON para a API."""
        
        try:
            dados = formatar_dados(obj, tipo)
            response = requests.post(url, json=dados)
            return response.json()
        
        except requests.RequestException as e:
            logging.error(f"Erro ao enviar o email: {e}")
            raise

def formatar_dados(obj, tipo):
    """Formata os dados para envio à API."""
    dados = {
        "tipo": tipo,
        "from_name": obj.sender_name,
        "from_complete_name": obj.complete_name,
        "endereco": obj.email_name,
        "titulo": obj.subject,
        "corpo": obj.body,
        "anexos": obj.attachments,
    }

    if tipo == 'f':
        dados.update({
            "origin_name": obj.origin_name,
            "origin_address": obj.origin_address,
        })
    elif tipo == 'd':
        dados.update({
            "origin_name": "não encaminhado",
            "origin_address": "não encaminhado",
        })

    return dados