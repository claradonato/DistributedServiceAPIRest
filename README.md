# DistributedServiceAPIRest
Implementação de serviço distribuído de comunicação com API REST utilizando contâineres para implementar servidor e clientes orquestrados por um Docker Compose, utilizando o protocolo HTTP como contrato de comunicação desacoplado e transparente.

**Desafio:** fazer com que processos independentes consigam trocar informações sem compartilhar memória interna.

## Arquitetura

O projeto é composto por:

- **1 servidor Flask**, responsável por armazenar usuários e mensagens e disponibilizar a API REST;
- **3 clientes independentes**, representados por Alice, Bob e Carol;
- **Docker Compose**, responsável por criar e conectar todos os containers.

Os clientes não compartilham memória diretamente. A comunicação ocorre através do servidor utilizando requisições HTTP e dados em formato JSON.

```text
                    ┌─────────────────┐
                    │    SERVIDOR     │
                    │  Flask :5000    │
                    └────────┬────────┘
                             │
                  HTTP / JSON│
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
          Alice             Bob            Carol
         Cliente           Cliente         Cliente
```

## Estrutura do projeto

```text
DistributedServiceAPIRest/
├── servidor/
│   ├── servidor.py
│   └── Dockerfile
├── clientes/
│   ├── clientes.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Principais endpoints

### Usuários

**POST `/usuarios`**

Cadastra um novo usuário.

**GET `/usuarios`**

Consulta os usuários cadastrados.

### Mensagens

**POST `/mensagens`**

Cria uma nova mensagem contendo remetente, destinatário e conteúdo.

**GET `/mensagens`**

Consulta as mensagens armazenadas. A rota permite utilizar filtros através de query parameters, como:

```text
/mensagens?destinatario=Bob&lida=false
```

**PATCH `/mensagens/<id>`**

Atualiza uma mensagem específica. No projeto, é utilizado para marcar uma mensagem como lida.

Exemplo:

```json
{
    "lida": true
}
```

## Funcionamento

Os clientes executam automaticamente seus respectivos roteiros, sem entrada pelo teclado.

- **Alice** se cadastra e envia uma mensagem para Bob.
- **Carol** se cadastra e envia uma mensagem para Bob.
- **Bob** se cadastra, consulta suas mensagens não lidas, marca uma mensagem como lida e realiza uma nova consulta.

Dessa forma, é possível observar nos logs a comunicação entre os clientes e o servidor.

## API Rest
Funciona como um contrato de interoperabilidade.
* Desacoplamento e independência: o servidor e o cliente não precisam saber a linguagem que cada um foi programado. Ambos seguem protocolo HTTP e tem compreensão da estrutura JSON.
* Modelagem Orientada à Recursos: ao invés de chamar funções remotas com nomes arbitrários, a comunicação é feita manipulando recursos (/usuarios e /mensagens) por meio da semântica padronizada dos métodos HTTP (POST, GET e PATCH)
* Comunicação sem estado (stateless): cada requisição tem tudo que o servidor precisa para processar, ou seja, a arquitetura fica mais simples.

## Dicionários e Listas
Servem para manter o estado da aplicação em totalmente em memória, já que não foi solicitado que utilizasse um banco de dados persistente.

## Bibliotecas e funções
**Request**:
- serve para fazer requisições HTTP de forma simples, rápida e intuitiva; 
- consegue conversar com servidores web, consumir APIs, baixar arquivos e extrair dados; 
- lida com dados em formato JSON.

**Jsonify**: origina do flask e é uma função usada para converter estruturas de dados nativos do python em formato de resposta JSON adequado para a API.

## Dockerfile
Define como o ambiente da aplicação é montado do zero, empacotando o python e a biblioteca flask

**Dockerfile do servidor**: "EXPOSE 5000 + WORKDIR /app": organiza a estrutura interna do contâiner e sinaliza que o serviço vai disponibilizar a API na porta 5000.

## Execução

É necessário possuir Docker instalado e em execução.

Na pasta raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando constrói as imagens e inicia o servidor e os três clientes.

Para encerrar os containers:

```bash
docker compose down
```
