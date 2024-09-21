## Criando uma Postman Collection para a API de gerenciamento de estoque

### Passos Iniciais

1. **Abra o Postman** e clique em **New** > **Collection**.
2. Nomeie a coleção como `C216-L1-PRATICA-4a-NOME_MATRICULA`.
3. Para cada método HTTP, você deve criar uma nova requisição conforme descrito abaixo.

### 1. **GET - Listar todos os livros**
- **Nome:** `GET - Listar todos os livros`
- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/v1/livros`
- **Descrição:** Testa o endpoint para listar todos os livros cadastrados.
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should be a list", function () {
        pm.expect(pm.response.json()).to.be.an('array');
    });
    ```

### 2. **GET - Buscar Livro por ID**
- **Nome:** `GET - Buscar Livro por ID`
- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/v1/livros/1`
- **Descrição:** Busca um livro específico pelo ID.
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should contain book details", function () {
        pm.expect(pm.response.json()).to.have.property('titulo');
    });
    ```

### 3. **POST - Adicionar um Livro**
- **Nome:** `POST - Adicionar um Livro`
- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/v1/livros`
- **Headers:** 
    - `Content-Type: application/json`
- **Body (JSON):**
    ```json
    {
      "titulo": "Clean Code",
      "autor": "Robert C. Martin",
      "ano_publicacao": 2008,
      "quantidade": 5
    }
    ```
- **Descrição:** Adiciona um novo livro ao repositório.
- **Testes:**
    ```javascript
    pm.test("Status code is 201", function () {
        pm.response.to.have.status(201);
    });
    pm.test("Response should contain confirmation message", function () {
        pm.expect(pm.response.json().message).to.eql('Livro adicionado com sucesso!');
    });
    ```

### 4. **PUT - Vender um Livro**
- **Nome:** `PUT - Vender um Livro`
- **Método:** `PUT`
- **URL:** `http://127.0.0.1:8000/api/v1/livros/1/vender`
- **Descrição:** Deduz uma unidade da quantidade de um livro ao realizar uma venda.
- **Headers:** 
    - `Content-Type: application/json`
- **Body (JSON):**
    ```json
    {
      "quantidade": 2
    }
    ```
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should confirm sale", function () {
        pm.expect(pm.response.json().message).to.eql('Venda realizada com sucesso!');
    });

    // Validar se a quantidade foi reduzida
    pm.sendRequest("http://127.0.0.1:8000/api/v1/livros/1", function (err, res) {
        pm.test("Quantidade do livro foi atualizada", function () {
            let book = res.json();
            pm.expect(book.quantidade).to.eql(8); // A quantidade deve ter sido reduzida
        });
    });
    ```

### 5. **PATCH - Atualizar Atributos de um Livro**
- **Nome:** `PATCH - Atualizar Atributos de um Livro`
- **Método:** `PATCH`
- **URL:** `http://127.0.0.1:8000/api/v1/livros/3`
- **Headers:** 
    - `Content-Type: application/json`
- **Body (JSON):**
    ```json
    {
      "titulo": "Clean Code - Revised Edition",
      "autor": "Robert C. Martin",
      "ano_publicacao": 2020,
      "quantidade": 10
    }
    ```
- **Descrição:** Atualiza os atributos de um livro, exceto o ID.
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should confirm update", function () {
        pm.expect(pm.response.json().message).to.eql('Livro atualizado com sucesso!');
    });

    // Validar se o livro foi atualizado corretamente
    pm.sendRequest("http://127.0.0.1:8000/api/v1/livros/3", function (err, res) {
        pm.test("Os atributos do livro foram atualizados", function () {
            let book = res.json();
            pm.expect(book.titulo).to.eql("Clean Code - Revised Edition");
            pm.expect(book.autor).to.eql("Robert C. Martin");
            pm.expect(book.ano_publicacao).to.eql(2020);
            pm.expect(book.quantidade).to.eql(10); // Verifica se a quantidade foi alterada
        });
    });
    ```

### 6. **DELETE - Remover um Livro**
- **Nome:** `DELETE - Remover um Livro`
- **Método:** `DELETE`
- **URL:** `http://127.0.0.1:8000/api/v1/livros/1`
- **Descrição:** Remove um livro do repositório pelo ID.
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should confirm deletion", function () {
        pm.expect(pm.response.json().message).to.eql('Livro removido com sucesso!');
    });
    ```

### 7. **DELETE - Remover Todos os Livros**
- **Nome:** `DELETE - Remover Todos os Livros (RESETAR REPOSITORIO)`
- **Método:** `DELETE`
- **URL:** `http://127.0.0.1:8000/api/v1/livros`
- **Descrição:** Remove todos os livros do repositório.
- **Testes:**
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response should confirm deletion", function () {
        pm.expect(pm.response.json().message).to.eql('Repositorio limpo com sucesso!');
    });
    ```

---

### Executando os Testes
-

Para cada requisição, você pode configurar os parâmetros do corpo (quando necessário) e clicar em **Send** para enviar a solicitação. A resposta será exibida na aba de resposta, e os testes que foram escritos acima serão executados automaticamente, com os resultados sendo exibidos na aba **Tests**.

### Resumo dos Passos para Testar a API:
- **Crie uma nova coleção no Postman** com o nome `Bookstore-API-FastAPI`.
- Adicione as requisições `GET`, `POST`, `PUT`, `PATCH` e `DELETE` conforme explicado.
- Execute cada requisição e observe se os testes retornam como **Pass** ou **Fail**. Caso algum teste falhe, analise a resposta e compare com os valores esperados nos testes.

Essa abordagem ajuda a garantir que a API de gerenciamento de livros esteja funcionando corretamente, com todos os métodos testados de maneira eficiente e clara.

Se precisarem de mais alguma alteração ou explicação, estou à disposição!

---
[Voltar](../crud-middleware-1.md)