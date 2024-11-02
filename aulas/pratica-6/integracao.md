[Voltar ao início](../../README.md)
---
## Prática 6 - Integração dos Sistemas Distribuídos Utilizando Containers e Docker Compose

Nesta prática, estamos atualizando nossa aplicação para integrar o **Flask** com a **API de Livros** e o banco de dados utilizando **containers** e **Docker Compose**. Abaixo, apresentamos o fluxo de chamadas à API e como renderizar os templates com as informações retornadas pela API.

---

### Objetivo da Prática

O objetivo é permitir que a aplicação Flask se comunique com a API para realizar operações de CRUD (Create, Read, Update, Delete) sobre os livros armazenados no banco de dados. Isso inclui funcionalidades como listar, cadastrar, atualizar, excluir e vender livros, além de exibir o histórico de vendas.

---

## Estrutura das Chamadas à API no Flask

Para integrar a aplicação Flask com a API de livros, usamos o módulo `requests` do Python, qual deve ser instalada no Dockerfile da aplicação. Abaixo estão as etapas para realizar chamadas à API e renderizar os templates com as respostas obtidas.

### Definindo a URL da API no Flask

```python
API_BASE_URL = "http://backend:8000"
```

Essa URL (`http://backend:8000`) é utilizada nas chamadas HTTP, e `backend` é o nome do serviço da API configurado no `docker-compose.yml`.

---

## Código Python no Flask para Integração com a API

```python
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def inserir_livro_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    payload = {
        'titulo': titulo,
        'autor': autor,
        'quantidade' : quantidade,
        'preco' : preco
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/livros/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_livros'))
    else:
        return "Erro ao inserir livro", 500

# Rota para listar todos os livros
@app.route('/estoque', methods=['GET'])
def listar_livros():
    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    try:
        livros = response.json()
    except:
        livros = []
    return render_template('estoque.html', livros=livros)

# Rota para exibir o formulário de edição de livro
@app.route('/atualizar/<int:livro_id>', methods=['GET'])
def atualizar_livro_form(livro_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/livros/")
    #filtrando apenas o livro correspondente ao ID
    livros = [livro for livro in response.json() if livro['id'] == livro_id]
    if len(livros) == 0:
        return "livro não encontrado", 404
    livro = livros[0]
    return render_template('atualizar.html', livro=livro)

# Rota para enviar os dados do formulário de edição de livro para a API
@app.route('/atualizar/<int:livro_id>', methods=['POST'])
def atualizar_livro(livro_id):
    titulo = request.form['titulo']
    autor = request.form['autor']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    payload = {
        'id': livro_id,
        'titulo': titulo,
        'autor': autor,
        'quantidade' : quantidade,
        'preco' : preco
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/livros/{livro_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_livros'))
    else:
        return "Erro ao atualizar livro", 500

# Rota para exibir o formulário de edição de livro
@app.route('/vender/<int:livro_id>', methods=['GET'])
def vender_livro_form(livro_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/livros/")
    #filtrando apenas o livro correspondente ao ID
    livros = [livro for livro in response.json() if livro['id'] == livro_id]
    if len(livros) == 0:
        return "livro não encontrado", 404
    livro = livros[0]
    return render_template('vender.html', livro=livro)

# Rota para vender um livro
@app.route('/vender/<int:livro_id>', methods=['POST'])
def vender_livro(livro_id):
    quantidade = request.form['quantidade']

    payload = {
        'quantidade': quantidade
    }

    response = requests.put(f"{API_BASE_URL}/api/v1/livros/{livro_id}/vender/", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_livros'))
    else:
        return "Erro ao vender livro", 500

# Rota para listar todas as vendas
@app.route('/vendas', methods=['GET'])
def listar_vendas():
    response = requests.get(f"{API_BASE_URL}/api/v1/vendas/")
    try:
        vendas = response.json()
    except:
        vendas = []
    #salvando nomes dos livros vendidos
    total_vendas = 0
    for venda in vendas:
        total_vendas += float(venda['valor_venda'])
    return render_template('vendas.html', vendas=vendas, total_vendas=total_vendas)

# Rota para excluir um livro
@app.route('/excluir/<int:livro_id>', methods=['POST'])
def excluir_livro(livro_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/livros/{livro_id}")
    
    if response.status_code == 200  :
        return redirect(url_for('listar_livros'))
    else:
        return "Erro ao excluir livro", 500

#Rota para resetar o database
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/livros/")
    
    if response.status_code == 200  :
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o database", 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')

```
### Explicação do Código e exemplos de uso

