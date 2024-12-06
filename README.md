# **Sistema de Coleta, Processamento, e Envio de Emails integrado com Flask Framework**

Este projeto implementa um sistema automatizado para coletar e-mails, processá-los, e retorna-los. O sistema utiliza Flask para gerenciar a interface e interagir com um banco de dados PostgreSQL configurado no Aiven. O objetivo principal desse sistema é automatizar os processos atrelados ao envio dos emails, atualmente alocados em "Solicitação de Defesa" e "Acesso a Computadores".
É importante salientar que o atual repositório funciona independentemente para Coleta integrado ao Framework, porém o sistema cistado é a junção de 5 repositórios, que seram citados detalhadamente abaixo.

---
## **Entendendo o Sistema**

Primeiramente existem duas situações:

- Situação 1: 
   Agente(Professor) solicita a publicação da defesa de mestrado de um aluno, e os repectivos documentos para registro da defesa. No email, estão presentes os dados sobre a banca.
- Situação 2: 
   Agente(Aluno) solicita o acesso aos computadores do laboratório do campus, para isso é necessário ser criado o usuário e a senha do aluno. Nos dados do email, estão presentes o nome do aluno.


## **email_collector_api_web_service(presente repositório)**

1. **Coleta de E-mails:**
   - Coleta automática de e-mails a cada 1 minuto.
   - Armazena os e-mails coletados em objetos `Email`.
   - Emails são classificados em Forwarded(Encaminhados) e Direct(Diretos) 

2. **Evita Envios Duplicados:**
   - E-mails já enviados são movidos para uma lista para evitar duplicidade.

3. **Integração com Banco de Dados:**
   - Armazena logs de e-mails processados e status de envio.
   - Utiliza PostgreSQL configurado via **Aiven** para armazenamento.

4. **Post Flask:**
   - Insere os email coletados no endpoint definido.
   - Pemite o acesso aos dados via requisições HTTP

---
## **neural_categorizer(https://github.com/OnllyWal/neural_categorizer)**

1. **Categorização dos Emails:**
   - Através do título do email, categoriza o tipo do email em Defesa ou Acesso.

2. **Put Flask:**
   - Atualiza o tipo do email para Defesa ou Acesso

---
## **defesa_api_web_service(https://github.com/OnllyWal/defesa_api_web_service)**

1. **Cria Documentação:**
   - Identificado o tipo de email, cria os documentos necessários para a defesa, com os exatos dados da banca apresentados no email.
  
2. **Cria Chamado:**
  - Com os dados do email, inicia o processo para criação de chamado.

3. **Put Flask:**
   - Atualiza os dados do email, com os anexos.
   
---
## **acesso_api_web_service(https://github.com/OnllyWal/acesso_api_web_service)**

1. **Cria Login e Senha:**
   - Identificado o tipo de email, cria o login e senha do aluno em todos os computadores listados por IP.

2. **Put Flask:**
   - Atualiza o corpo do email, com o login e senha.
  
---
## **sender_api_web_service(https://github.com/OnllyWal/sender_api_web_service)**

1. **Envia os Emails:**
   - Identifica os emails processados, e os envia como resposta para o agente, contendo os dados criados.

## **Requisitos**

- **Python** >= 3.8
- **Bibliotecas Python:**
  - Flask
  - Flask-SQLAlchemy
  - psycopg2-binary
  - imaplib (para coleta de e-mails)
  - smtplib (para envio de e-mails)
- **Banco de Dados:**
  - PostgreSQL (hospedado via [Aiven](https://aiven.io/))
- **Outros:**
  - Conta de e-mail com IMAP e SMTP habilitados.

---

## **Instalação**

### 1. Clone o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Configure o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as Dependências
```env
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo .env no diretório raiz com as seguintes variáveis:
```env
EMAIL_HOST=<host_do_email>
EMAIL_USER=<email_usuario>
EMAIL_PASS=<senha_do_email>
DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<nome_do_banco>
```
---

## **Uso**

1. **Execute o Sistema:**
   Ative o servidor Flask:
   ```env
   flask run
   ```

2. **Fluxo do Sistema**
   - A coleta de e-mails ocorre automaticamente.
   - Respostas processadas geram logs no banco de dados.
   - Acesse a interface do Flask para monitorar e gerenciar o sistema.
  
---

## **Arquiterura do Projeto**
   ```
   project
   ├── controllers/
   │   ├── activate_email.py: Inicializa a api de email, coletando emails
   │   ├── api_connector.py: Transforma os objetos de email nos dados a serem enviados para o framework 
   ├── emailapi/
   │   ├── collector.py: Coleta emails via IMAP 
   │   ├── sender.py: Envia emails via SMTP 
   ├── flaskapi/
   │   ├── __init__.py: Inicialização e configuração do framework Flask 
   │   ├── routes.py: Rotas GET e POST do framework Flask 
   ├── models/
   │   ├── db_model.py: Definição da classe de Email do bando de dados, e das funções de pull e push dos dados
   │   ├── email_model.py: Definição das classes de Email
   ├── main.py: Inicializa os dois serviços (emailapi e flaskapi), em threads diferentes
   └── requirements.txt
   ```

---

## **Licença**
Este projeto foi criado e idelializado totalmente pela autora do mesmo, e está protegido sob a lei de produção.
PLÁGIO É CRIME

---
## **Contato**
Caso tenha dúvidas ou sugestões, entre em contato:

E-mail: walcandeia@gmail.com

---
## **Notas**
Esse projeto não está finalizado, o mesmo se encontra em processo de desenvolvimento.
