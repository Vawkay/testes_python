import requests
import pandas as pd
import os
import logging
from datetime import datetime

# Configura o logger
logging.basicConfig(filename='consume_api_data.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class ConsumeApiData:
    """
    Classe para consumir a API e salvar os dados em um arquivo CSV.
    """

    def __init__(self):
        self.downloads = self.prepara_folder()
        self.token = os.getenv('API_TESTE_TOKEN')
        self.api = "https://sheetdb.io/api/v1/xlc7njblhysnw"

    @staticmethod
    def prepara_folder():
        """
        Cria o diret�rio de parsers
        :return: O caminho do diret�rio de downloads
        """
        folder = os.path.join(os.getcwd(), 'PARSED')
        if not os.path.exists(folder):
            os.mkdir(folder)

        logging.info('Diret�rio de downloads preparado.')
        return folder

    def verifica_data(self):
        """
        Verifica a �ltima atualiza��o de arquivos salvos no diret�rio de downloads, abre o arquivo e verifica a data
        mais recente que cont�m dados na coluna 'Atualizado_em'.
        :return: A data mais recente que cont�m dados.
        """
        # Lista todos os arquivos no diret�rio
        arquivos = [f for f in os.listdir(self.downloads) if os.path.isfile(os.path.join(self.downloads, f))]
        # Encontra o arquivo mais recente
        mais_recente = max(arquivos, key=lambda x: os.path.getmtime(os.path.join(self.downloads, x)))
        # Abrir o arquivo mais recente e adquirir a data mais recente que cont�m dados
        dataframe = pd.read_csv(os.path.join(self.downloads, mais_recente))
        # Adquirir a data mais recente que cont�m dados do arquivo
        ultima_atualizacao = dataframe['Atualizado_em'].max()
        logging.info('Data da �ltima atualiza��o verificada.')
        return ultima_atualizacao

    def test_api(self):
        """
        API de teste com par�metros supostos para consumo.
        Consume a API de acordo com par�metros e salva os dados em um arquivo CSV.
        � s� um modelo, n�o funciona porque os par�metros s�o fict�cios.
        """
        page = 1
        lista_dataframes = []
        while True:
            headers = {'Authorization': f'Bearer {self.token}'}
            # Faz uma solicita��o GET � API com o token de acesso no cabe�alho
            # Par�metros de pagina��o e �ltima atualiza��o
            response = requests.get(
                f'https://sheetdb.io/api/v1/xlc7njblhysnw?page={page}&search?data=>{self.verifica_data()}',
                headers=headers)
            logging.info(f'Solicita��o GET feita � API. P�gina: {page}')

            # Verifica se a resposta da requisi��o foi bem-sucedida
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(f"Erro: {str(e)} - {response.text}")
                return

            # Converte a resposta em um dicion�rio Python
            data = response.json()

            # Se a resposta estiver vazia, n�o h� mais dados para consumir
            if not data:
                break

            # Converte o dicion�rio em um DataFrame do pandas
            df = pd.DataFrame(data)

            # Adiciona o DataFrame � lista de DataFrames
            lista_dataframes.append(df)
            # Avan�a para a pr�xima p�gina
            page += 1

        df = pd.concat(lista_dataframes, ignore_index=True)
        df['Atualizado_em'] = datetime.now()
        # Salva o DataFrame em um arquivo CSV
        self.salvar_arquivo(df)

    def salvar_arquivo(self, dataframe):
        """
        Salva o DataFrame em um arquivo CSV.
        :param dataframe: DataFrame com os dados da tabela
        """
        try:
            # Salvar o DataFrame em um arquivo CSV
            file_path = os.path.join(self.downloads, 'CONTAS.csv')
            dataframe.to_csv(file_path, index=False, encoding='utf-8', sep=';')
            logging.info('Dados salvos em um arquivo CSV.')
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo: {e}")

    def real_api(self):
        """
        API real sem par�metros para consumo.
        """
        response = requests.get(self.api)
        logging.info(f'Solicita��o GET feita � API.')
        # Verifica se a resposta da requisi��o foi bem-sucedida
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro: {str(e)} - {response.text}")
            return
        # Converte a resposta em um dicion�rio Python
        data = response.json()
        # Verifica se a resposta est� vazia
        if not data:
            logging.info('A resposta da API est� vazia.')
            return
        # Converte o dicion�rio em um DataFrame do pandas
        df = pd.DataFrame(data)
        # Salva o DataFrame em um arquivo CSV
        self.salvar_arquivo(df)


if __name__ == '__main__':
    api = ConsumeApiData()
    # API de teste com supostos par�metros
    # api.test_api()
    # API real sem par�metros
    api.real_api()
    logging.info('Script conclu�do.')
