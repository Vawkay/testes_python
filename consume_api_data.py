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
        Cria o diretório de parsers
        :return: O caminho do diretório de downloads
        """
        folder = os.path.join(os.getcwd(), 'PARSED')
        if not os.path.exists(folder):
            os.mkdir(folder)

        logging.info('Diretório de downloads preparado.')
        return folder

    def verifica_data(self):
        """
        Verifica a última atualização de arquivos salvos no diretório de downloads, abre o arquivo e verifica a data
        mais recente que contém dados na coluna 'Atualizado_em'.
        :return: A data mais recente que contém dados.
        """
        # Lista todos os arquivos no diretório
        arquivos = [f for f in os.listdir(self.downloads) if os.path.isfile(os.path.join(self.downloads, f))]
        # Encontra o arquivo mais recente
        mais_recente = max(arquivos, key=lambda x: os.path.getmtime(os.path.join(self.downloads, x)))
        # Abrir o arquivo mais recente e adquirir a data mais recente que contém dados
        dataframe = pd.read_csv(os.path.join(self.downloads, mais_recente))
        # Adquirir a data mais recente que contém dados do arquivo
        ultima_atualizacao = dataframe['Atualizado_em'].max()
        logging.info('Data da última atualização verificada.')
        return ultima_atualizacao

    def test_api(self):
        """
        API de teste com parâmetros supostos para consumo.
        Consume a API de acordo com parâmetros e salva os dados em um arquivo CSV.
        É só um modelo, não funciona porque os parâmetros são fictícios.
        """
        page = 1
        lista_dataframes = []
        while True:
            headers = {'Authorization': f'Bearer {self.token}'}
            # Faz uma solicitação GET à API com o token de acesso no cabeçalho
            # Parâmetros de paginação e última atualização
            response = requests.get(
                f'https://sheetdb.io/api/v1/xlc7njblhysnw?page={page}&search?data=>{self.verifica_data()}',
                headers=headers)
            logging.info(f'Solicitação GET feita à API. Página: {page}')

            # Verifica se a resposta da requisição foi bem-sucedida
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(f"Erro: {str(e)} - {response.text}")
                return

            # Converte a resposta em um dicionário Python
            data = response.json()

            # Se a resposta estiver vazia, não há mais dados para consumir
            if not data:
                break

            # Converte o dicionário em um DataFrame do pandas
            df = pd.DataFrame(data)

            # Adiciona o DataFrame à lista de DataFrames
            lista_dataframes.append(df)
            # Avança para a próxima página
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
        API real sem parâmetros para consumo.
        """
        response = requests.get(self.api)
        logging.info(f'Solicitação GET feita à API.')
        # Verifica se a resposta da requisição foi bem-sucedida
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro: {str(e)} - {response.text}")
            return
        # Converte a resposta em um dicionário Python
        data = response.json()
        # Verifica se a resposta está vazia
        if not data:
            logging.info('A resposta da API está vazia.')
            return
        # Converte o dicionário em um DataFrame do pandas
        df = pd.DataFrame(data)
        # Salva o DataFrame em um arquivo CSV
        self.salvar_arquivo(df)


if __name__ == '__main__':
    api = ConsumeApiData()
    # API de teste com supostos parâmetros
    # api.test_api()
    # API real sem parâmetros
    api.real_api()
    logging.info('Script concluído.')
