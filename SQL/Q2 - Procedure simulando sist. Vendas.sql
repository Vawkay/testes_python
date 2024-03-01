ALTER PROCEDURE dbo.RealizarVenda
    @IDProduto INT,
    @QuantidadeVendida INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @QuantidadeEstoqueAtual INT;

    -- Iniciar a transação
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Verificar a quantidade em estoque do produto
        SELECT @QuantidadeEstoqueAtual = QuantidadeEstoque
        FROM DB_TESTE.dbo.Produtos
        WHERE IDProduto = @IDProduto;

        -- Verificar se há estoque suficiente para a venda
        IF @QuantidadeEstoqueAtual >= @QuantidadeVendida
        BEGIN
			-- Obter o último ID de venda
			DECLARE @UltimoIDVenda INT;
			SET @UltimoIDVenda = (SELECT MAX(IDVenda)+ 1 FROM dbo.Vendas);
			-- Registrar a venda
			INSERT INTO DB_TESTE.dbo.Vendas (IDVenda, IDProduto, QuantidadeVendida, TimestampVenda)
			VALUES (@UltimoIDVenda, @IDProduto, @QuantidadeVendida, GETDATE());

			-- Atualizar o estoque
			UPDATE DB_TESTE.dbo.Produtos
			SET QuantidadeEstoque = @QuantidadeEstoqueAtual - @QuantidadeVendida
			WHERE IDProduto = @IDProduto;


            -- Confirmar a transação
            COMMIT;

            PRINT 'Venda realizada com sucesso!';
        END
        ELSE
        BEGIN
            -- Rolback se não houver estoque suficiente
            ROLLBACK;
            PRINT 'Estoque insuficiente. A venda não pode ser concluída.';
        END
    END TRY
	BEGIN CATCH
		-- Rollback em caso de erro
		IF @@TRANCOUNT > 0
		BEGIN
			ROLLBACK;
		END

		DECLARE @ErrorMessage NVARCHAR(4000);
		DECLARE @ErrorSeverity INT;
		DECLARE @ErrorState INT;

		SELECT
			@ErrorMessage = ERROR_MESSAGE(),
			@ErrorSeverity = ERROR_SEVERITY(),
			@ErrorState = ERROR_STATE();

		PRINT 'Erro durante a venda. A transação foi revertida.';
		PRINT 'Mensagem de erro: ' + @ErrorMessage;
		PRINT 'Gravidade do erro: ' + CAST(@ErrorSeverity AS NVARCHAR(10));
		PRINT 'Estado do erro: ' + CAST(@ErrorState AS NVARCHAR(10));
	END CATCH
END;

/* ################### Ex. de uso ######################## */ 
EXEC RealizarVenda @IDProduto = 2, @QuantidadeVendida = 15;