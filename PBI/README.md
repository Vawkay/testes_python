# POWER BI - DESPESAS

O power bi `DESPESAS` � um relat�rio que foi criado para analisar e visualizar dados de despesas de varias contas e centros de custo.
O relat�rio inclui v�rias visualiza��es, como gr�ficos de barras, gr�ficos de linhas, tabelas e cart�es, 
que mostram informa��es sobre despesas por centro de custo, despesas por conta, despesas por m�s, desvios e or�amento.

## Funcionalidade

A O Power BI opera com as seguintes fontes de dados:

**ARQUIVOS CSV**: `CENTRO_DE_CUSTO.csv`, `CONTAS.csv`, `DESPESAS.csv` e `OR�AMENTO.csv`.

As consultas foram criadas com os seguintes comandos em M:

*DESPESAS.csv:*
Tabela contendo os valores de despesas. 
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\DESPESAS.csv"),[Delimiter=";", Columns=7, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Cabe�alhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabe�alhos Promovidos",{{"VLDESPESA", type number}, {"DTBASE", type date}}),
    #"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado",{"MES A"})
in
    #"Colunas Removidas"
```
*ORCAMENTO.csv:*
Tablea contendo os valores de or�amento.
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\ORCAMENTO.csv"),[Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabe�alhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabe�alhos Promovidos",{{"ULTDATA", type date}}),
    #"Valor Substitu�do" = Table.ReplaceValue(#"Tipo Alterado",".",",",Replacer.ReplaceText,{"OR�ADO"}),
    #"Tipo Alterado1" = Table.TransformColumnTypes(#"Valor Substitu�do",{{"OR�ADO", type number}})
in
    #"Tipo Alterado1"
```
*CENTRO_DE_CUSTO.csv:*
Tabela contendo os centros de custo e c�digos
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CENTRO_DE_CUSTO.csv"),[Delimiter=";", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabe�alhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabe�alhos Promovidos",{{"CODIGOCENTROCUSTO", type text}, {"DESCRICAO", type text}, {"CENTROCUSTO", type text}, {"CENTROCUSTO_COD", type text}})
in
    #"Tipo Alterado"
```
*CONTAS.csv:*
Tabela contendo as contas e c�digos
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CONTAS.csv"),[Delimiter=";", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabe�alhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabe�alhos Promovidos",{{"CODCONTA", type text}, {"CONTA", type text}, {"GRUPO", type text}}),
    #"Texto em Mai�scula" = Table.TransformColumns(#"Tipo Alterado",{{"GRUPO", Text.Upper, type text}, {"CONTA", Text.Upper, type text}})
in
    #"Texto em Mai�scula"
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
    // Adiciona Coluna M�s Abreviado em Mai�sculas
    AdicionaMesAbreviado = Table.AddColumn(RenomeiaColuna, "Mes_Abreviado", each Text.Upper(Date.ToText([Data], "MMM"))),
    // Adiciona Coluna N�mero do M�s
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
Tabela de dimens�o com os centros de custo unicos sem repeti��o. 
```m
let
    Fonte = Csv.Document(File.Contents("C:\Users\felip\python\prova_python\PARSED\CENTRO_DE_CUSTO.csv"),[Delimiter=";", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabe�alhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabe�alhos Promovidos",{{"CODIGOCENTROCUSTO", type text}, {"DESCRICAO", type text}, {"CENTROCUSTO", type text}, {"CENTROCUSTO_COD", type text}}),
    #"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado",{"CODIGOCENTROCUSTO", "DESCRICAO"}),
    #"Duplicatas Removidas" = Table.Distinct(#"Colunas Removidas"),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Duplicatas Removidas",{{"CENTROCUSTO_COD", "CC_COD_MASTER"}, {"CENTROCUSTO", "CC_NOME"}})
in
    #"Colunas Renomeadas"
```
*dAtualiza��o_BI:*
Tabela de dimens�o que mostra a data da �ltima atualiza��o do BI.
```m
let
    Fonte = DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(),-3)),
    #"Convertido para Tabela" = #table(1, {{Fonte}}),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Convertido para Tabela",{{"Column1", "Data Hora"}}),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Colunas Renomeadas",{{"Data Hora", type datetime}})
in
    #"Tipo Alterado"
```

