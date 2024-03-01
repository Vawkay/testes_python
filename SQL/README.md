# SP_InserirAtualizarDespesasDetalhadas Procedure

A procedure `SP_InserirAtualizarDespesasDetalhadas` � uma rotina SQL armazenada que foi criada para manipular e atualizar um conjunto de dados relacionados a despesas detalhadas.

## Funcionalidade

A procedure realiza as seguintes opera��es:

1. **Cria��o de Tabelas Tempor�rias**: A procedure cria v�rias tabelas tempor�rias (`#centro_de_custo`, `#contas`, `#despesas`, `#orcamento`, `#despesas_detalhadas` e `#LogErros`) para armazenar dados intermedi�rios e erros de execu��o.

2. **Importa��o de Dados**: A procedure importa dados de v�rios arquivos CSV (`CENTRO_DE_CUSTO.csv`, `CONTAS.csv`, `DESPESAS.csv` e `orcamento.csv`) para as tabelas tempor�rias correspondentes.

3. **Manipula��o de Dados**: A procedure realiza v�rias opera��es de manipula��o de dados, como atualiza��o de valores de despesas e cria��o de uma subquery tempor�ria agrupada.

4. **Atualiza��o da Tabela Principal**: A procedure deleta registros antigos da tabela principal `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` e insere novos registros a partir da tabela tempor�ria `#despesas_detalhadas`.

5. **Tratamento de Erros**: A procedure utiliza blocos `TRY...CATCH` para capturar e registrar erros de execu��o na tabela tempor�ria `#LogErros`.

## Uso

Para executar a procedure, use o seguinte comando:

```sql
EXEC DBO.SP_InserirAtualizarDespesasDetalhadas
```

## Observa��es

A procedure foi projetada para ser usada em um ambiente SQL Server. Ela utiliza v�rias fun��es espec�ficas do SQL Server, como `TRY_CONVERT` e `ERROR_MESSAGE`.

Al�m disso, a procedure assume que os arquivos CSV de entrada est�o dispon�veis em um caminho de rede especificado e que a tabela principal `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` j� existe no banco de dados.

Por fim, a procedure utiliza uma transa��o para garantir que as opera��es de atualiza��o da tabela principal sejam at�micas. Se ocorrer um erro durante a atualiza��o, a transa��o ser� revertida e os detalhes do erro ser�o registrados na tabela `#LogErros`.

A tabela `DB_ALELO.DBO.TB_DESPESAS_DETALHADAS` � criada para armazenar informa��es detalhadas sobre despesas. A tabela possui as seguintes colunas:

- `DTBASE`: Uma coluna de data que armazena a data base da despesa.
- `CODIGOCENTROCUSTO`: Uma coluna VARCHAR que armazena o c�digo do centro de custo.
- `CENTROCUSTOMASTER`: Uma coluna VARCHAR que armazena o nome do centro de custo master.
- `VLDESPESA`: Uma coluna FLOAT que armazena o valor da despesa.
- `CODFILIALPRINCIPAL`: Uma coluna VARCHAR que armazena o c�digo da filial principal.
- `CODCONTA`: Uma coluna BIGINT que armazena o c�digo da conta.
- `MES_A`: Uma coluna VARCHAR que armazena o m�s e o ano da despesa no formato 'YYYY-MM'.
- `DESCRICAO`: Uma coluna VARCHAR que armazena a descri��o da despesa.
- `CENTROCUSTO`: Uma coluna VARCHAR que armazena o nome do centro de custo.
- `CENTROCUSTO_COD`: Uma coluna VARCHAR que armazena o c�digo do centro de custo.
- `CONTA`: Uma coluna VARCHAR que armazena o nome da conta.
- `GRUPO`: Uma coluna VARCHAR que armazena o nome do grupo de despesas.
- `ORCADO`: Uma coluna FLOAT que armazena o valor or�ado para a despesa.
- `PERRATEIO`: Uma coluna INT que armazena o percentual de rateio da despesa.
- `REGISTRO`: Uma coluna DATETIME que armazena a data e hora do registro da despesa.

A tabela � criada com o seguinte comando SQL:

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

Para visualizar todos os registros na tabela, voc� pode usar o seguinte comando SQL:

```sql
SELECT * FROM DB_ALELO.DBO.TB_DESPESAS_DETALHADAS
```
# RealizarVenda Procedure

A procedure `RealizarVenda` � uma rotina SQL armazenada que foi criada para gerenciar vendas de produtos e atualizar o estoque em tempo real, minimizando conflitos de estoque em um sistema de e-commerce.

## Funcionalidade

