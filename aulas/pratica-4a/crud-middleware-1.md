[Voltar ao início](../../README.md)
---

### Prática 4a - CRUD com Middleware

Nesta prática, vamos evoluir o sistema de estoque de livros desenvolvido na aula anterior para uma API completa usando FastAPI, seguindo o padrão de rotas `/api/v1/`. O sistema permitirá **criar**, **listar**, **buscar por ID** e **vender livros**. Além disso, faremos a integração de um **middleware** para logging de requisições e retornos. No final, você irá criar testes para validar a API usando Postman.

---

### Pré-requisitos

- Docker para executar a API: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Postman para testes: [Download Postman](https://www.postman.com/downloads/)

### Documentação do FastAPI

[Documentação](https://fastapi.tiangolo.com/tutorial/first-steps/)

---

### Endpoints da API:

- `POST /api/v1/livros/`: Adiciona um novo livro ao estoque.
- `GET /api/v1/livros/`: Lista todos os livros disponíveis.
- `GET /api/v1/livros/{livro_id}`: Busca um livro pelo ID.
- `PUT /api/v1/livros/{livro_id}/vender/`: Vende uma quantidade de um livro, diminuindo o estoque.
- `PATCH /api/v1/livros/{livro_id}`: Atualiza os atributos de um livro.
- `DELETE /api/v1/livros/{livro_id}`: Remove um livro do estoque.
- `DELETE /api/v1/livros/`: Remove todos os livros adicionados do estoque e restaura o repositório para o estado inicial.

---

### Estrutura da API com FastAPI

#### Código da API

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time


# Inicializar o repositório de livros (armazenado na memória)
livros = [
    {"id": 1, "titulo": "Livro A", "autor": "Autor A", "quantidade": 10, "preco": 50.0},
    {"id": 2, "titulo": "Livro B", "autor": "Autor B", "quantidade": 5, "preco": 40.0},
]

# Inicializar a aplicação FastAPI
app = FastAPI()


# Modelo para adicionar novos livros
class Livro(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    quantidade: int
    preco: float

# Modelo para venda de livros
class VendaLivro(BaseModel):
    quantidade: int


# Modelo para atualizar atributos de um livro (exceto o ID)
class AtualizarLivro(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    quantidade: Optional[int] = None
    preco: Optional[float] = None

# Função para gerar o próximo ID dinamicamente
def gerar_proximo_id():
    if livros:
        return max(livro['id'] for livro in livros) + 1
    else:
        return 1

# Função auxiliar para buscar livro por ID
def buscar_livro_por_id(livro_id: int):
    for livro in livros:
        if livro["id"] == livro_id:
            return livro
    return None

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# 1. Adicionar um novo livro
@app.post("/api/v1/livros/", status_code=201)
def adicionar_livro(livro: Livro):
    # Verificar se o livro já existe
    for l in livros:
        if l["autor"].lower() == livro.autor.lower() and l["titulo"].lower() == livro.titulo.lower():
            raise HTTPException(status_code=400, detail="Livro já existe.")
    
    # Gerar ID dinamicamente
    novo_livro = livro.dict()
    novo_livro['id'] = gerar_proximo_id()

    # Adicionar o novo livro ao repositório
    livros.append(novo_livro)
    return {"message": "Livro adicionado com sucesso!", "livro": novo_livro}

# 2. Listar todos os livros
@app.get("/api/v1/livros/", response_model=List[Livro])
def listar_livros():
    return livros

# 3. Buscar livro por ID
@app.get("/api/v1/livros/{livro_id}")
def listar_livro_por_id(livro_id: int):
    livro = buscar_livro_por_id(livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro

# 4. Vender um livro (reduzir quantidade no estoque)
@app.put("/api/v1/livros/{livro_id}/vender/")
def vender_livro(livro_id: int, venda: VendaLivro):
    livro = buscar_livro_por_id(livro_id)
    
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    
    if livro["quantidade"] < venda.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")
    
    livro["quantidade"] -= venda.quantidade
    return {"message": "Venda realizada com sucesso!", "livro": livro}


# 5. Atualizar atributos de um livro pelo ID (exceto o ID)
@app.patch("/api/v1/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizacao: AtualizarLivro):
    livro = buscar_livro_por_id(livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    
    # Atualizar apenas os campos fornecidos no body
    if livro_atualizacao.titulo is not None:
        livro["titulo"] = livro_atualizacao.titulo
    if livro_atualizacao.autor is not None:
        livro["autor"] = livro_atualizacao.autor
    if livro_atualizacao.quantidade is not None:
        livro["quantidade"] = livro_atualizacao.quantidade
    if livro_atualizacao.preco is not None:
        livro["preco"] = livro_atualizacao.preco

    return {"message": "Livro atualizado com sucesso!", "livro": livro}


# 6. Remover um livro pelo ID
@app.delete("/api/v1/livros/{livro_id}")
def remover_livro(livro_id: int):
    for i, livro in enumerate(livros):
        if livro["id"] == livro_id:
            del livros[i]
            return {"message": "Livro removido com sucesso!"}
        

# 7. Resetar repositorio de livros
@app.delete("/api/v1/livros/")
def resetar_livros():
    global livros
    livros = [
    {"id": 1, "titulo": "Livro A", "autor": "Autor A", "quantidade": 10, "preco": 50.0},
    {"id": 2, "titulo": "Livro B", "autor": "Autor B", "quantidade": 5, "preco": 40.0},
    ]
    return {"message": "Repositorio limpo com sucesso!", "livros": livros}
```

---

### Explicação das Funcionalidades:

1. **Adicionar Livro**:
   - O endpoint `POST /api/v1/livros/` adiciona um novo livro ao repositório.
   - Verifica se o livro já existe no repositório comparando pelo `id` ou pelo `título`.

2. **Listar Livros**:
   - O endpoint `GET /api/v1/livros/` lista todos os livros presentes no repositório.

3. **Listar Livro por ID**:
   - O endpoint `GET /api/v1/livros/{livro_id}` permite buscar um livro específico pelo seu `ID`.

4. **Vender Livro**:
   - O endpoint `PUT /api/v1/livros/{livro_id}/vender/` permite vender uma quantidade de um livro.
   - Verifica se a quantidade solicitada está disponível no estoque e atualiza a quantidade do livro.

5. **Atualizar Livro**: 
   - O endpoint `PATCH /api/v1/livros/{livro_id}` permite atualizar os atributos de um livro, exceto o `ID`.
   - Atualiza apenas os campos fornecidos no corpo da requisição.

6. **Remover Livro**: 
   - O endpoint `DELETE /api/v1/livros/{livro_id}` permite remover um livro do repositório.

7. **Resetar o repositório**:
   - O endpoint `DELETE /api/v1/livros/` permite remover todos os livros do repositório, e restaurar o repositório para o estado inicial, contendo apenas os 2 livros de exemplo.

8. **(BUNUS) Middleware de Logging**:
   - Adicionamos um middleware que registra o **tempo de processamento** e informações da requisição, como o método HTTP e o caminho da URL.

---

### Como Executar a API no ambiente local:

1. **Instalar as dependências**:
   Certifique-se de que o FastAPI e o Uvicorn estão instalados:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Executar o servidor**:
   Rode o servidor usando o Uvicorn:
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **Testar os Endpoints**:
   Acesse a documentação interativa do FastAPI:
   ```
   http://127.0.0.1:8000/docs
   ```

---

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


### Testando a API com o Postman

 - [Criando testes da API](postman/postman.md)

---

### Exercício Proposto:

1. Implementar o CRUD completo do **seu gerenciador de estoque da pratica-1** usando FastAPI.
2. Executar a API usando docker-compose (**OBRIGATÓRIO**).
3. Criar uma **collection** no Postman usando os testes de exemplo em [Criando teste de API](postman/postman.md)
4. Subir a **collection** e os **resultados** na pasta `pratica-4a/api-tests`.
5. Tirar prints dos resultados e subir na pasta `pratica-4a/img`.

Prints:
- Summary dos resultados do postman
- Logs do container contendo as chamadas na API.

### Observação Importante

## ENTREGAR O PROJETO COM A MESMA ESTRUTURA!
```sh
 - aulas/
    - pratica-x/ # o x é o número da prática
       - api-tests/ # aqui vão os arquivos de testes do postman (collection e test run)
          - C216-L1-PRATICA-x-Nome_Matricula.postman_collection.json
          - C216-L1-PRATICA-x-Nome_Matricula.postman_test_run.json
       - img/ # aqui vão os prints solicitados
          - logs-api.png
          - postman.png
 - backend/ # o backend deve estar na raiz do repositório
    - main.py
    - Dockerfile
    - requirements.txt
docker-compose.yml
```
---
[Voltar ao início](../../README.md)
