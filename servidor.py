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

        if not nome: #transforma o dicionário em json e já retorna o cabeçalho HTTP
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

# ROTA 2: Envio e consulta de coleção de mensagens ----------------------------
@app.route("/mensagens", methods=["POST", "GET"])
def gerenciar_mensagens():
    global contador_mensagem_id

    if request.method == "POST":
        dados = request.get_json() or {}
        remetente = dados.get("remetente")
        destinatario = dados.get("destinatario")
        conteudo = dados.get("conteudo")

        if not remetente or not destinatario or not conteudo:
            return jsonify({"erro": "Campos 'remetente', 'destinatario', e 'conteudo' são obrigatórios."}), 400

        nova_mensagem = {
            "id": contador_mensagem_id,
            "remetente": remetente,
            "destinatario": destinatario,
            "conteudo": conteudo,
            "lida": False
        }

        mensagens.append(nova_mensagem)
        print(f"[LOG SERVIDOR] Mensagem #{contador_mensagem_id} de '{remetente}' para '{destinatario}' registrada.")
        contador_mensagem_id += 1

        return jsonify(nova_mensagem), 201
    elif request.method == "GET":
        destinatario_filtro = request.args.get("destinatario")
        remetente_filtro = request.args.get("remetente")
        lida_filtro = request.args.get("lida");

        resultado = mensagens

        if destinatario_filtro:
            resultado = [m for m in resultado if m["destinatario"] == destinatario_filtro]

        if remetente_filtro:
            resultado = [m for m in resultado if m["remetente"] == remetente_filtro]

        if lida_filtro is not None:
            is_lida = lida_filtro.lower() == "true"
            resultado = [m for m in resultado if m["lida"] == is_lida]

        return jsonify(resultado), 200
    
# Execução do servidor Flask na porta 5000 escutando em todas as interfaces de rede
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
