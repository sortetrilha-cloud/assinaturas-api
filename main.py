import os
import pyodbc
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Carrega variáveis do .env
load_dotenv(dotenv_path="app/config/.env")

# Flask
app = Flask(__name__)

# Conexão com SQL Server
SQLSERVER_CONN = os.getenv("SQLSERVER_CONN")

def conectar_banco():
    try:
        conn = pyodbc.connect(SQLSERVER_CONN)
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return None


@app.route('/api/cadastro', methods=['POST'])
def cadastro_cliente():
    try:
        dados = request.get_json()
        print("📦 Dados recebidos:", dados)

        nome = dados.get("nome")
        email = dados.get("email")
        celular = dados.get("telefone")

        # Campos fixos
        produto = "TESTE"
        plano = 7
        cpf = "111"
        quantidade_jogos = 3
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Validação básica
        if not nome or not email:
            return jsonify({"status": "erro", "mensagem": "Campos obrigatórios faltando"}), 400

        conn = conectar_banco()
        if not conn:
            return jsonify({"status": "erro", "mensagem": "Falha na conexão com o banco"}), 500

        cursor = conn.cursor()

        # 1️⃣ Inserir na tabela MEGASENA_CLIENTE_ESPECIAL
        cursor.execute("""
            INSERT INTO MEGASENA_CLIENTE_ESPECIAL (produto, plano, nome, e_mail, celular, cpf, quantidade_jogos, data_assinatura)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (produto, plano, nome, email, celular, cpf, quantidade_jogos, data_atual))
        conn.commit()

        # 2️⃣ Inserir na tabela LOTOFACIL_CLIENTE_ESPECIAL
        cursor.execute("""
            INSERT INTO LOTOFACIL_CLIENTE_ESPECIAL (produto, plano, nome, e_mail, celular, cpf, quantidade_jogos, data_assinatura)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (produto, plano, nome, email, celular, cpf, quantidade_jogos, data_atual))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Cliente {nome} cadastrado com sucesso nas duas loterias!"
        }), 200

    except Exception as e:
        print("Erro geral:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)