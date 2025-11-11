import os
import pickle
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CRED_FILE = os.getenv("GMAIL_CREDENTIALS_FILE")
TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE")
IMAGEM_PADRAO = "static/imagens/logo_email.png"

def autenticar_gmail():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def enviar_email_loteria(destinatario, jogos, loteria, produto):
    service = autenticar_gmail()
    with open('templates/email_template.html', 'r', encoding='utf-8') as f:
        corpo_html = f.read().replace('{{PRODUTO}}', produto).replace('{{LOTERIA}}', loteria)

    mensagem = MIMEMultipart("related")
    mensagem["to"] = destinatario
    mensagem["subject"] = f"🎲 Seu jogo teste grátis da {loteria} chegou!"

    alternativa = MIMEMultipart("alternative")
    mensagem.attach(alternativa)
    alternativa.attach(MIMEText(corpo_html, "html"))

    with open(IMAGEM_PADRAO, 'rb') as img:
        imagem = MIMEImage(img.read())
        imagem.add_header('Content-ID', '<logo>')
        mensagem.attach(imagem)

    raw_message = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
