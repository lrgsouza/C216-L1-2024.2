### Postman Collection - FastAPI HTTP Methods

- [Documentação Postman](https://learning.postman.com/docs/getting-started/overview/)
#### Passos para Criar a Coleção:

1. **Abra o Postman** e clique em **New** > **Collection**.
2. Nomeie a coleção como `C216-L1-PRATICA-3-Lucas_GES134`.
3. Clique no botão **Add Request** para adicionar uma nova requisição.
4. Para os testes utilizar seu nome_matricula!
5. Para cada método HTTP, crie uma nova requisição conforme descrito abaixo:

#### 0. GET Request com Rota Raiz
- **Nome:** `GET - Hello World`
- **Método:** `GET`
- **URL:** `http://localhost:8000/`
- **Descrição:** Testa o endpoint GET.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response contains 'Hello, FastAPI!'", function () {
        pm.expect(pm.response.text()).to.include("Hello, FastAPI!");
    });
    ``` 

#### 1. GET Request com Query Parameter
- **Nome:** `GET - Hello via Query Parameter`
- **Método:** `GET`
- **URL:** `http://localhost:8000/api/v1/hello?name=Lucas_GES134`
- **Descrição:** Testa o endpoint GET usando um *query parameter*.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response contains 'Hello Lucas_GES134'", function () {
        pm.expect(pm.response.json().message).to.eql("Hello Lucas_GES134");
    });
    ```

#### 2. GET Request com Path Parameter
- **Nome:** `GET - Hello via Path Parameter`
- **Método:** `GET`
- **URL:** `http://localhost:8000/api/v1/hello/Lucas_GES134`
- **Descrição:** Testa o endpoint GET usando um *path parameter*.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response contains 'Hello Lucas_GES134'", function () {
        pm.expect(pm.response.json().message).to.eql("Hello Lucas_GES134");
    });
    ```

#### 3. POST Request com Request Body
- **Nome:** `POST - Hello via Body`
- **Método:** `POST`
- **URL:** `http://localhost:8000/api/v1/hello`
- **Headers:** 
    - `Content-Type: application/json`
- **Body:** 
    - Tipo: `raw`
    - Formato: `JSON`
    ```json
    {
        "name": "Lucas_GES134"
    }
    ```
- **Descrição:** Testa o endpoint POST enviando o nome via *request body*.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response contains 'Hello Lucas_GES134'", function () {
        pm.expect(pm.response.json().message).to.eql("Hello Lucas_GES134");
    });
    ```

#### 4. PUT Request para Atualização
- **Nome:** `PUT - Update Name`
- **Método:** `PUT`
- **URL:** `http://localhost:8000/api/v1/update`
- **Headers:** 
    - `Content-Type: application/json`
- **Body:** 
    - Tipo: `raw`
    - Formato: `JSON`
    ```json
    {
        "name": "Lucas_GES134_New"
    }
    ```

- **Descrição:** Testa o endpoint PUT atualizando o nome.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response contains updated name", function () {
        pm.expect(pm.response.json().message).to.eql("Recurso atualizado com o nome: Lucas_GES134_New");
    });
    ```

#### 5. DELETE Request com Query Parameter
- **Nome:** `DELETE - Delete Resource`
- **Método:** `DELETE`
- **URL:** `http://localhost:8000/api/v1/delete?name=Lucas_GES134`
- **Descrição:** Testa o endpoint DELETE deletando o recurso pelo nome passado como *query parameter*.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response confirms deletion", function () {
        pm.expect(pm.response.json().message).to.eql("Recurso deletado com o nome: Lucas_GES134");
    });
    ```

#### 6. PATCH Request para Modificação Parcial
- **Nome:** `PATCH - Modify Resource`
- **Método:** `PATCH`
- **URL:** `http://localhost:8000/api/v1/patch`
- **Headers:** 
    - `Content-Type: application/json`
- **Body:** 
    - Tipo: `raw`
    - Formato: `JSON`
    ```json
    {
        "name": "Lucas_GES134"
    }
    ```
- **Descrição:** Testa o endpoint PATCH aplicando uma modificação parcial ao recurso.
- **Testes:** 
    ```javascript
    pm.test("Status code is 200", function () {
        pm.response.to.have.status(200);
    });
    pm.test("Response confirms partial modification", function () {
        pm.expect(pm.response.json().message).to.eql("Modificação parcial aplicada ao recurso com o nome: Lucas_GES134");
    });
    ```

### Exportando a Collection do Postman

Após criar todas as requisições:

1. Clique com o botão direito na coleção `FastAPI HTTP Methods`.
2. Selecione **Export** e escolha o formato `Collection v2.1`.
3. Salve o arquivo `.json` exportado.

### Conclusão

Esta coleção cobre todos os métodos HTTP apresentados na prática, utilizando diferentes formas de passar parâmetros e corpos de requisição. Ela ajudará a testar a aplicação FastAPI implementada na aula, garantindo que cada endpoint funcione corretamente.

---

[Voltar](../middleware_fastapi.md)