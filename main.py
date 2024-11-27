import time
import threading
from emailapi.collector import EmailCollector  # Classe EmailCollector já implementada
from emailapi.sender import EmailSender  # Classe EmailSender já implementada
from emailapi.connection_flask import enviar_email
from emailapi.email_obj import Email
from flaskapi.app import app


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

    sender.disconnect()


def main():
    # Rodar o serviço de coleta de e-mails em uma thread separada
    email_thread = threading.Thread(target=coletar_emails)
    email_thread.daemon = True  # A thread será encerrada quando o programa principal terminar
    email_thread.start()

    # Rodar o aplicativo Flask
    app.run(debug=True, use_reloader=False)  # use_reloader=False para evitar conflito com threading


if __name__ == "__main__":
    main()
