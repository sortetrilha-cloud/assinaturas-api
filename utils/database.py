import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    conn_str = os.getenv("SQLSERVER_CONN")
    conn = pyodbc.connect(conn_str)
    return conn