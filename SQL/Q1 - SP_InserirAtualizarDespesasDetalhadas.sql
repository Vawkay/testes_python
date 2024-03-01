CREATE PROCEDURE DBO.SP_InserirAtualizarDespesasDetalhadas AS 

DECLARE
    @CaminhoAbsoluto VARCHAR(8000),
	@CaminhoRede     VARCHAR(8000),
    @NomeArquivo     VARCHAR(500),
    @SQLCOMMAND      VARCHAR(8000),
	-- Dados de Log
	@DataHoraErro DATETIME,
    @NomeErro NVARCHAR(MAX),
    @NomeEtapa NVARCHAR(MAX),
    @LinhaErro INT
 
    SET @CaminhoRede = '\\repositorio.tivit.bpo\mis\OPERACIONAL\CONTROLES MIS\ANALISTAS\FELIPE_ROCHA\SQL\'

-- Criação da tabela temporária para armazenar erros
IF OBJECT_ID('tempdb..#LogErros') IS NOT NULL DROP TABLE #LogErros;

CREATE TABLE #LogErros (
    DataHoraErro DATETIME,
    NomeErro NVARCHAR(MAX),
    NomeEtapa NVARCHAR(MAX),
    LinhaErro INT
);
 
BEGIN TRY
	-- Criação da tabela temporária centro de custo (Deleta se já existir)
	IF OBJECT_ID('tempdb..#centro_de_custo') IS NOT NULL DROP TABLE #centro_de_custo;
	CREATE TABLE
		#centro_de_custo (
			CODIGOCENTROCUSTO VARCHAR(10),
			DESCRICAO VARCHAR(100),
			CENTROCUSTO VARCHAR(100),
			CENTROCUSTO_COD VARCHAR(10),
	);

	-- Caminho do arquivo de centro de custo
	SET @NomeArquivo = 'CENTRO_DE_CUSTO.csv'
	EXEC master.dbo.PR_CopiaArquivoRede @CaminhoRede,@NomeArquivo, @CaminhoAbsoluto output, 1
	-- Bulk Insert do arquivo de centro de custo
	SET @SQLCOMMAND = 'bulk insert #centro_de_custo ' +
						'FROM ''' + @CaminhoAbsoluto + '''
						WITH (FIRSTROW = 2, CODEPAGE = ''UTF-8'' , FIELDTERMINATOR = '';'', ROWTERMINATOR = ''\n'')'
	EXEC (@SQLCOMMAND);
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Criação da tabela temporaria #centro_de_custo'
	SET @LinhaErro = ERROR_LINE()

	-- Inserir detalhes do erro na tabela de log
    INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
    VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
END CATCH;

--------------------------------------------------------------------------
BEGIN TRY
	-- Criação da tabela temporária contas (Deleta se já existir)
	IF OBJECT_ID('tempdb..#contas') IS NOT NULL DROP TABLE #contas;
	CREATE TABLE
		#contas (
			CODCONTA BIGINT,
			CONTA VARCHAR(100),
			GRUPO VARCHAR(100),
	);

	-- Caminho do arquivo de contas
	SET @NomeArquivo = 'CONTAS.csv'
	EXEC master.dbo.PR_CopiaArquivoRede @CaminhoRede,@NomeArquivo, @CaminhoAbsoluto output, 1
	-- Bulk Insert do arquivo de contas
	SET @SQLCOMMAND = 'bulk insert #contas ' +
					   'FROM ''' + @CaminhoAbsoluto + '''
						WITH (FIRSTROW = 2, CODEPAGE = ''UTF-8'' , FIELDTERMINATOR = '';'', ROWTERMINATOR = ''\n'')'
	EXEC (@SQLCOMMAND)
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Criação da tabela temporaria ..#contas'
	SET @LinhaErro = ERROR_LINE()
	-- Inserir detalhes do erro na tabela de log
    INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
    VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
END CATCH;

--------------------------------------------------------------------------
-- Criação da tabela temporária despesas (Deleta se já existir)
BEGIN TRY
	IF OBJECT_ID('tempdb..#despesas') IS NOT NULL DROP TABLE #despesas;
	CREATE TABLE
		#despesas (
			DTBASE VARCHAR(10),
			CODIGOCENTROCUSTO VARCHAR(10),
			CENTROCUSTOMASTER VARCHAR(100),
			VLDESPESA VARCHAR(10),
			CODFILIALPRINCIPAL VARCHAR(10),
			CODCONTA  BIGINT,
			MES_A VARCHAR(10),
	);

	-- Caminho do arquivo de despesas
	SET @NomeArquivo = 'DESPESAS.csv'
	EXEC master.dbo.PR_CopiaArquivoRede @CaminhoRede,@NomeArquivo, @CaminhoAbsoluto output, 1

	-- Bulk Insert do arquivo de contas
	SET @SQLCOMMAND = 'bulk insert #despesas ' +
					   'FROM ''' + @CaminhoAbsoluto + '''
						WITH (FIRSTROW = 2, CODEPAGE = ''UTF-8'' , FIELDTERMINATOR = '';'', ROWTERMINATOR = ''\n'')'
	EXEC (@SQLCOMMAND)
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Criação da tabela temporaria ..#despesas'
	SET @LinhaErro = ERROR_LINE()
	-- Inserir detalhes do erro na tabela de log
    INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
    VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
END CATCH;
--------------------------------------------------------------------------
-- Criação da tabela temporária orçamento (Deleta se já existir)
BEGIN TRY
IF OBJECT_ID('tempdb..#orcamento') IS NOT NULL DROP TABLE #orcamento;
CREATE TABLE
    #orcamento (
        ULTDATA DATE,
        FILIALCOD INT,
        CONTACOD BIGINT,
		CENTROCUSTOCOD VARCHAR(10),
		ORCADO FLOAT,
		PERRATEIO INT,
);

-- Caminho do arquivo de orcamento
SET @NomeArquivo = 'orcamento.csv'
EXEC master.dbo.PR_CopiaArquivoRede @CaminhoRede,@NomeArquivo, @CaminhoAbsoluto output, 1

-- Bulk Insert do arquivo de contas
SET @SQLCOMMAND = 'bulk insert #orcamento ' +
                   'FROM ''' + @CaminhoAbsoluto + '''
                    WITH (FIRSTROW = 2, CODEPAGE = ''UTF-8'' , FIELDTERMINATOR = '';'', ROWTERMINATOR = ''\n'')'
EXEC (@SQLCOMMAND)
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Criação da tabela temporaria ..#orcamento'
	SET @LinhaErro = ERROR_LINE()
	-- Inserir detalhes do erro na tabela de log
    INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
    VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
END CATCH;
--------------------------------------------------------------------------
BEGIN TRY
	-- Substitui ponto por virgulas
	UPDATE #despesas
	SET VLDESPESA = REPLACE(VLDESPESA, ',', '.')
	WHERE VLDESPESA LIKE '%,%';
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Update da tabela de despesas'
	SET @LinhaErro = ERROR_LINE()
	-- Inserir detalhes do erro na tabela de log
    INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
    VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
END CATCH;

-- Deleta a tabela que vai ser criada no INTO
IF OBJECT_ID('tempdb..#despesas_detalhadas') IS NOT NULL DROP TABLE #despesas_detalhadas;

BEGIN TRY
	BEGIN TRANSACTION;
		-- Cria uma subquery temporaria agrupada
		WITH SBQ_DESPESAS AS (
			SELECT
			TRY_CONVERT(DATE, A.DTBASE, 103) AS DTBASE
			,A.CODIGOCENTROCUSTO
			,A.CENTROCUSTOMASTER
			,SUM(TRY_CONVERT(FLOAT, A.VLDESPESA)) AS VLDESPESA
			,A.CODFILIALPRINCIPAL
			,A.CODCONTA
			,A.MES_A
			FROM #despesas AS A
			GROUP BY 
				TRY_CONVERT(DATE, A.DTBASE, 103)
				,A.CODIGOCENTROCUSTO
				,A.CENTROCUSTOMASTER
				,A.CODFILIALPRINCIPAL
				,A.CODCONTA
				,A.MES_A
		)
		SELECT
			TRY_CONVERT(DATE, A.DTBASE, 103)	AS DTBASE
			,A.CODIGOCENTROCUSTO
			,A.CENTROCUSTOMASTER
			,A.VLDESPESA
			,A.CODFILIALPRINCIPAL
			,A.CODCONTA
			,A.MES_A
			,UPPER(B.DESCRICAO)					AS DESCRICAO
			,B.CENTROCUSTO
			,B.CENTROCUSTO_COD
			,UPPER(C.CONTA)						AS CONTA
			,UPPER(C.GRUPO)						AS GRUPO
			,D.ORCADO
			,D.PERRATEIO
			INTO #despesas_detalhadas
		FROM SBQ_DESPESAS AS A 
		LEFT JOIN #centro_de_custo AS B ON A.CODIGOCENTROCUSTO = B.CODIGOCENTROCUSTO
		LEFT JOIN #contas AS C ON A.CODCONTA = C.CODCONTA
		LEFT JOIN #orcamento AS D ON TRY_CONVERT(DATE, A.DTBASE, 103) = ULTDATA
										AND A.CODCONTA = D.CONTACOD
										AND TRY_CONVERT(VARCHAR, A.CODIGOCENTROCUSTO) = TRY_CONVERT(VARCHAR, D.CENTROCUSTOCOD)
										AND TRY_CONVERT(VARCHAR, A.CODFILIALPRINCIPAL) =  TRY_CONVERT(VARCHAR, D.FILIALCOD)

		-- Deleta os registros antigos para substituir por novos
		DELETE DB_ALELO.DBO.TB_DESPESAS_DETALHADAS WHERE CONCAT(DTBASE, CODFILIALPRINCIPAL) IN (SELECT DISTINCT CONCAT(DTBASE, CODFILIALPRINCIPAL) FROM #despesas_detalhadas)

		-- Insere novos registros na tabela junto com a marca de data e hora
		INSERT INTO DB_ALELO.DBO.TB_DESPESAS_DETALHADAS SELECT *, GETDATE() AS REGISTRO FROM #despesas_detalhadas
	 
	 -- Se ocorreu tudo certo confirma a transação
	 COMMIT TRANSACTION;
END TRY
BEGIN CATCH
	SET @DataHoraErro = GETDATE()
	SET @NomeErro = ERROR_MESSAGE()
	SET @NomeEtapa = 'Deletando e atualizando a tabela principal'
	SET @LinhaErro = ERROR_LINE()
	-- Inserir detalhes do erro na tabela de log
	INSERT INTO #LogErros (DataHoraErro, NomeErro, NomeEtapa, LinhaErro)
	VALUES (@DataHoraErro, @NomeErro, @NomeEtapa, @LinhaErro);
	ROLLBACK
END CATCH;

/*
SELECT * FROM #despesas_detalhadas
SELECT * FROM #despesas
SELECT * FROM #orcamento
SELECT * FROM #centro_de_custo
SELECT * FROM #contas 
SELECT * FROM #LogErros ---------- SELECT PRA VER ERROS DE EXECUÇÃO
*/ 

EXEC DBO.SP_InserirAtualizarDespesasDetalhadas