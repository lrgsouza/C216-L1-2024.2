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
