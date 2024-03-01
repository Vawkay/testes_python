# SP_InserirAtualizarDespesasDetalhadas Procedure

A procedure `SP_InserirAtualizarDespesasDetalhadas` é uma rotina SQL armazenada que foi criada para manipular e atualizar um conjunto de dados relacionados a despesas detalhadas.

## Funcionalidade

A procedure realiza as seguintes operações:

1. **Criação de Tabelas Temporárias**: A procedure cria várias tabelas temporárias (`#centro_de_custo`, `#contas`, `#despesas`, `#orcamento`, `#despesas_detalhadas` e `#LogErros`) para armazenar dados intermediários e erros de execução.

2. **Importação de Dados**: A procedure importa dados de vários arquivos CSV (`CENTRO_DE_CUSTO.csv`, `CONTAS.csv`, `DESPESAS.csv` e `orcamento.csv`) para as tabelas temporárias correspondentes.

3. **Manipulação de Dados**: A procedure realiza várias operações de manipulação de dados, como atualização de valores de despesas e criação de uma subquery temporária agrupada.

4. **Atualização da Tabela Principal**: A procedure deleta registros antigos da tabela principal `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` e insere novos registros a partir da tabela temporária `#despesas_detalhadas`.

5. **Tratamento de Erros**: A procedure utiliza blocos `TRY...CATCH` para capturar e registrar erros de execução na tabela temporária `#LogErros`.

## Uso

Para executar a procedure, use o seguinte comando:

```sql
EXEC DBO.SP_InserirAtualizarDespesasDetalhadas
```

## Observações

A procedure foi projetada para ser usada em um ambiente SQL Server. Ela utiliza várias funções específicas do SQL Server, como `TRY_CONVERT` e `ERROR_MESSAGE`.

Além disso, a procedure assume que os arquivos CSV de entrada estão disponíveis em um caminho de rede especificado e que a tabela principal `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` já existe no banco de dados.

Por fim, a procedure utiliza uma transação para garantir que as operações de atualização da tabela principal sejam atômicas. Se ocorrer um erro durante a atualização, a transação será revertida e os detalhes do erro serão registrados na tabela `#LogErros`.

A tabela `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` é criada para armazenar informações detalhadas sobre despesas. A tabela possui as seguintes colunas:

- `DTBASE`: Uma coluna de data que armazena a data base da despesa.
- `CODIGOCENTROCUSTO`: Uma coluna VARCHAR que armazena o código do centro de custo.
- `CENTROCUSTOMASTER`: Uma coluna VARCHAR que armazena o nome do centro de custo master.
- `VLDESPESA`: Uma coluna FLOAT que armazena o valor da despesa.
- `CODFILIALPRINCIPAL`: Uma coluna VARCHAR que armazena o código da filial principal.
- `CODCONTA`: Uma coluna BIGINT que armazena o código da conta.
- `MES_A`: Uma coluna VARCHAR que armazena o mês e o ano da despesa no formato 'YYYY-MM'.
- `DESCRICAO`: Uma coluna VARCHAR que armazena a descrição da despesa.
- `CENTROCUSTO`: Uma coluna VARCHAR que armazena o nome do centro de custo.
- `CENTROCUSTO_COD`: Uma coluna VARCHAR que armazena o código do centro de custo.
- `CONTA`: Uma coluna VARCHAR que armazena o nome da conta.
- `GRUPO`: Uma coluna VARCHAR que armazena o nome do grupo de despesas.
- `ORCADO`: Uma coluna FLOAT que armazena o valor orçado para a despesa.
- `PERRATEIO`: Uma coluna INT que armazena o percentual de rateio da despesa.
- `REGISTRO`: Uma coluna DATETIME que armazena a data e hora do registro da despesa.

A tabela é criada com o seguinte comando SQL:

```sql
CREATE TABLE DB_ALELO.DBO.TB_DESPESAS_DETALHADAS (
    DTBASE DATE,
    CODIGOCENTROCUSTO VARCHAR(10),
    CENTROCUSTOMASTER VARCHAR(100),
    VLDESPESA FLOAT,
    CODFILIALPRINCIPAL VARCHAR(10),
    CODCONTA BIGINT,
    MES_A VARCHAR(7),
    DESCRICAO VARCHAR(100),
    CENTROCUSTO VARCHAR(100),
    CENTROCUSTO_COD VARCHAR(10),
    CONTA VARCHAR(100),
    GRUPO VARCHAR(100),
    ORCADO FLOAT,
    PERRATEIO INT,
    REGISTRO DATETIME 
);
```

Para visualizar todos os registros na tabela, você pode usar o seguinte comando SQL:

```sql
SELECT * FROM DB_ALELO.DBO.TB_DESPESAS_DETALHADAS
```
# RealizarVenda Procedure

A procedure `RealizarVenda` é uma rotina SQL armazenada que foi criada para gerenciar vendas de produtos e atualizar o estoque em tempo real, minimizando conflitos de estoque em um sistema de e-commerce.

