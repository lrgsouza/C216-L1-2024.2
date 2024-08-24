[Voltar ao início](../../README.md)
---

# Introdução ao Docker e Build de Aplicações Python

## O que é Docker?

Docker é uma plataforma que permite a criação, implantação e execução de aplicações em containers. Containers são ambientes isolados que incluem tudo o que uma aplicação precisa para ser executada: código, bibliotecas, dependências, etc. Isso garante que a aplicação funcione de maneira consistente em qualquer ambiente.

- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Benefícios do Docker
- **Portabilidade:** Docker containers podem ser executados em qualquer ambiente que suporte Docker.
- **Consistência:** Garantia de que a aplicação funciona da mesma forma em diferentes ambientes.
- **Eficiência:** Uso eficiente de recursos, já que vários containers podem compartilhar o mesmo sistema operacional.
- **Facilidade de Gerenciamento:** Ferramentas integradas para gerenciamento e orquestração de containers.

## Conceitos Básicos

- **Imagem:** Um blueprint imutável que contém tudo o que o aplicativo precisa para rodar.
- **Container:** Uma instância de uma imagem em execução.
- **Dockerfile:** Um arquivo de script que contém instruções para construir uma imagem Docker.
- **Docker Hub:** Um repositório público para armazenar e compartilhar imagens Docker.

## Criando um Dockerfile para a Aplicação Python

Vamos construir uma imagem Docker para o sistema de gerenciamento de estoque que desenvolvemos anteriormente. A seguir, um exemplo de `Dockerfile`:

### Dockerfile

```Dockerfile
# Usando uma imagem base do Python
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo Python para o diretório de trabalho no container
COPY sistema_estoque.py .

# Comando para executar o script Python
CMD ["python", "sistema_estoque.py"]
```

### Explicação do Dockerfile

- **FROM:** Especifica a imagem base. Neste caso, usamos `python:3.10-slim`, que é uma imagem leve do Python.
- **WORKDIR:** Define o diretório de trabalho dentro do container. Todos os comandos seguintes serão executados nesse diretório.
- **COPY:** Copia o arquivo `sistema_estoque.py` do diretório local para o diretório de trabalho no container.
- **CMD:** Especifica o comando que será executado quando o container for iniciado. Aqui, estamos executando o script Python.

## Build da Imagem Docker

Para construir a imagem Docker a partir do `Dockerfile`, use o seguinte comando no terminal:

```bash
docker build -t sistema_estoque .
```

- **docker build:** Comando para construir uma imagem Docker.
- **-t sistema_estoque:** Define a tag (nome) da imagem como `sistema_estoque`.
- **.** : Indica que o Dockerfile está no diretório atual.

## Rodando a Imagem Docker

Depois de construir a imagem, você pode rodá-la usando o comando:

```bash
docker run -it sistema_estoque
```

- **docker run:** Comando para rodar um container a partir de uma imagem.
- **-it:** Flags que permitem interação com o terminal dentro do container (`-i` para interação e `-t` para alocar um pseudo-terminal).
- **sistema_estoque:** Nome da imagem que criamos anteriormente.

Ao rodar este comando, o sistema de gerenciamento de estoque será executado dentro do container, e você poderá interagir com ele via terminal, assim como faria ao rodar o script Python diretamente no seu sistema.

## Interagindo com o Terminal

Dentro do container, você verá o menu de opções do sistema de gerenciamento de estoque, onde poderá cadastrar, listar, consultar e vender livros, conforme implementado no exercício.

Para parar a execução do container, você pode usar `CTRL + C`. Se você precisar sair do container sem parar o script, pode usar o comando `exit` no terminal.

## Resumo

- **Construímos uma imagem Docker** para a aplicação Python usando um Dockerfile.
- **Rodamos a aplicação dentro de um container** e interagimos com ela via terminal.
- **Docker** proporciona um ambiente consistente e isolado para a execução de aplicações, facilitando o desenvolvimento e a implantação.

---
[Voltar ao início](../../README.md)
