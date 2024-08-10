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