### 1. Listando Todos os Livros

Na rota `/estoque`, a aplicação Flask realiza uma **chamada GET** para `/api/v1/livros/`, obtendo a lista de livros disponíveis no estoque.

```python
@app.route('/estoque', methods=['GET'])
def listar_livros():
    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    livros = response.json()
    return render_template('estoque.html', livros=livros)
```

**Explicação:**
- Utilizamos `requests.get()` para buscar os livros.
- A resposta (`livros`) é um JSON convertido em uma lista Python e passado para o template `estoque.html` para ser renderizado na página.

### 2. Cadastro de Novo Livro

Na rota `/inserir`, o Flask envia os dados coletados em um formulário para a API, utilizando uma **chamada POST**.

```python
@app.route('/inserir', methods=['POST'])
def inserir_livro():
    payload = {
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'quantidade': request.form['quantidade'],
        'preco': request.form['preco']
    }
    response = requests.post(f'{API_BASE_URL}/api/v1/livros/', json=payload)
    return redirect(url_for('listar_livros')) if response.status_code == 201 else "Erro ao inserir livro", 500
```

**Explicação:**
- Os dados do formulário são coletados com `request.form` e enviados no corpo da requisição (`json=payload`).
- Se a resposta for bem-sucedida (`201`), redirecionamos o usuário para a página de estoque.

### 3. Atualizando um Livro

Na rota `/atualizar/<int:livro_id>`, o Flask exibe um formulário com os dados atuais do livro. Quando o formulário é submetido, uma **chamada PATCH** é feita à API para atualizar as informações.

```python
@app.route('/atualizar/<int:livro_id>', methods=['POST'])
def atualizar_livro(livro_id):
    payload = {
        'id': livro_id,
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'quantidade': request.form['quantidade'],
        'preco': request.form['preco']
    }
    response = requests.patch(f"{API_BASE_URL}/api/v1/livros/{livro_id}", json=payload)
    return redirect(url_for('listar_livros')) if response.status_code == 200 else "Erro ao atualizar livro", 500
```

**Explicação:**
- Coletamos as novas informações do formulário e enviamos à API usando `requests.patch()`.
- Em caso de sucesso, redirecionamos para a página de estoque.

### 4. Venda de Livro

Na rota `/vender/<int:livro_id>`, exibimos um formulário para que o usuário insira a quantidade de livros que deseja vender. Após submissão, enviamos uma **chamada PUT** para a API.

```python
@app.route('/vender/<int:livro_id>', methods=['POST'])
def vender_livro(livro_id):
    payload = {'quantidade': request.form['quantidade']}
    response = requests.put(f"{API_BASE_URL}/api/v1/livros/{livro_id}/vender/", json=payload)
    return redirect(url_for('listar_livros')) if response.status_code == 200 else "Erro ao vender livro", 500
```

**Explicação:**
- O ID do livro e a quantidade são enviados na requisição PUT para atualizar o estoque na API.
- Em caso de sucesso, redirecionamos para a página de estoque.

### 5. Exibindo o Histórico de Vendas

Na rota `/vendas`, a aplicação realiza uma **chamada GET** para buscar o histórico de vendas na API.

```python
@app.route('/vendas', methods=['GET'])
def listar_vendas():
    response = requests.get(f"{API_BASE_URL}/api/v1/vendas/")
    vendas = response.json()
    total_vendas = sum(float(venda['valor_venda']) for venda in vendas)
    return render_template('vendas.html', vendas=vendas, total_vendas=total_vendas)
```

**Explicação:**
- A resposta JSON é convertida para uma lista Python.
- Calculamos o total de vendas e renderizamos o template `vendas.html`.

---

### Templates HTML: Renderização de Dados da API

Abaixo está o código de template HTML para exibir os dados da API de livros usando Flask e Bootstrap, uma biblioteca CSS que facilita a estilização e criação de layouts responsivos. Esse template mostra a lista de livros em estoque e fornece ações para atualizar, vender ou excluir cada livro.

