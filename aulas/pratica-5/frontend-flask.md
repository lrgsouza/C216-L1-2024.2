
[Voltar ao início](../../README.md)
---
### Prática 5 - Frontend com Flask

Esta prática tem o objetivo de introduzir o **Flask** e demonstrar como utilizá-lo para criar um frontend simples para uma aplicação web. O foco desta prática é ajudar a entender os conceitos básicos do Flask e como servir templates HTML usando a funcionalidade `render_template`. Por enquanto, não faremos a integração com o backend. 

---

## O que é o Flask?

**Flask** é um framework web leve e flexível desenvolvido em Python. Ele é categorizado como um **micro-framework**, pois fornece as funcionalidades essenciais para desenvolvimento web, sem impor uma estrutura rígida ou exigir componentes específicos, como camadas de banco de dados. Flask é construído sobre o padrão WSGI (Web Server Gateway Interface), que facilita a comunicação entre os servidores web e as aplicações Python.

### Características principais do Flask:
- **Leve e Simples**: O Flask fornece apenas o necessário para construir uma aplicação web, mantendo a simplicidade.
- **Flexível**: Permite adicionar componentes conforme a necessidade do projeto (como integração com banco de dados).
- **Modularidade**: Utiliza extensões para adicionar funcionalidades extras (como autenticação, gestão de sessões, etc.).
- **Renderização de Templates**: Facilita o envio de páginas HTML para o usuário através da função `render_template`.

### Como funciona o Flask?

O Flask segue o padrão de desenvolvimento baseado em **rotas**. Cada rota (ou endpoint) responde a uma URL específica e é associada a uma função Python que processa a requisição e retorna uma resposta (geralmente em HTML).

---

## Passo a Passo: Construindo um Frontend Simples com Flask

### Estrutura do Projeto

O projeto terá a seguinte estrutura de diretórios:

```
frontend/
│
├── app.py                # Arquivo principal da aplicação Flask
├── templates/             # Diretório para arquivos HTML
│   ├── index.html         # Página principal
│   ├── about.html         # Página "Sobre"
│
└── static/                # Arquivos estáticos (CSS, JS, imagens)
    └── styles.css         # Estilos CSS para a aplicação
```

### 1. Configurando o Flask

No arquivo `app.py`, configuraremos a aplicação Flask com rotas simples para renderizar templates HTML.

```python
from flask import Flask, render_template

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para a página "Sobre"
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
```

### 2. Criando os Templates HTML

Dentro do diretório `templates/`, crie os arquivos HTML que serão servidos pelas rotas definidas no Flask.

#### `index.html` (Página Principal)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Inicial</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <h1>Bem-vindo ao Frontend com Flask</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/about">Sobre</a>
        </nav>
    </header>
    <section>
        <h2>Introdução ao Flask</h2>
        <p>Este é um exemplo básico de como utilizar o Flask para renderizar templates HTML.</p>
        <p>Esta página foi criada por Lucas Garcia - GES134</p>
    </section>
</body>
</html>
```

#### `about.html` (Página Sobre)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sobre</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <h1>Sobre o Projeto</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/about">Sobre</a>
        </nav>
    </header>
    <section>
        <h2>Sobre esta Aplicação</h2>
        <p>Este projeto utiliza o Flask para criar uma interface web simples.</p>
        <p>Esta página foi criada por Lucas Garcia - GES134</p>
    </section>
</body>
</html>
```

### 3. Estilizando com CSS

Agora, dentro do diretório `static/`, crie um arquivo CSS chamado `styles.css` para estilizar as páginas.

#### `styles.css`

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
    margin: 0;
    padding: 0;
}

header {
    background-color: #333;
    color: white;
    padding: 1em 0;
    text-align: center;
}

nav a {
    margin: 0 15px;
    color: white;
    text-decoration: none;
}

section {
    margin: 20px;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
}

h1, h2 {
    margin-bottom: 10px;
}
```

### 4. Executando a Aplicação

Para rodar o projeto:

1. Certifique-se de que o arquivo Dockerfile esteja correto, ele deve estar dentro do diretório `frontend/`.

   ```bash
    # Using a lightweight Python runtime as a parent image
    FROM python:3.10-slim

    # Install any dependencies needed to run your Python code
    RUN pip install flask

    # Set the working directory to /app
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Make port 3000 available to the world outside this container
    EXPOSE 3000

    # Run app.py when the container launches
    CMD ["python", "app.py"]
   ```

2. Atualize o docker-compose.yml para incluir o novo arquivo.

   ```yaml
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

    frontend:
        build: ./frontend
        restart: always
        ports:
        - "3000:3000"
        depends_on:
        - backend
   ```

3. Execute o comando abaixo para iniciar os containers.

   ```bash
   docker-compose up --build
   ```

4. Acesse a aplicação no navegador, digitando o endereço:
   ```
   http://127.0.0.1:3000/
   ```

---

## Exercício Proposto

1. Personalize seus templates HTML Contendo seu nome e matricula.
2. Adicione uma nova pagina "contact" contendo inforações de contato ficticias.
2. Execute utilizando o docker compose.
3. Tire print dos logs do container frontend.
4. Tire print das `três` paginas HTML.
5. Suba os prints solicitados na `pratica-5/img`.

---
[Voltar ao início](../../README.md)