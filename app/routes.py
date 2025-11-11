from flask import Blueprint, request, jsonify
from .database import inserir_cliente
from .email_sender import enviar_email_loteria

main_bp = Blueprint('main', __name__)

@main_bp.route('/cadastro', methods=['POST'])
def cadastro_cliente():
    data = request.get_json()
    try:
        nome = data['nome']
        email = data['email']
        telefone = data['telefone']
        cpf = data['cpf']

        inserir_cliente(nome, email, telefone, cpf)
        enviar_email_loteria(email, None, 'MEGASENA', 'Teste Grátis Mega-Sena')
        enviar_email_loteria(email, None, 'LOTOFACIL', 'Teste Grátis Lotofácil')

        return jsonify({"status": "success", "message": "Cadastro concluído e e-mails enviados!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
