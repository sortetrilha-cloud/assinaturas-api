import requests
import json

def cadastrar_usuario(cliente):
    url = "https://api.sorte-trilha.com/api/cadastro"
    payload = {
        "nome": cliente["nome"],
        "e_mail": cliente["e_mail"],
        "celular": cliente["celular"],
        "cpf": "111",
        "plano": "TESTE"
    }

    try:
        resposta = requests.post(url, json=payload)
        if resposta.status_code == 200:
            print("✅ Cadastro realizado com sucesso!")
            return True
        else:
            print(f"⚠️ Erro ao cadastrar: {resposta.status_code}")
            print(resposta.text)
            return False
    except Exception as e:
        print("❌ Erro na conexão com a API:", e)
        return False
