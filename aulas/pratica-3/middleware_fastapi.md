[Voltar ao início](../../README.md)
---

## Prática 3 - Middleware com FastAPI

Nesta prática, vamos explorar os métodos HTTP básicos utilizados em arquiteturas REST (Representational State Transfer) utilizando o framework Python **FastAPI**. Vamos demonstrar como utilizar cada método HTTP com exemplos práticos, incluindo o uso de *query parameters*, *path parameters* e *request body*.

### Pré-requisitos

- **Postman:** para testes de API. [Download Postman](https://www.postman.com/downloads/)
- **Docker Desktop:** para executar a aplicação em container. [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Entendendo os Métodos HTTP

Os métodos HTTP são utilizados para definir a ação desejada ao acessar um recurso em um servidor web. A seguir, veremos os métodos mais comuns:

1. **GET**: Recupera dados de um servidor sem causar efeitos colaterais.
2. **POST**: Envia dados para o servidor para criar um novo recurso.
3. **PUT**: Atualiza um recurso existente com dados enviados na requisição.
4. **DELETE**: Remove um recurso específico do servidor.
5. **PATCH**: Aplica modificações parciais a um recurso existente.

- [MDN: Metodos HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Methods)
- [Devmedia: Metodos HTTP](https://www.devmedia.com.br/servicos-restful-verbos-http/37103)

## Exemplos em Python com FastAPI

### Instalação do FastAPI e Uvicorn

Antes de começar, instale o FastAPI e o Uvicorn (servidor ASGI utilizado para rodar a aplicação):

```bash
pip install fastapi uvicorn
```

### Código do Servidor com FastAPI

Crie ou edite o arquivo `main.py` com o seguinte conteúdo:

```python
from fastapi import FastAPI
from pydantic import BaseModel

# Definindo a classe para o corpo da requisição
class User(BaseModel):
    name: str

app = FastAPI()

# Método GET - Rota raiz
@app.get("/")
async def hello_world():
    return {"message": "Hello, FastAPI!"}

# Método GET - Retorna uma saudação usando um query parameter
@app.get("/api/v1/hello")
async def hello_name_via_query(name: str):
    return {"message": f"Hello {name}"}

# Método GET - Retorna uma saudação usando um path parameter
@app.get("/api/v1/hello/{name}")
async def hello_name_via_path(name: str):
    return {"message": f"Hello {name}"}

# Método POST - Retorna uma saudação utilizando o nome do usuário no corpo da requisição
@app.post("/api/v1/hello")
async def hello_name(user: User):
    return {"message": f"Hello {user.name}"}

# Método PUT - Atualiza um recurso com o nome do usuário
@app.put("/api/v1/update")
async def put_update(user: User):
    return {"message": f"Recurso atualizado com o nome: {user.name}"}

# Método DELETE - Deleta um recurso pelo nome do usuário passado via query parameter
@app.delete("/api/v1/delete")
async def delete_name(name: str):
    return {"message": f"Recurso deletado com o nome: {name}"}

# Método PATCH - Aplica uma modificação parcial ao recurso com o nome do usuário no corpo da requisição
@app.patch("/api/v1/patch")
async def patch_name(user: User):
    return {"message": f"Modificação parcial aplicada ao recurso com o nome: {user.name}"}
```

### Explicação do Código

- **`User` (classe BaseModel):** Define a classe `User` que possui o atributo `name`. Todas as rotas que precisam receber dados via *request body* aceitam um objeto do tipo `User`.
- **Rota raiz (`hello_world`):** Um exemplo simples de uma rota GET que retorna uma mensagem "Hello, FastAPI!".
- **Rotas GET com *query parameter* e *path parameter*:**
  - *Query Parameter*: O parâmetro é passado na URL, por exemplo: `http://127.0.0.1:8000/api/v1/hello?name=Lucas`.
  - *Path Parameter*: O parâmetro faz parte do caminho da URL, por exemplo: `http://127.0.0.1:8000/api/v1/hello/Lucas`.
- **Rotas POST, PUT, DELETE e PATCH:** Estas rotas aceitam um corpo de requisição ou parâmetros e retornam uma resposta apropriada, demonstrando como usar cada método HTTP.

### Rodando o Servidor FastAPI

Para rodar o servidor, utilize:

```bash
uvicorn main:app --reload
```

Este comando iniciará o servidor na URL `http://127.0.0.1:8000`. A flag `--reload` faz com que o servidor reinicie automaticamente quando mudanças no código forem detectadas.

### Testando a API com o Postman

 - [Criando teste de API](postman/postman.md)

### Dockerizando a Aplicação FastAPI

Para executar o backend utilizando Docker, crie um `Dockerfile` para construir uma imagem Docker da aplicação:

### Dockerfile

```Dockerfile
# Usando uma imagem base do Python
FROM python:3.10-slim

# Instalando dependências
RUN pip install fastapi uvicorn

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o código para o container
COPY main.py .

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Construindo e Rodando a Imagem Docker

Execute os seguintes comandos no terminal para construir a imagem Docker e rodar o container:

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

- **docker build -t fastapi-app .**: Constrói a imagem Docker com o nome `fastapi-app`.
- **docker run -p 8000:8000 fastapi-app**: Roda o container e mapeia a porta `8000` do host para a porta `8000` do container.

### Executando o Backend com Docker Compose

Para executar o backend com docker compose, crie um arquivo `docker-compose.yml` na raiz do repositório com o seguinte conteúdo:

```yml
version: '3'
services:

  backend:
    build: ./backend
    restart: always
    ports:
      - "8000:8000"
```

Execute o comando `docker-compose up --build` no terminal da raiz para iniciar o backend.

- **docker compose up --build**: Executa o docker compose e inicia o backend na porta `8000`.


### Exercício Proposto

1. Implemente os métodos HTTP apresentados.
2. Execute o backend utilizando Docker Compose.
3. Desenvolva uma suíte de testes no Postman (pode usar a da aula como base).
4. Rode os testes e exporte os resultados.
5. Suba os resultados na pasta `pratica-3/api-tests`.
6. Suba os prints solicitados na `pratica-3/img`.
7. Suba a collection editada na `pratica-3/postman`.

Prints:
- Summary dos resultados do postman
- Logs do container
- Print do Docker Desktop rodando o container (ou docker ps -a)

### Observação Importante

#### Garantir que o repositório contenha o arquivo `.gitignore` com o conteúdo abaixo:

```gitignore
__pycache__/
.env
```

Isso fará com que arquivos desnecessários não sejam enviados ao Git.

---

Este material cobre a introdução aos métodos HTTP com FastAPI, incluindo como construir e testar uma API e empacotá-la usando Docker. Na próxima aula, aprenderemos como criar um repositório e manipular dados com FastAPI.

---
[Voltar ao início](../../README.md)