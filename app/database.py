import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def conectar_sqlserver():
    conn_str = os.getenv("SQLSERVER_CONN")
    return pyodbc.connect(conn_str)

def inserir_cliente(nome, email, telefone, cpf):
    conn = conectar_sqlserver()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ASSINANTES_NOVOS (NOME, E_MAIL, CELULAR, CPF, PLANO)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, email, telefone, cpf, 7))
    conn.commit()
    cursor.close()
    conn.close()
