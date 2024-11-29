import time
from emailapi.sender import EmailSender
from emailapi.collector import EmailCollector
from controller.api_connector import enviar_email

def coletar_emails():
    email_address = 'maquinas902@gmail.com'  # email para coleta
    password = 'vjmm jseq feuk amhv'  # senha email de coleta
    destinatario = 'walcandeia@gmail.com'  # email para autorização

    # Configuração do coletor e do sender
    collector = EmailCollector(email_address, password)
    sender = EmailSender(email_address, password)

    # Conecta ao servidor SMTP
    sender.connect()

    while True:
        # Coleta Emails, cria objetos e armazena na lista collector.emails
        print("Coletando novos emails...")
        collector.connect()
        collector.fetch_emails()

        if collector.emails_dict:
            print(f"{len(collector.emails_dict)} emails coletados. Processando...")
            for tipo, list_emails in collector.emails_dict.items():
                for email in list_emails:
                    enviar_email(email, tipo)

            collector.emails_dict.clear()
            print("Lista de emails coletados esvaziada.")
        else:
            print("Nenhum novo email coletado.")

        collector.logout()
        time.sleep(30)  # Pausa de 30 segundos antes de coletar novamente