A procedure realiza as seguintes opera��es:

1. **Verifica��o de Estoque**: A procedure verifica a quantidade atual em estoque do produto que est� sendo vendido.

2. **Valida��o de Venda**: A procedure valida se h� estoque suficiente para a venda. Se a quantidade em estoque for menor que a quantidade vendida, a venda n�o � realizada e uma mensagem de erro � exibida.

3. **Registro de Venda**: Se houver estoque suficiente, a venda � registrada na tabela `Vendas` e a quantidade em estoque do produto � atualizada na tabela `Produtos`.

4. **Tratamento de Erros**: A procedure utiliza blocos `TRY...CATCH` para capturar e registrar erros durante a venda. Se ocorrer um erro, a transa��o � revertida e as mensagens de erro s�o exibidas.

## Uso

Para executar a procedure, use o seguinte comando:

```sql
EXEC RealizarVenda @IDProduto = 2, @QuantidadeVendida = 15;
```

## Observa��es

A procedure foi projetada para ser usada em um ambiente SQL Server. Ela utiliza v�rias fun��es espec�ficas do SQL Server, como `BEGIN TRANSACTION`, `COMMIT` e `ROLLBACK`.

Al�m disso, a procedure assume que as tabelas `Produtos` e `Vendas` j� existem no banco de dados.

A tabela `Produtos` � criada para armazenar informa��es sobre os produtos dispon�veis para venda. A tabela possui as seguintes colunas:

- `IDProduto`: Uma coluna INT que armazena o ID do produto.
- `NomeProduto`: Uma coluna VARCHAR que armazena o nome do produto.
- `QuantidadeEstoque`: Uma coluna INT que armazena a quantidade atual em estoque do produto.

A tabela `Vendas` � criada para registrar cada venda. A tabela possui as seguintes colunas:

- `IDVenda`: Uma coluna INT que armazena o ID da venda.
- `IDProduto`: Uma coluna INT que armazena o ID do produto vendido.
- `QuantidadeVendida`: Uma coluna INT que armazena a quantidade vendida do produto.
- `TimestampVenda`: Uma coluna DATETIME que armazena o timestamp da venda.

As tabelas s�o criadas com os seguintes comandos SQL:

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

Para visualizar todos os registros nas tabelas, voc� pode usar os seguintes comandos SQL:

```sql
SELECT * FROM dbo.Vendas;
SELECT * FROM dbo.Produtos;
```
# PostsOtimizada Table

O script `PostsOtimizada.sql` � um conjunto de instru��es SQL que foi criado para otimizar as consultas usadas para gerar relat�rios de an�lise de sentimento em um sistema de monitoramento de redes sociais.

## Funcionalidade

O script realiza as seguintes opera��es:

1. **Cria��o de Tabela**: O script cria a tabela `PostsOtimizada` com as colunas `IDPost`, `TextoPost`, `DataHoraPost`, `Sentimento` e `IDProduto`.

2. **Cria��o de �ndices**: O script cria �ndices n�o agrupados nas colunas `DataHoraPost` e `Sentimento` da tabela `PostsOtimizada` para acelerar as consultas que filtram por essas colunas.

3. **Cria��o de Parti��o**: O script adiciona uma coluna de parti��o `DataParticao` � tabela `PostsOtimizada` e cria um esquema de parti��o de 6 meses em 6 meses para a coluna `DataHoraPost`. Isso pode melhorar o desempenho das consultas que filtram por data.

## Uso

Para executar o script, voc� pode copiar e colar as instru��es SQL no seu ambiente SQL Server e execut�-las.

## Observa��es

O script foi projetado para ser usado em um ambiente SQL Server. Ele utiliza v�rias fun��es espec�ficas do SQL Server, como `CREATE NONCLUSTERED INDEX` e `CREATE PARTITION SCHEME`.

A tabela `PostsOtimizada` � criada para armazenar informa��es sobre os posts coletados das redes sociais para an�lise de sentimento. A tabela possui as seguintes colunas:

- `IDPost`: Uma coluna INT que armazena o ID do post.
- `TextoPost`: Uma coluna NVARCHAR(MAX) que armazena o texto do post.
- `DataHoraPost`: Uma coluna DATETIME que armazena a data e hora do post.
- `Sentimento`: Uma coluna NVARCHAR(50) que armazena o sentimento do post (positivo, negativo, neutro).
- `IDProduto`: Uma coluna INT que armazena o ID do produto associado ao post.

Para visualizar todos os registros na tabela, voc� pode usar o seguinte comando SQL:

```sql
SELECT * FROM PostsOtimizada;
```