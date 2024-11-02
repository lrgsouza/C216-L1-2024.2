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
            INSERT INTO vendas (livro_id, titulo, quantidade_vendida, valor_venda) 
            VALUES ($1, $2, $3, $4)
        """
        await conn.execute(insert_venda_query, livro_id, livro['titulo'], venda.quantidade, valor_venda)

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

# 7. Resetar banco de dados de livros
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
        return {"message": "Banco de dados limpo com sucesso!"}
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