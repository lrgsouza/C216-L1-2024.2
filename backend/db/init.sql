DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "livros";

CREATE TABLE "livros" (
    "id" SERIAL PRIMARY KEY,
    "titulo" VARCHAR(255) NOT NULL,
    "autor" VARCHAR(255) NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "preco" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "livro_id" INTEGER REFERENCES livros(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('O Senhor dos Anéis', 'J.R.R. Tolkien', 10, 50.00);
INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('Harry Potter', 'J.K. Rowling', 20, 30.00);
INSERT INTO "livros" ("titulo", "autor", "quantidade", "preco") VALUES ('1984', 'George Orwell', 15, 40.00)