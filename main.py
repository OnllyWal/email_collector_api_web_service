import threading
from flaskapi import create_app, db
from controllers.activate_email import coletar_emails

def main():
    app = create_app()

    # Criando tabelas no banco
    with app.app_context():
        db.create_all()

    # Rodar o serviço de coleta de e-mails em uma thread separada
    email_thread = threading.Thread(target=coletar_emails)
    email_thread.daemon = True  # A thread será encerrada quando o programa principal terminar
    email_thread.start()

    # Rodar o aplicativo Flask
    app.run(host="0.0.0.0", port=5000) # use_reloader=False para evitar conflito com threading


if __name__ == "__main__":
    main()
