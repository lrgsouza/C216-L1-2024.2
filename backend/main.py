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
