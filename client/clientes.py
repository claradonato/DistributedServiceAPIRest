import os
import requests
import time

NOME = os.getenv("NOME_CLIENTE")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5000")

# FUNÇÃO CADASTRAR ;)
def cadastrar_usuario():
    url = f"{SERVER_URL}/usuarios"
    dados = {"nome": NOME}

    resposta = requests.post(url, json=dados)

    print(f"[{NOME}] Cadastro de usuário")
    print(f"Status HTTP: {resposta.status_code}")
    print(f"Resposta: {resposta.json()}")

    return resposta

# FUNÇÃO PARA ENVIAR UMA MENSAGEM ;)
def enviar_mensagem(destinatario, conteudo):
    url = f"{SERVER_URL}/mensagens"

    dados = {
        "remetente": NOME,
        "destinatario": destinatario,
        "conteudo": conteudo
    }

    resposta = requests.post(url, json=dados)

    print(f"[{NOME}] Enviando mensagem para {destinatario}")
    print(f"Conteúdo: {conteudo}")
    print(f"Status HTTP: {resposta.status_code}")
    print(f"Resposta: {resposta.json()}")

    return resposta

# FUNÇÃO PARA CONSULTAR ;)
def consultar_mensagens():
    url = f"{SERVER_URL}/mensagens"

    parametros = {
        "destinatario": NOME,
        "lida": "false"
    }

    resposta = requests.get(url, params=parametros)

    print(f"[{NOME}] Consultando mensagens não lidas")
    print(f"Status HTTP: {resposta.status_code}")

    mensagens = resposta.json()
    print(f"Mensagens recebidas: {mensagens}")

    return mensagens

# FUNÇÃO PARA MARCAR COMO LIDA
def marcar_como_lida(id_mensagem):
    url = f"{SERVER_URL}/mensagens/{id_mensagem}"

    dados = {
        "lida": True
    }

    resposta = requests.patch(url, json=dados)

    print(f"[{NOME}] Marcando mensagem #{id_mensagem} como lida")
    print(f"Status HTTP: {resposta.status_code}")
    print(f"Resposta: {resposta.json()}")

    return resposta

# Entender que cada conteiner executara o main,
# Porém cada uma com sua variavel nome diferente graças ao compose
def main():
    # Todo cliente começa se cadastrando
    cadastrar_usuario()

    # Alice envia uma mensagem para Bob
    if NOME == "Alice":
        enviar_mensagem(
            "Bob",
            "Olá, Bob! Aqui é a Alice."
        )

    # Carol envia uma mensagem para Bob
    elif NOME == "Carol":
        enviar_mensagem(
            "Bob",
            "Olá, Bob! Aqui é a Carol."
        )

    # Bob consulta suas mensagens novas
    elif NOME == "Bob":
        time.sleep(2)
        mensagens = consultar_mensagens()

        # Bob marca a primeira mensagem recebida como lida
        if mensagens:
            id_mensagem = mensagens[0]["id"]
            marcar_como_lida(id_mensagem)

        # Bob consulta novamente para confirmar
        consultar_mensagens()

if __name__ == "__main__":
    main()