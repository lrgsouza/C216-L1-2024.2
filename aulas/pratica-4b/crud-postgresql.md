
[Voltar ao início](../../README.md)
---

### Prática 4b - Acessando Postgresql via Middleware

Nesta prática, vamos evoluir o sistema de estoque de livros desenvolvido na aula anterior para utilizar o PostgreSQL. Utilizaremos a biblioteca asyncpg pela sua facilidade de implementação e entendimento.

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
- `GET /api/v1/vendas/`: Lista todas as vendas.
- `PUT /api/v1/livros/{livro_id}/vender/`: Vende uma quantidade de um livro, diminuindo o estoque.
- `PATCH /api/v1/livros/{livro_id}`: Atualiza os atributos de um livro.
- `DELETE /api/v1/livros/{livro_id}`: Remove um livro do estoque.
- `DELETE /api/v1/livros/`: Remove todos os livros adicionados do estoque e restaura o repositório para o estado inicial.

---

### Script de criação da base de dados e tabelas

```sql

DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "livros";

CREATE TABLE "livros" (
    "id" SERIAL PRIMARY KEY,
    "titulo" VARCHAR(255) NOT NULL,
    "autor" VARCHAR(255) NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "preco" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "livro_id" INTEGER REFERENCES livros(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('O Senhor dos Anéis', 'J.R.R. Tolkien', 10, 50.00);
INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('Harry Potter', 'J.K. Rowling', 20, 30.00);
INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('1984', 'George Orwell', 15, 40.00)

```
Este script deve ser executado assim que a API subir pois ele cria as tabelas e preenche os dados iniciais. Para resetar a base de dados, basta executar a chamada `DELETE` na API no path `/api/v1/livros/`.

### Estrutura da API com FastAPI

