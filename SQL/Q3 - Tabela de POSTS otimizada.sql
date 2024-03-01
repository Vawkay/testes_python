-- Criar tabela de Posts
CREATE TABLE PostsOtimizada (
    IDPost INT PRIMARY KEY,
    TextoPost NVARCHAR(MAX),
    DataHoraPost DATETIME,
    Sentimento NVARCHAR(50),
    IDProduto INT
);

-- Criar �ndice n�o agrupado na coluna DataHoraPost
CREATE NONCLUSTERED INDEX IX_DataHoraPost
ON PostsOtimizada (DataHoraPost);

-- Criar �ndice n�o agrupado na coluna Sentimento
CREATE NONCLUSTERED INDEX IX_Sentimento
ON PostsOtimizada (Sentimento);

-- Adicionar coluna de Parti��o para DataHoraPost
ALTER TABLE PostsOtimizada
ADD DataParticao AS CONVERT(DATE, DataHoraPost) PERSISTED;

-- Criar esquema de parti��o de 6m em 6m
CREATE PARTITION FUNCTION ParticaoMensal(DATE) AS RANGE RIGHT FOR VALUES ('2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01', '2024-01-01', '2024-07-01');

-- Criar esquema de esquema de parti��o
CREATE PARTITION SCHEME ParticaoMensal
AS PARTITION ParticaoMensal
ALL TO ([PRIMARY]);