#### Template `estoque.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estoque</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Estoque</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-link active" aria-current="page" href="/">Home</a>
                    <a class="nav-link" href="/cadastro">Cadastrar Livro</a>
                    <a class="nav-link" href="/estoque">Mostrar Estoque</a>
                    <a class="nav-link" href="/vendas">Mostrar Vendas Realizadas</a>
                </div>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if livros %}
            <table class="table table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Título</th>
                        <th>Autor</th>
                        <th>Quantidade</th>
                        <th>Preço</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for livro in livros %}
                    <tr>
                        <td>{{ livro.titulo }}</td>
                        <td>{{ livro.autor }}</td>
                        <td>{{ livro.quantidade }}</td>
                        <td>{{ livro.preco }}</td>
                        <td class="d-flex gap-2">
                            <form action="/excluir/{{ livro.id }}" method="POST">
                                <input type="submit" value="Excluir" class="btn btn-danger btn-sm">
                            </form>
                            <form action="/atualizar/{{ livro.id }}" method="GET">
                                <input type="submit" value="Atualizar" class="btn btn-primary btn-sm">
                            </form>
                            <form action="/vender/{{ livro.id }}" method="GET">
                                <input type="submit" value="Vender" class="btn btn-success btn-sm">
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p class="text-center">Nenhum livro encontrado.</p>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
```

### Explicação do Uso do Bootstrap

Neste template, o **Bootstrap** foi utilizado para fornecer uma aparência visual consistente e elegante, além de otimizar a responsividade para diferentes dispositivos. Abaixo estão algumas das principais classes do Bootstrap utilizadas:

1. **Barra de Navegação (Navbar):**
   - A navbar com a classe `navbar navbar-expand-lg bg-body-tertiary` cria uma barra de navegação responsiva.
   - A `navbar-toggler` permite que o menu seja expandido em dispositivos menores, e `navbar-collapse` controla o comportamento expansível.

2. **Tabela (Table):**
   - A tabela principal tem as classes `table` e `table-striped`, que aplicam uma estilização básica e alternam a cor de fundo das linhas.
   - `table-dark` no `<thead>` proporciona um cabeçalho com fundo escuro para melhorar a distinção visual.

3. **Botões (Buttons):**
   - Cada botão de ação (`Excluir`, `Atualizar`, `Vender`) tem uma classe de botão (ex., `btn btn-danger` para excluir, `btn btn-primary` para atualizar) que define cores e tamanhos, enquanto `btn-sm` reduz o tamanho dos botões.

4. **Layout Responsivo e Espaçamento:**
   - A classe `container mt-4` centraliza e adiciona espaçamento superior à tabela.
   - A classe `d-flex` com `gap-2` na célula de ações permite uma disposição em linha com espaçamento entre os botões.

Utilizar o **Bootstrap** facilita a criação de interfaces intuitivas e responsivas, deixando a aplicação mais acessível e profissional sem a necessidade de estilizações manuais complexas.
---
Para importar o Bootstrap, adicione os seguintes códigos no `<head>` e no `<body>` do arquivo HTML:

```html
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>

<body>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
```
---
## Explicação do Código HTML

O link do Bootstrap é adicionado no `<head>` para importar o arquivo CSS, enquanto o script é colocado no final do `<body>` para carregar o arquivo JavaScript. Isso garante que o conteúdo HTML seja renderizado antes de aplicar estilos e funcionalidades do Bootstrap.
---

## Conclusão

Nesta prática, integramos o Flask com a API utilizando `requests` para realizar chamadas de criação, leitura, atualização, exclusão e venda de livros. A renderização de templates no Flask nos permite exibir dados dinâmicos de maneira eficiente, oferecendo uma interface web interativa e funcional. A aplicação está pronta para ser executada em containers com Docker, mantendo todos os componentes distribuídos e organizados para o desenvolvimento de sistemas distribuídos.

## Exercício Proposto
1. Adapte a aplicação de livros para o seu produto ou serviço, modificando os campos do formulário e as informações exibidas nos templates.
2. Execute a aplicação em containers com Docker Compose e teste as funcionalidades de CRUD e vendas.
3. Tire prints das páginas da aplicação e do terminal com os logs da execução e adiciones ao seu repositório no GitHub, na pasta `pratica-6/img`.
### Páginas a serem tiradas prints:
 - Página inicial
 - Página com a confirmação de reset do banco de dados
 - Página de estoque
 - Página do formulário de venda
 - Página do formulário de atualização
 - Página de vendas
 - Página de cadastro
 - Página de estoque após excluir um produto, atualizar um produto, cadastrar um produto e vender um produto.
 - Print do Docker desktop com os containers rodando ou print do terminal com os containers rodando `docker ps`.
---
[Voltar ao início](../../README.md)