
[Voltar ao início](../../README.md)
---
# Revisão de Python

Este documento serve como uma revisão geral de conceitos fundamentais de Python que serão necessários para o curso de Sistemas Distribuídos. Python é uma linguagem de programação versátil e amplamente utilizada para desenvolvimento de software, automação, análise de dados e muito mais.

## Índice

1. [Introdução](#introdução)
2. [Variáveis e Tipos de Dados](#variáveis-e-tipos-de-dados)
3. [Estruturas de Controle](#estruturas-de-controle)
4. [Funções](#funções)
5. [Manipulação de Arquivos](#manipulação-de-arquivos)
6. [Módulos e Pacotes](#módulos-e-pacotes)
7. [Trabalhando com Bibliotecas](#trabalhando-com-bibliotecas)
8. [Manipulação de Erros e Exceções](#manipulação-de-erros-e-exceções)
9. [Introdução a Programação Orientada a Objetos](#introdução-a-programação-orientada-a-objetos)
10. [Conclusão](#conclusão)

---

## Introdução

Python é uma linguagem de programação de alto nível, interpretada e de propósito geral, conhecida por sua simplicidade e legibilidade. É uma excelente escolha para desenvolvimento rápido e tem uma ampla gama de bibliotecas e frameworks que facilitam o desenvolvimento de sistemas distribuídos.

## Variáveis e Tipos de Dados

### Variáveis
Em Python, as variáveis são criadas no momento em que você atribui um valor a elas.

```python
x = 5
nome = "Python"
```

### Tipos de Dados
- **Inteiros:** `int` (ex: 10, -5)
- **Flutuantes:** `float` (ex: 3.14, -0.001)
- **Strings:** `str` (ex: "Olá", 'Mundo')
- **Booleanos:** `bool` (ex: True, False)
- **Listas:** `list` (ex: [1, 2, 3], ['a', 'b', 'c'])
- **Tuplas:** `tuple` (ex: (1, 2, 3), ('a', 'b', 'c'))
- **Dicionários:** `dict` (ex: {"chave": "valor", "idade": 25})
- **Conjuntos:** `set` (ex: {1, 2, 3}, {'a', 'b', 'c'})

## Estruturas de Controle

### Condicionais
As estruturas condicionais são usadas para executar código com base em uma condição.

```python
x = 10
if x > 5:
    print("x é maior que 5")
elif x == 5:
    print("x é igual a 5")
else:
    print("x é menor que 5")
```

### Loops
Loops são usados para repetir um bloco de código várias vezes.

- **For Loop:**

```python
for i in range(5):
    print(i)
```

- **While Loop:**

```python
i = 0
while i < 5:
    print(i)
    i += 1
```

## Funções

Funções são blocos de código que executam uma tarefa específica e podem ser reutilizados.

```python
def soma(a, b):
    return a + b

resultado = soma(5, 3)
print(resultado)  # Saída: 8
```

## Manipulação de Arquivos

Python permite a leitura e escrita de arquivos com facilidade.

```python
# Leitura
with open('arquivo.txt', 'r') as file:
    conteudo = file.read()

# Escrita
with open('arquivo.txt', 'w') as file:
    file.write("Novo conteúdo")
```

## Módulos e Pacotes

Módulos são arquivos Python que contêm funções e variáveis. Pacotes são coleções de módulos.

```python
# Importando um módulo
import math
print(math.sqrt(16))  # Saída: 4.0

# Importando uma função específica
from math import sqrt
print(sqrt(25))  # Saída: 5.0
```

## Trabalhando com Bibliotecas

Python possui uma rica variedade de bibliotecas. Algumas bibliotecas populares incluem:

- **NumPy:** Manipulação de arrays e cálculos matemáticos.
- **Pandas:** Manipulação e análise de dados.
- **Requests:** Realização de requisições HTTP.

```python
import requests

response = requests.get('https://api.github.com')
print(response.status_code)  # Saída: 200
```

## Manipulação de Erros e Exceções

Tratar erros e exceções é crucial para criar programas robustos.

```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Erro: divisão por zero!")
finally:
    print("Bloco finally sempre é executado")
```

## Introdução a Programação Orientada a Objetos

Python suporta Programação Orientada a Objetos (POO), que permite a criação de classes e objetos.

```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def cumprimentar(self):
        print(f"Olá, meu nome é {self.nome}.")

pessoa1 = Pessoa("João", 30)
pessoa1.cumprimentar()  # Saída: Olá, meu nome é João.
```

## Conclusão

Esta revisão cobre os fundamentos essenciais de Python que serão usados ao longo do curso de Sistemas Distribuídos. Aprofunde-se nesses conceitos, pois eles servirão como base para os tópicos mais avançados que exploraremos nas aulas futuras.

---
[Exercício proposto](./aulas/pratica-1/exercicio_pratica-1.md)
[Voltar ao início](../../README.md)