[Voltar ao início](../../README.md)
---

# Exercício Prática 1 - Introdução ao Python

## Objetivo

O objetivo deste exercício é aplicar os conceitos básicos de Python abordados na revisão, incluindo variáveis, tipos de dados, estruturas de controle e funções. Ao final, você deverá enviar um script Python que resolva o problema descrito abaixo.

## Descrição do Problema

Você foi contratado por uma pequena loja para criar um sistema básico de gerenciamento de estoque. Este sistema deve ser capaz de:

1. **Cadastrar Itens.**
   
2. **Listar Itens.**
   
3. **Consultar Itens.**
   
4. **Vender Itens.**

## Requisitos

1. **Funções:** 
   - O programa deve ser modularizado, com cada funcionalidade implementada em uma função separada.
   
2. **Estrutura de Dados:**
   - O programa deve usar uma lista ou um dicionário para armazenar as informações sobre os itens.

3. **Interação com o Usuário:**
   - O programa deve interagir com o usuário através de um menu no terminal, permitindo que ele escolha entre as opções disponíveis.

## Exemplo de Solução usando Livros

### OBS: Este é apenas um exemplo e você não poderá usa-lo na sua entrega:

```python
def cadastrar_livro(estoque):
    nome = input("Digite o nome do livro: ")
    autor = input("Digite o autor do livro: ")
    quantidade = int(input("Digite a quantidade em estoque: "))
    estoque.append({"nome": nome, "autor": autor, "quantidade": quantidade})
    print(f"Livro '{nome}' cadastrado com sucesso!")

def listar_livros(estoque):
    if len(estoque) == 0:
        print("Nenhum livro cadastrado.")
    else:
        for livro in estoque:
            print(f"Nome: {livro['nome']}, Autor: {livro['autor']}, Quantidade: {livro['quantidade']}")

def consultar_livro(estoque):
    nome = input("Digite o nome do livro a consultar: ")
    for livro in estoque:
        if livro["nome"] == nome:
            print(f"Nome: {livro['nome']}, Autor: {livro['autor']}, Quantidade: {livro['quantidade']}")
            return
    print("Livro não encontrado no estoque.")

def vender_livro(estoque):
    nome = input("Digite o nome do livro a vender: ")
    for livro in estoque:
        if livro["nome"] == nome:
            quantidade = int(input("Digite a quantidade a vender: "))
            if quantidade <= livro["quantidade"]:
                livro["quantidade"] -= quantidade
                print(f"Venda registrada! Quantidade restante de '{nome}': {livro['quantidade']}")
            else:
                print("Erro: Quantidade em estoque insuficiente.")
            return
    print("Livro não encontrado no estoque.")

def main():
    estoque = []
    while True:
        print("\nMenu de Opções:")
        print("1. Cadastrar Livro")
        print("2. Listar Livros")
        print("3. Consultar Livro")
        print("4. Vender Livro")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_livro(estoque)
        elif opcao == '2':
            listar_livros(estoque)
        elif opcao == '3':
            consultar_livro(estoque)
        elif opcao == '4':
            vender_livro(estoque)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
```

## Entrega

- **Execução:** Rode o arquivo `sistema_estoque.py` no terminal e execute as seguintes instruções:
    - Cadastrar pelo menos 3 itens.
    - Listar os itens cadastrados.
    - Consultar um item cadastrado.
    - Vender um item cadastrado.
    - Listar os itens novamente para verificar se a quantidade foi atualizada.

- **Formato:** Envie o link para o seu repositório no GitHub contendo o arquivo `sistema_estoque.py`e um arquivo `logs.txt` com a saída do programa.
- **Critérios de Avaliação:**
  - Corretude do código.
  - Uso adequado das estruturas de controle e funções.
  - Implementação da lógica de gerenciamento de estoque utilizando listas ou dicionários.
  - Clareza e organização do código.

Boa sorte e mãos à obra!

---
[Voltar ao início](../../README.md)