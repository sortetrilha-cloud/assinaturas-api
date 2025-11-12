import os
import pyodbc
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
# Carrega variáveis do .env
load_dotenv(dotenv_path="app/config/.env")

# Flask
app = Flask(__name__)

# Conexão com SQL Server
SQLSERVER_CONN = os.getenv("SQLSERVER_CONN")

# 🔧 Conexão com o banco do Render
def conectar_banco():
    try:
        conn = psycopg2.connect(
            host="dpg-d49rogruibrs73c29nb0-a.oregon-postgres.render.com",
            database="assinaturas_db",
            user="assinaturas_db_user",
            password="TOxnum4xqerbjiwyxrs0X6dfPtiBGwwP",
            port="5432"
        )
        return conn
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        return None


@app.route("/cadastro", methods=["POST"])
def cadastro_cliente():
    try:
        dados = request.get_json()
        print("📦 Dados recebidos:", dados)

        nome = dados.get("nome")
        email = dados.get("email")
        celular = dados.get("telefone")

        # Validação básica
        if not nome or not email:
            return jsonify({"status": "erro", "mensagem": "Campos obrigatórios faltando"}), 400

        conn = conectar_banco()
        if not conn:
            return jsonify({"status": "erro", "mensagem": "Falha na conexão com o banco"}), 500

        cursor = conn.cursor()

        # Inserir na tabela CLIENTES_API (sem duplicar e-mails)
        cursor.execute("""
            INSERT INTO CLIENTES_API (nome, email, celular)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """, (nome, email, celular))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Cliente {nome} cadastrado com sucesso!"
        }), 200

    except Exception as e:
        print("Erro geral:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)