import requests

def enviar_email(obj, tipo):

    url = "http://127.0.0.1:5000/emails"

    if tipo == 'f':
        #print(f"tipo: {tipo},from_name: {obj.sender_name},from_complete_name: {obj.complete_name} endereco: {obj.email_name} origin_name: {obj.origin_name},origin_address: {obj. origin_address},titulo: {obj.subject},corpo: {obj.body},anexos: {obj.attachments}")
        dados = {
            "tipo": tipo,
            "from_name" : obj.sender_name,
            "from_complete_name" : obj.complete_name,
            "endereco" : obj.email_name,
            "origin_name" : obj.origin_name,
            "origin_address" : obj. origin_address,
            "titulo" : obj.subject,
            "corpo" : obj.body,
            "anexos" : obj.attachments
        }

    elif tipo == 'd':
        dados = {
            "tipo": tipo,
            "from_name" : obj.sender_name,
            "from_complete_name" : obj.complete_name,
            "endereco" : obj.email_name,
            "titulo" : obj.subject,
            "corpo" : obj.body,
            "anexos" : obj.attachments,
            "origin_name" : "não encaminhado",
            "origin_adress" : "não encaminhado"
        }
    
    answer = requests.post(url,json=dados)
    print("Status:", answer.status_code)
    print("Resposta:", answer.json())