## Funcionalidade

A procedure realiza as seguintes operações:

1. **Verificação de Estoque**: A procedure verifica a quantidade atual em estoque do produto que está sendo vendido.

2. **Validação de Venda**: A procedure valida se há estoque suficiente para a venda. Se a quantidade em estoque for menor que a quantidade vendida, a venda não é realizada e uma mensagem de erro é exibida.

3. **Registro de Venda**: Se houver estoque suficiente, a venda é registrada na tabela `Vendas` e a quantidade em estoque do produto é atualizada na tabela `Produtos`.

4. **Tratamento de Erros**: A procedure utiliza blocos `TRY...CATCH` para capturar e registrar erros durante a venda. Se ocorrer um erro, a transação é revertida e as mensagens de erro são exibidas.

## Uso

Para executar a procedure, use o seguinte comando:

```sql
EXEC RealizarVenda @IDProduto = 2, @QuantidadeVendida = 15;
```

## Observações

A procedure foi projetada para ser usada em um ambiente SQL Server. Ela utiliza várias funções específicas do SQL Server, como `BEGIN TRANSACTION`, `COMMIT` e `ROLLBACK`.

Além disso, a procedure assume que as tabelas `Produtos` e `Vendas` já existem no banco de dados.

A tabela `Produtos` é criada para armazenar informações sobre os produtos disponíveis para venda. A tabela possui as seguintes colunas:

- `IDProduto`: Uma coluna INT que armazena o ID do produto.
- `NomeProduto`: Uma coluna VARCHAR que armazena o nome do produto.
- `QuantidadeEstoque`: Uma coluna INT que armazena a quantidade atual em estoque do produto.

A tabela `Vendas` é criada para registrar cada venda. A tabela possui as seguintes colunas:

- `IDVenda`: Uma coluna INT que armazena o ID da venda.
- `IDProduto`: Uma coluna INT que armazena o ID do produto vendido.
- `QuantidadeVendida`: Uma coluna INT que armazena a quantidade vendida do produto.
- `TimestampVenda`: Uma coluna DATETIME que armazena o timestamp da venda.

As tabelas são criadas com os seguintes comandos SQL:

```sql
CREATE TABLE dbo.Produtos (
    IDProduto INT PRIMARY KEY,
    NomeProduto VARCHAR(255),
    QuantidadeEstoque INT
);

CREATE TABLE dbo.Vendas (
    IDVenda INT PRIMARY KEY,
    IDProduto INT,
    QuantidadeVendida INT,
    TimestampVenda DATETIME,
    FOREIGN KEY (IDProduto) REFERENCES Produtos(IDProduto)
);
```

Para visualizar todos os registros nas tabelas, você pode usar os seguintes comandos SQL:

```sql
SELECT * FROM dbo.Vendas;
SELECT * FROM dbo.Produtos;
```
# PostsOtimizada Table

O script `PostsOtimizada.sql` é um conjunto de instruções SQL que foi criado para otimizar as consultas usadas para gerar relatórios de análise de sentimento em um sistema de monitoramento de redes sociais.

## Funcionalidade

O script realiza as seguintes operações:

1. **Criação de Tabela**: O script cria a tabela `PostsOtimizada` com as colunas `IDPost`, `TextoPost`, `DataHoraPost`, `Sentimento` e `IDProduto`.

2. **Criação de Índices**: O script cria índices não agrupados nas colunas `DataHoraPost` e `Sentimento` da tabela `PostsOtimizada` para acelerar as consultas que filtram por essas colunas.

3. **Criação de Partição**: O script adiciona uma coluna de partição `DataParticao` à tabela `PostsOtimizada` e cria um esquema de partição de 6 meses em 6 meses para a coluna `DataHoraPost`. Isso pode melhorar o desempenho das consultas que filtram por data.

## Uso

Para executar o script, você pode copiar e colar as instruções SQL no seu ambiente SQL Server e executá-las.

## Observações

O script foi projetado para ser usado em um ambiente SQL Server. Ele utiliza várias funções específicas do SQL Server, como `CREATE NONCLUSTERED INDEX` e `CREATE PARTITION SCHEME`.

A tabela `PostsOtimizada` é criada para armazenar informações sobre os posts coletados das redes sociais para análise de sentimento. A tabela possui as seguintes colunas:

- `IDPost`: Uma coluna INT que armazena o ID do post.
- `TextoPost`: Uma coluna NVARCHAR(MAX) que armazena o texto do post.
- `DataHoraPost`: Uma coluna DATETIME que armazena a data e hora do post.
- `Sentimento`: Uma coluna NVARCHAR(50) que armazena o sentimento do post (positivo, negativo, neutro).
- `IDProduto`: Uma coluna INT que armazena o ID do produto associado ao post.

Para visualizar todos os registros na tabela, você pode usar o seguinte comando SQL:

```sql
SELECT * FROM PostsOtimizada;
```