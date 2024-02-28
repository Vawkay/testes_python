import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime


class ParseXml:
    """
    Classe para analisar um arquivo XML e extrair os dados da tabela.
    """
    def __init__(self):
        self.folder = self.prepara_folder()
        self.xml_file = self.encontra_arquivo()

    @staticmethod
    def prepara_folder():
        """
        Cria o diretório de parsers
        :return: O caminho do diretório de downloads
        """
        folder = os.path.join(os.getcwd(), 'PARSED')
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder

    @staticmethod
    def encontra_arquivo():
        """
        Encontra o arquivo XML no diretório de downloads.
        :return: O caminho do arquivo XML
        """
        try:
            # Diretório de downloads
            downloads = os.path.join(os.getcwd(), 'DOWNLOADS')
            # Lista os arquivos XML no diretório de downloads
            file_list = [downloads + "\\" + f for f in os.listdir(downloads) if f.endswith(".xml")]
            xml_file = file_list[0]
            return xml_file
        except Exception as e:
            print(f"Erro ao encontrar o arquivo: {e}")
            return None

    @staticmethod
    def parse_xml(file_path):
        """
        Analisa o arquivo XML e retorna um DataFrame com os dados da tabela.
        :param file_path:
        :return: DataFrame com os dados da tabela
        """
        try:
            # Carrega e analisa o arquivo XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Inicializa uma lista para armazenar os dicionários
            data = []
            # Itera sobre cada elemento 'ORÇAMENTO' no XML
            for item in root.iter('ORÇAMENTO'):
                # Inicializa um dicionário para armazenar os dados do elemento 'ORÇAMENTO'
                dados = {}
                # Itera sobre cada filho do elemento 'ORÇAMENTO'
                for child in item:
                    # Adiciona a tag e o texto do filho ao dicionário
                    # Se o texto for None (tag vazia), substitui por uma string vazia
                    dados[child.tag] = child.text if child.text is not None else ""
                # Adiciona o dicionário à lista
                data.append(dados)

            # Cria um DataFrame a partir da lista de dicionários
            dataframe = pd.DataFrame(data)
            return dataframe
        except Exception as e:
            print(f"Erro ao analisar o XML: {e}")
            return None

    def salva_arquivo(self, dataframe):
        """
        Salva o DataFrame em um arquivo CSV.
        :param dataframe: DataFrame com os dados da tabela
        """
        try:
            # Salvar o DataFrame em um arquivo CSV
            file_path = os.path.join(self.folder, 'ORCAMENTO.csv')
            dataframe.to_csv(file_path, index=False, encoding='ANSI', sep=';')
            print(f"Arquivo salvo em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")


if __name__ == '__main__':

    try:
        execute = ParseXml()
        xml_file = execute.encontra_arquivo()
        if xml_file is not None:
            df = execute.parse_xml(xml_file)
            if df is not None:
                execute.salva_arquivo(df)

    except Exception as e:
        print(f"Erro ao executar o programa: {e}")