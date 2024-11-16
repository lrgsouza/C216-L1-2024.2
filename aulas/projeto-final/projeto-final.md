[Voltar ao início](../../README.md)
### Proposta de Projeto Final

Como avaliação final da disciplina, o projeto a ser desenvolvido deve englobar todos os conceitos trabalhados durante o curso, integrando **backend com FastAPI**, **banco de dados PostgreSQL**, **frontend com Flask** e **containers Docker**. O projeto deve ser desenvolvido em **dupla** e terá como objetivo avaliar a capacidade dos alunos de integrar os sistemas distribuídos com containers, realizar chamadas da API, manipular o banco de dados e renderizar dados no frontend de forma eficiente.

### Requisitos

O projeto final deverá atender aos seguintes requisitos, garantindo que todos os conceitos aprendidos na disciplina sejam aplicados de forma integrada:

#### **Backend:**
1. **CRUD Completo:** O backend deverá ser capaz de realizar as operações CRUD (Create, Read, Update, Delete) completas para pelo menos uma entidade do sistema.
   - **Create:** Permitir a inserção de novos registros.
   - **Read:** Permitir a leitura de registros existentes, com opções de filtro e listagem.
   - **Update:** Permitir a atualização de registros existentes.
   - **Delete:** Permitir a exclusão de registros existentes.
   
2. **Testes de API com Postman:** 
   - O backend deverá ter testes automatizados utilizando o Postman, que validem todas as operações CRUD.
   - Os testes devem cobrir todos os cenários possíveis, como inserção, atualização, leitura e exclusão de dados, com validação de respostas corretas, erros e status HTTP adequados.

3. **Endpoint de Reset do Banco de Dados:** 
   - O backend deverá ter um endpoint que permita reiniciar o banco de dados, apagando todos os dados de forma segura. Este endpoint será útil para resetar o sistema durante o desenvolvimento e testes.
   - O script de inicialização do banco de dados (para criar tabelas e relacionamentos) deverá ser fornecido junto com o código.

#### **Banco de Dados:**
1. **Script de Inicialização:** 
   - O banco de dados deverá ser inicializado com um script SQL que crie todas as tabelas necessárias e insira dados de exemplo, caso necessário.
   
2. **Persistência de Dados:** 
   - O banco de dados deverá ser configurado para armazenar dados de forma adequada, com relações entre as tabelas (se necessário).
   
#### **Frontend:**
1. **CRUD no Frontend:** 
   - O frontend, desenvolvido com Flask, deverá apresentar todas as telas necessárias para realizar o CRUD completo com a API.
   - Deve ser possível visualizar, adicionar, editar e excluir registros através do frontend.
   
2. **Estilo do Frontend:**
   - As telas devem ser estilizadas utilizando o **Bootstrap**, facilitando a criação de uma interface visual agradável e responsiva.
   - As telas devem ser claras, com botões de interação para o usuário e exibição de mensagens de sucesso ou erro.

#### **Docker:**
1. **Containers Docker:** 
   - O projeto deve ser orquestrado utilizando o **Docker Compose**, com pelo menos dois containers:
     - Um container para o **backend** (FastAPI).
     - Um container para o **banco de dados** (PostgreSQL).
     - Um container para o **frontend** (Flask).
   
2. **Arquivo `docker-compose.yml`:** 
   - O arquivo Docker Compose deve estar configurado corretamente para rodar todos os containers juntos, permitindo a execução do sistema como um todo em um único comando.

#### **Repositório e Documentação:**
1. **Repositório GitHub:**
   - O projeto deverá ser hospedado em um **Novo** repositório no GitHub, com a dupla sendo adicionada como colaboradores.
   - O repositório deverá conter commits frequentes e bem descritos, demonstrando o progresso do projeto.
   - O nome do repositório é de livre escolha da dupla.
   
2. **README.md:**
   - O repositório deverá conter um arquivo **README.md** na raiz com a explicação do projeto, objetivos, como rodar o projeto (comandos Docker), e informações dos integrantes:
     - Nomes completos
     - Matrículas
     - E-mails dos participantes
     
3. **Documentação de Testes:**
   - Incluir a documentação dos testes realizados, com as etapas para rodar os testes de API utilizando o Postman. (collections e export dos resultados)

#### **Avaliação:**
- **Apresentação:** A dupla deverá apresentar o projeto em um vídeo de no máximo **15 minutos**, mostrando o funcionamento do sistema, destacando o backend, frontend, containers e como os dados estão sendo persistidos e manipulados.
- **Commits e Código:** A dupla será avaliada também pela qualidade e organização do código e pelos commits realizados ao longo do desenvolvimento.

### Sugestões de Projeto

Aqui estão algumas ideias de sistemas simples que podem ajudar na inspiração. Lembre-se de que os projetos não precisam ser complexos, mas devem envolver a integração das tecnologias que foram trabalhadas ao longo da disciplina.

1. **Sistema de reserva de hotel:** Um sistema para gerenciar a reserva de quartos, com cadastro de clientes e opções de busca por data e disponibilidade.
  
2. **Sistema de agendamento de consultas:** Permite que os usuários agendem consultas médicas, com a possibilidade de escolher um profissional, data e hora disponíveis.

3. **Sistema de controle de tarefas (To-Do List):** Um sistema simples para gerenciar tarefas, com funcionalidades de adicionar, editar, excluir e marcar como concluídas.

4. **Sistema de cadastro de clientes e pedidos:** Para uma loja online, onde os clientes podem fazer pedidos e acompanhar o status do seu pedido.

5. **Sistema de gerenciamento de bibliotecas:** Permite que os usuários cadastrem livros, pesquisem por título e autor, e realizem empréstimos e devoluções.

6. **Sistema de gerenciamento de eventos:** Permite que os usuários criem, visualizem e se inscrevam em eventos, como palestras ou cursos.

7. **Sistema de controle de despesas:** Ajuda os usuários a registrar e categorizar suas despesas mensais, visualizando gráficos e relatórios.

8. **Sistema de vendas de ingressos para cinema:** Permite a compra de ingressos para filmes, com funcionalidades de exibição de horários e salas disponíveis.

9. **Sistema de controle de ponto de funcionários:** Registra entradas e saídas dos funcionários, calculando a carga horária de trabalho semanal.

10. **Sistema de controle de pedidos de comida:** Um sistema para restaurantes gerenciarem pedidos online, com integração de cardápio e formas de pagamento.

Essas ideias são apenas sugestões para ajudar a dar início ao projeto. O importante é que o sistema escolhido envolva a integração de todas as partes do curso: backend com FastAPI, frontend com Flask, banco de dados PostgreSQL e orquestração com Docker.

## Entrega

### DATA LIMITE: 07/12/2024

Entregar o link do repositório do projeto final e o link do video da apresentação.

Boa sorte a todos!
---
[Voltar ao início](../../README.md)