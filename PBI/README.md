# POWER BI - DESPESAS

O power bi `DESPESAS` é um relatório que foi criado para analisar e visualizar dados de despesas de varias contas e centros de custo.
O relatório inclui várias visualizações, como gráficos de barras, gráficos de linhas, tabelas e cartões, 
que mostram informações sobre despesas por centro de custo, despesas por conta, despesas por mês, desvios e orçamento.

## Funcionalidade

A O Power BI opera com as seguintes fontes de dados:

**ARQUIVOS CSV**: `CENTRO_DE_CUSTO.csv`, `CONTAS.csv`, `DESPESAS.csv` e `ORÇAMENTO.csv`.

As consultas foram criadas com os seguintes comandos em M:

*DESPESAS.csv:*
Tabela contendo os valores de despesas. 
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\DESPESAS.csv"),[Delimiter=";", Columns=7, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"VLDESPESA", type number}, {"DTBASE", type date}}),
    #"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado",{"MES A"})
in
    #"Colunas Removidas"
```
*ORCAMENTO.csv:*
Tablea contendo os valores de orçamento.
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\ORCAMENTO.csv"),[Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"ULTDATA", type date}}),
    #"Valor Substituído" = Table.ReplaceValue(#"Tipo Alterado",".",",",Replacer.ReplaceText,{"ORÇADO"}),
    #"Tipo Alterado1" = Table.TransformColumnTypes(#"Valor Substituído",{{"ORÇADO", type number}})
in
    #"Tipo Alterado1"
```
*CENTRO_DE_CUSTO.csv:*
Tabela contendo os centros de custo e códigos
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CENTRO_DE_CUSTO.csv"),[Delimiter=";", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"CODIGOCENTROCUSTO", type text}, {"DESCRICAO", type text}, {"CENTROCUSTO", type text}, {"CENTROCUSTO_COD", type text}})
in
    #"Tipo Alterado"
```
*CONTAS.csv:*
Tabela contendo as contas e códigos
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CONTAS.csv"),[Delimiter=";", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"CODCONTA", type text}, {"CONTA", type text}, {"GRUPO", type text}}),
    #"Texto em Maiúscula" = Table.TransformColumns(#"Tipo Alterado",{{"GRUPO", Text.Upper, type text}, {"CONTA", Text.Upper, type text}})
in
    #"Texto em Maiúscula"
```
*dCalendario:*
Tabela de datas divindo em dias, meses e anos.
```m
let
    AnoInicial = 2021,
    AnoFinal = Date.Year(DateTime.LocalNow()),
    // Declara uma data inicial
    DataInicial = Date.StartOfYear(#date(AnoInicial, 1, 1)),
    // Declara uma data final
    DataFinal = Date.EndOfYear(#date(AnoFinal, 12, 31)),
    // Conta a quantidade de dias entre as duas datas
    QtdeDias = Duration.Days(DataFinal - DataInicial) + 1,
    // Cria lista de datas
    Datalist = List.Dates(DataInicial, QtdeDias, #duration(1, 0, 0, 0)),
    // Converter para Tabela
    ConvertTabela = Table.FromList(Datalist, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    // Altera Tipo
    AlteraTipo = Table.TransformColumnTypes(ConvertTabela, {{"Column1", type date}}),
    // Renomeia Coluna e adiciona Coluna Dia_Mes
    RenomeiaColuna = Table.RenameColumns(Table.AddColumn(AlteraTipo, "Dia_Mes", each Text.From(Date.Day([Column1])) & "/" & Date.ToText([Column1], "MMM")), {{"Column1", "Data"}}),
    // Adiciona Coluna Mês Abreviado em Maiúsculas
    AdicionaMesAbreviado = Table.AddColumn(RenomeiaColuna, "Mes_Abreviado", each Text.Upper(Date.ToText([Data], "MMM"))),
    // Adiciona Coluna Número do Mês
    AdicionaNumeroMes = Table.AddColumn(AdicionaMesAbreviado, "Numero_Mes", each Date.Month([Data])),
    // Adiciona Coluna Ano
    AdicionaAno = Table.AddColumn(AdicionaNumeroMes, "Ano", each Date.Year([Data])),
    // Adiciona Coluna Dia
    AdicionaDia = Table.AddColumn(AdicionaAno, "Dia", each Date.Day([Data])),
    //Altera o tipo
    #"Tipo Alterado" = Table.TransformColumnTypes(AdicionaDia,{{"Numero_Mes", Int64.Type}, {"Dia", Int64.Type}})
in
    #"Tipo Alterado"
```
*dCENTRO_DE_CUSTO_MASTER:*
Tabela de dimensão com os centros de custo unicos sem repetição. 
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CENTRO_DE_CUSTO.csv"),[Delimiter=";", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"CODIGOCENTROCUSTO", type text}, {"DESCRICAO", type text}, {"CENTROCUSTO", type text}, {"CENTROCUSTO_COD", type text}}),
    #"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado",{"CODIGOCENTROCUSTO", "DESCRICAO"}),
    #"Duplicatas Removidas" = Table.Distinct(#"Colunas Removidas"),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Duplicatas Removidas",{{"CENTROCUSTO_COD", "CC_COD_MASTER"}, {"CENTROCUSTO", "CC_NOME"}})
in
    #"Colunas Renomeadas"
```
*dAtualização_BI:*
Tabela de dimensão que mostra a data da última atualização do BI.
```m
let
    Fonte = DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(),-3)),
    #"Convertido para Tabela" = #table(1, {{Fonte}}),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Convertido para Tabela",{{"Column1", "Data Hora"}}),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Colunas Renomeadas",{{"Data Hora", type datetime}})
in
    #"Tipo Alterado"
```

