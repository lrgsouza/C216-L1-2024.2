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