USE DB_TESTE
-- Criar tabela de Produtos
CREATE TABLE dbo.Produtos (
    IDProduto INT PRIMARY KEY,
    NomeProduto VARCHAR(255),
    QuantidadeEstoque INT
);

-- Inserir dados de exemplo na tabela de Produtos
INSERT INTO Produtos (IDProduto, NomeProduto, QuantidadeEstoque)
VALUES
    (1, 'Brinquedo', 100),
    (2, 'Fruta', 150),
    (3, 'Celular', 200);

-- Criar tabela de Vendas
CREATE TABLE dbo.Vendas (
    IDVenda INT PRIMARY KEY,
    IDProduto INT,
    QuantidadeVendida INT,
    TimestampVenda DATETIME,
    FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto)
);


/* ################### Select das tabelas  ######################## */ 
SELECT * FROM dbo.Vendas
SELECT * FROM dbo.Produtos

