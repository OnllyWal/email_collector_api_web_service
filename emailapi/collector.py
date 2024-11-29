import imaplib
import email as email_lib
import os
import re
from models.email_model import Direct_Email, Forwarded_Email

class EmailCollector:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.connection = None
        self.emails_dict = {'f':[], 'd':[]}  # Lista para armazenar objetos da classe Email

    def connect(self):
        """Conecta ao servidor de email e seleciona a caixa de entrada."""
        try:
            self.connection = imaplib.IMAP4_SSL("imap.gmail.com")
            self.connection.login(self.email_address, self.password)
            print("Conectado ao servidor de email")
            self.connection.select('inbox', readonly=False)  # Permite modificar a caixa de entrada (marcar emails como lidos)
        
        except imaplib.IMAP4.error as e:
            print(f"Erro ao conectar ao servidor: {e}")
            raise ConnectionError("Erro ao conectar ao servidor de email.")
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            raise
    
    def fetch_emails(self):
        """Busca todos os emails não lidos da caixa de entrada e cria objetos Email."""
        if self.connection is None:
            raise ConnectionError("Você deve conectar primeiro.")

        try:
            # Busca apenas os emails não lidos
            answers, ids = self.connection.search(None, 'UNSEEN')
            email_ids = ids[0].split()

            for num in email_ids:
                results, data = self.connection.fetch(num, '(RFC822)')
                text = data[0][1].decode('utf-8')
                msg = email_lib.message_from_string(text)
                email_obj = self.process_email(msg)
                if email_obj:
                      # Processa o email e retorna um objeto Email
                    if isinstance(email_obj, Direct_Email):
                        self.emails_dict['d'].append(email_obj)  # Adiciona o objeto Email à lista
                    if isinstance(email_obj, Forwarded_Email):
                        self.emails_dict['f'].append(email_obj)

                # Marca o email como lido
                self.connection.store(num, '+FLAGS', '\\Seen')
        
        except Exception as e:
            print(f"Erro ao buscar emails: {e}")
            raise

    def process_email(self, msg):
        """Processa cada mensagem de email e retorna um objeto Email."""
        try:
            sender_name = msg['From'].split(" ")[0] if msg['From'] else "Desconhecido"
            email_name = msg['From'].split(" ")[-1].strip('<>') if len(msg['From'].split(" ")) > 0 else "Desconhecido"
            complete_name = msg['From'].split('<')[0].strip() if msg['From'] else "Desconhecido"
            raw = str(msg)

            attachments = []  # Lista para armazenar os caminhos dos anexos
            email_body = ''  # String para armazenar o corpo do email

            # Processa as partes do email
            for part in msg.walk():
                if part.get_content_maintype() == 'text' and part.get_content_type() == 'text/plain':
                    email_body = part.get_payload(decode=True).decode('utf-8')  # Captura o corpo do email
                elif part.get('Content-Disposition') is not None:
                    attachment_path = self.save_attachment(part, sender_name)
                    if attachment_path:
                        attachments.append(attachment_path)
            
            ans = self.get_subject(email_body)
            if ans:
                origin_name, origin_adress, subject = ans
                return Forwarded_Email(
                    sender_name, 
                    complete_name,
                    email_name,
                    email_body,
                    attachments,
                    subject,
                    origin_name , 
                    origin_adress)
            else:
                subject = msg['Subject'] if msg['Subject'] else "Sem título"
                return Direct_Email(
                    sender_name, 
                    complete_name,
                    email_name,
                    email_body,
                    attachments,
                    subject)
        
        except Exception as e:
            print(f"Erro ao processar o email: {e}")
            return None
    
    def get_subject(self, txt):
        match = re.search(r"From:\s*(.*?)\s*<([^>]+)>\s*.*?Subject:\s*(.*?)\s*\n", txt, re.DOTALL | re.IGNORECASE)
        if match:
            print(match.group(1).strip(), match.group(2).strip(), match.group(3).strip())
            return match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        return None

    def extrair_nome_email(from_texto):

        # Regex para capturar Nome e email no formato Nome <email>
        match = re.match(r"(.*)\s*<(.+)>", from_texto)
        if match:
            nome = match.group(1).strip()
            email = match.group(2).strip()
            return [nome, email]
        else:
            # Caso não esteja no formato Nome <email>, retorna o texto original
            return from_texto, None

    def save_attachment(self, part, sender_name):
        """Salva os anexos de email e retorna o caminho do arquivo salvo."""
        try:
            filename = part.get_filename()
            if filename:
                base_dir = f'/home/wal/ProcessAutomation/Process-Automation/OO/collected/{sender_name}'
                os.makedirs(base_dir, exist_ok=True)

                # Gera um caminho de arquivo único para o anexo
                attachment_path = os.path.join(base_dir, filename)
                count = 1

                while os.path.exists(attachment_path):
                    attachment_path = os.path.join(base_dir, f"{filename.split('.')[0]}_{count}.{filename.split('.')[-1]}")
                    count += 1

                # Salva o anexo
                with open(attachment_path, 'wb') as attachment:
                    attachment.write(part.get_payload(decode=True))

                print(f"Anexo salvo: {attachment_path}")
                return attachment_path
            return None
        
        except Exception as e:
            print(f"Erro ao salvar anexo: {e}")
            return None
    
    def logout(self):
        """Desfaz a conexão com o servidor de email."""
        if self.connection:
            try:
                self.connection.logout()
                print("Desconectado do servidor de email")
            
            except Exception as e:
                print(f"Erro ao desconectar: {e}")
                raise
