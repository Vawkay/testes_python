# Scripts Python

Este projeto contém vários scripts Python que realizam tarefas específicas, como consumir dados de uma API, analisar arquivos PDF e XML, e automatizar ações em um navegador da web usando Selenium WebDriver. Abaixo estão os detalhes de cada script.

## consume_api_data.py

Este script Python contém a classe `ConsumeApiData`, que é usada para consumir dados de uma API e salvar os dados em um arquivo CSV. A classe possui os seguintes métodos:

- `prepara_folder()`: Cria o diretório para armazenar os dados baixados.
- `verifica_data()`: Verifica a data da última atualização dos arquivos salvos no diretório de downloads.
- `test_api()`: Consome a API de teste com parâmetros supostos e salva os dados em um arquivo CSV.
- `salvar_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.
- `real_api()`: Consome a API real sem parâmetros.

## parsing_pdf.py

Este script Python contém a classe `ParsePdf`, que é usada para analisar um arquivo PDF e extrair os dados da tabela. A classe possui os seguintes métodos:

- `prepara_folder()`: Cria o diretório para armazenar os dados extraídos.
- `encontra_arquivo()`: Encontra o arquivo PDF no diretório de downloads.
- `parse_pdf(file_path)`: Analisa o arquivo PDF e retorna um DataFrame com os dados da tabela.
- `salva_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.

## parsing_xml.py

Este script Python contém a classe `ParseXml`, que é usada para analisar um arquivo XML e extrair os dados da tabela. A classe possui os seguintes métodos:

- `prepara_folder()`: Cria o diretório para armazenar os dados extraídos.
- `encontra_arquivo()`: Encontra o arquivo XML no diretório de downloads.
- `parse_xml(file_path)`: Analisa o arquivo XML e retorna um DataFrame com os dados da tabela.
- `salva_arquivo(dataframe)`: Salva o DataFrame em um arquivo CSV.

## webdriver.py

Este script Python contém a classe `Driver`, que representa um Selenium WebDriver. A classe possui os seguintes métodos:

- `setup()`: Inicializa e configura o WebDriver.

## download_files_kaggle.py

Este script Python contém a classe `KaggleDownload`, que é usada para realizar o download de arquivos do Kaggle. A classe possui os seguintes métodos:

- `prepara_downloads()`: Cria o diretório de downloads e limpa os arquivos existentes.
- `login()`: Realiza o login via e-mail e senha no Kaggle.
- `aguardar_download()`: Aguarda durante o tempo limite o arquivo ser baixado completamente antes de continuar.
- `download()`: Executa o download do arquivo do Kaggle em três tentativas.
- `unzip()`: Descompacta o arquivo zip baixado.