#### Código da API

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/livros") 
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Modelo para adicionar novos livros
class Livro(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    quantidade: int
    preco: float

class LivroBase(BaseModel):
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

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# Função para verificar se o livro existe usado autor e nome do livro
async def livro_existe(titulo: str, autor: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM livros WHERE LOWER(titulo) = LOWER($1) AND LOWER(autor) = LOWER($2)"
        result = await conn.fetchval(query, titulo, autor)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se o livro existe: {str(e)}")

# 1. Adicionar um novo livro
@app.post("/api/v1/livros/", status_code=201)
async def adicionar_livro(livro: LivroBase):
    conn = await get_database()
    if await livro_existe(livro.titulo, livro.autor, conn):
        raise HTTPException(status_code=400, detail="Livro já existe.")
    try:
        query = "INSERT INTO livros (titulo, autor, quantidade, preco) VALUES ($1, $2, $3, $4)"
        async with conn.transaction():
            result = await conn.execute(query, livro.titulo, livro.autor, livro.quantidade, livro.preco)
            return {"message": "Livro adicionado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar o livro: {str(e)}")
    finally:
        await conn.close()

# 2. Listar todos os livros
@app.get("/api/v1/livros/", response_model=List[Livro])
async def listar_livros():
    conn = await get_database()
    try:
        # Buscar todos os livros no banco de dados
        query = "SELECT * FROM livros"
        rows = await conn.fetch(query)
        livros = [dict(row) for row in rows]
        return livros
    finally:
        await conn.close()

# 3. Buscar livro por ID
@app.get("/api/v1/livros/{livro_id}")
async def listar_livro_por_id(livro_id: int):
    conn = await get_database()
    try:
        # Buscar o livro por ID
        query = "SELECT * FROM livros WHERE id = $1"
        livro = await conn.fetchrow(query, livro_id)
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")
        return dict(livro)
    finally:
        await conn.close()

# 4. Vender um livro (reduzir quantidade no estoque)
@app.put("/api/v1/livros/{livro_id}/vender/")
async def vender_livro(livro_id: int, venda: VendaLivro):
    conn = await get_database()
    try:
        # Verificar se o livro existe
        query = "SELECT * FROM livros WHERE id = $1"
        livro = await conn.fetchrow(query, livro_id)
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        # Verificar se a quantidade no estoque é suficiente
        if livro['quantidade'] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")

        # Atualizar a quantidade no banco de dados
        nova_quantidade = livro['quantidade'] - venda.quantidade
        update_query = "UPDATE livros SET quantidade = $1 WHERE id = $2"
        await conn.execute(update_query, nova_quantidade, livro_id)


        # Calcular o valor total da venda
        valor_venda = livro['preco'] * venda.quantidade
        # Registrar a venda na tabela de vendas
        insert_venda_query = """
            INSERT INTO vendas (livro_id, quantidade_vendida, valor_venda) 
            VALUES ($1, $2, $3)
        """
        await conn.execute(insert_venda_query, livro_id, venda.quantidade, valor_venda)

        # Criar um novo dicionário com os dados atualizados
        livro_atualizado = dict(livro)
        livro_atualizado['quantidade'] = nova_quantidade

        return {"message": "Venda realizada com sucesso!", "livro": livro_atualizado}
    finally:
        await conn.close()

# 5. Atualizar atributos de um livro pelo ID (exceto o ID)
@app.patch("/api/v1/livros/{livro_id}")
async def atualizar_livro(livro_id: int, livro_atualizacao: AtualizarLivro):
    conn = await get_database()
    try:
        # Verificar se o livro existe
        query = "SELECT * FROM livros WHERE id = $1"
        livro = await conn.fetchrow(query, livro_id)
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        # Atualizar apenas os campos fornecidos
        update_query = """
            UPDATE livros
            SET titulo = COALESCE($1, titulo),
                autor = COALESCE($2, autor),
                quantidade = COALESCE($3, quantidade),
                preco = COALESCE($4, preco)
            WHERE id = $5
        """
        await conn.execute(
            update_query,
            livro_atualizacao.titulo,
            livro_atualizacao.autor,
            livro_atualizacao.quantidade,
            livro_atualizacao.preco,
            livro_id
        )
        return {"message": "Livro atualizado com sucesso!"}
    finally:
        await conn.close()

# 6. Remover um livro pelo ID
@app.delete("/api/v1/livros/{livro_id}")
async def remover_livro(livro_id: int):
    conn = await get_database()
    try:
        # Verificar se o livro existe
        query = "SELECT * FROM livros WHERE id = $1"
        livro = await conn.fetchrow(query, livro_id)
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        # Remover o livro do banco de dados
        delete_query = "DELETE FROM livros WHERE id = $1"
        await conn.execute(delete_query, livro_id)
        return {"message": "Livro removido com sucesso!"}
    finally:
        await conn.close()

# 7. Resetar repositorio de livros
@app.delete("/api/v1/livros/")
async def resetar_livros():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!!"}
    finally:
        await conn.close()


# 8 . Listar vendas
@app.get("/api/v1/vendas/")
async def listar_vendas():
    conn = await get_database()
    try:
        # Buscar todas as vendas no banco de dados
        query = "SELECT * FROM vendas"
        rows = await conn.fetch(query)
        vendas = [dict(row) for row in rows]
        return vendas
    finally:
        await conn.close()
```

---

### Explicação das Funcionalidades:

1. **Adicionar Livro**:
   - O endpoint `POST /api/v1/livros/` adiciona um novo livro ao banco de dados.
   - Verifica se o livro já existe no banco de dados comparando pelo `id` ou pelo `título`.

2. **Listar Livros**:
   - O endpoint `GET /api/v1/livros/` lista todos os livros presentes no banco de dados.

3. **Listar Livro por ID**:
   - O endpoint `GET /api/v1/livros/{livro_id}` permite buscar um livro específico pelo seu `ID`.

4. **Vender Livro**:
   - O endpoint `PUT /api/v1/livros/{livro_id}/vender/` permite vender uma quantidade de um livro.
   - Verifica se a quantidade solicitada está disponível no estoque e atualiza a quantidade do livro.

5. **Atualizar Livro**: 
   - O endpoint `PATCH /api/v1/livros/{livro_id}` permite atualizar os atributos de um livro, exceto o `ID`.
   - Atualiza apenas os campos fornecidos no corpo da requisição.

6. **Remover Livro**: 
   - O endpoint `DELETE /api/v1/livros/{livro_id}` permite remover um livro do banco de dados.

7. **Resetar o banco de dados**:
   - O endpoint `DELETE /api/v1/livros/` permite remover todos os livros do banco de dados, e restaurar o banco de dados para o estado inicial.

8. **Listar Vendas**:
   - O endpoint `GET /api/v1/vendas/` lista todas as vendas registradas no banco de dados.

---

### Como Executar a API no ambiente local:

1. **Instalar as dependências**:
   Certifique-se de que o FastAPI e o Uvicorn estão instalados:
   ```bash
   pip install fastapi uvicorn asyncpg
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
services:

  backend:
    build: ./backend
    restart: always
    ports:
      - "8000:8000"
  db:
    image: postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: livros
```

Execute o comando `docker-compose up --build` no terminal da raiz para iniciar o backend.

- **docker compose up --build**: Executa o docker compose e inicia o backend na porta `8000`.


### Testando a API com o Postman

 - [Criando testes da API](postman/postman.md)

---

### Exercício Proposto:

1. Atualizar sua API para usar o PostgreSQL como seu banco de dados.
2. Executar a API usando docker-compose (**OBRIGATÓRIO**).
3. Criar uma **collection** no Postman usando os testes de exemplo em [Criando teste de API](postman/postman.md)
4. Subir a **collection** e os **resultados** na pasta `pratica-4b/api-tests`.
5. Tirar prints dos resultados e subir na pasta `pratica-4b/img`.

Prints:
- Summary dos resultados do postman
- Logs do container contendo as chamadas na API.

### Observação Importante

 - Sua API não pode ser genérica! Você precisa definir um produto (carro, bicicleta, etc)!
    - Se realizar a entrega de uma API generica será descontado 10 pontos.
 - Todo produto deve ter preço! Pois sem o preço não se calcula venda!
    - Se realizar a entrega de um produto sem o valor, será descontado 10 pontos.
 - Alem de preço e quantidade, cada produto deve ter pelo menos 2 atributos adicionais. (cor, ano, etc)
    - Se realizar a entrega de um produto sem os atributos adicionais, será descontado 10 pontos.
- Você pode usar livro como produto. Porém seu código não poderá ser igual ao meu!
    - Se realizar a entrega do código muito semelhante ao meu, sua entrega será ZERADA!

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
    - db/
       - init.sql
    - main.py
    - Dockerfile
docker-compose.yml
```
---
[Voltar ao início](../../README.md)
