from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para conectar ao banco de dados PostgreSQL (Render)
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
        print("Erro na conexão com o banco:", e)
        return None


@app.route("/cadastro", methods=["POST"])
def cadastro_cliente():
    try:
        dados = request.get_json()
        print("📦 Dados recebidos:", dados)

        nome = dados.get("nome")
        email = dados.get("email")
        celular = dados.get("telefone")

        if not nome or not email or not celular:
            return jsonify({"status": "erro", "mensagem": "Campos obrigatórios faltando"}), 400

        conn = conectar_banco()
        if not conn:
            return jsonify({"status": "erro", "mensagem": "Falha na conexão com o banco"}), 500

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes_assinaturas (nome, email, celular)
            VALUES (%s, %s, %s)
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


@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "API de Assinaturas ativa ✅"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
