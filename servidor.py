from flask import Flask, request, jsonify

# Inicialização da aplicação Flask
app = Flask(__name__)
app.json.ensure_ascii = False # Configura o Flask para manter caracteres acentuados legíveis no JSON de resposta

# PASSO 1: MODELAGEM DAS ESTRUTURAS DE DADOS EM MEMÓRIA
usuarios = {}
mensagens = [] # { "id": int, "remetente": str, "destinatario": str, "conteudo": str, "lida": bool }
contador_mensagem_id = 1

# PASSO 2: ROTAS DA API REST (ENDPOINTS)

# ROTA 1: Cadastro e Consulta Geral de Usuários ---------------------------
@app.route("/usuarios", methods=["POST", "GET"])
def gerenciar_usuarios():
    if request.method == "POST":
        dados = request.get_json() or {}
        nome = dados.get("nome")

        if not nome:
            return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400

        if nome in usuarios:
            return jsonify({"erro": f"Usuário '{nome}' já cadastrado."}), 409

        # Registra a identidade do cliente no dicionário de usuários
        usuarios[nome] = {"nome": nome}
        print(f"[LOG SERVIDOR] Usuário cadastrado com sucesso: {nome}")

        # Retorna 201 Created indicando criação bem-sucedida do recurso
        return jsonify(usuarios[nome]), 201
    
    elif request.method == "GET":
        return jsonify(list(usuarios.values())), 200

# Execução do servidor Flask na porta 5000 escutando em todas as interfaces de rede
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
