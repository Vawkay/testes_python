# Scripts Python

Este projeto cont�m v�rios scripts Python que realizam tarefas espec�ficas, como consumir dados de uma API, analisar arquivos PDF e XML, e automatizar a��es em um navegador da web usando Selenium WebDriver. Abaixo est�o os detalhes de cada script.

## consume_api_data.py

Este script Python cont�m a classe `ConsumeApiData`, que � usada para consumir dados de uma API e salvar os dados em um arquivo CSV. A classe possui os seguintes m�todos:

- `prepara_folder()`: Cria o diret�rio para armazenar os dados baixados.
- `verifica_data()`: Verifica a data da �ltima atualiza��o dos arquivos salvos no diret�rio de downloads.
- `test_api()`: Consome a API de teste com par�metros supostos e salva os dados em um arquivo CSV.
- `salvar_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.
- `real_api()`: Consome a API real sem par�metros.

## parsing_pdf.py

Este script Python cont�m a classe `ParsePdf`, que � usada para analisar um arquivo PDF e extrair os dados da tabela. A classe possui os seguintes m�todos:

- `prepara_folder()`: Cria o diret�rio para armazenar os dados extra�dos.
- `encontra_arquivo()`: Encontra o arquivo PDF no diret�rio de downloads.
- `parse_pdf(file_path)`: Analisa o arquivo PDF e retorna um DataFrame com os dados da tabela.
- `salva_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.

## parsing_xml.py

Este script Python cont�m a classe `ParseXml`, que � usada para analisar um arquivo XML e extrair os dados da tabela. A classe possui os seguintes m�todos:

- `prepara_folder()`: Cria o diret�rio para armazenar os dados extra�dos.
- `encontra_arquivo()`: Encontra o arquivo XML no diret�rio de downloads.
- `parse_xml(file_path)`: Analisa o arquivo XML e retorna um DataFrame com os dados da tabela.
- `salva_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.

## webdriver.py

Este script Python cont�m a classe `Driver`, que representa um Selenium WebDriver. A classe possui os seguintes m�todos:

- `setup()`: Inicializa e configura o WebDriver.

## download_files_kaggle.py

Este script Python cont�m a classe `KaggleDownload`, que � usada para realizar o download de arquivos do Kaggle. A classe possui os seguintes m�todos:

- `prepara_downloads()`: Cria o diret�rio de downloads e limpa os arquivos existentes.
- `login()`: Realiza o login via e-mail e senha no Kaggle.
- `aguardar_download()`: Aguarda durante o tempo limite o arquivo ser baixado completamente antes de continuar.
- `download()`: Executa o download do arquivo do Kaggle em tr�s tentativas.
- `unzip()`: Descompacta o arquivo zip baixado.