# DistributedServiceAPIRest
Implementação de serviço distribuído de comunicação com API REST utilizando contâineres para implementar servidor e clientes orquestrados por um Docker Compose, utilizando o protocolo HTTP como contrato de comunicação desacoplado e transparente.

**Desafio:** fazer com que processos independentes consigam trocar informações sem compartilhar memória interna.

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
