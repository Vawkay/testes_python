import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from babel.dates import format_date, parse_date, get_day_names, get_month_names


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
        Cria o diret�rio de parsers
        :return: O caminho do diret�rio de downloads
        """
        folder = os.path.join(os.getcwd(), 'PARSED')
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder

    @staticmethod
    def encontra_arquivo():
        """
        Encontra o arquivo XML no diret�rio de downloads.
        :return: O caminho do arquivo XML
        """
        try:
            # Diret�rio de downloads
            downloads = os.path.join(os.getcwd(), 'DOWNLOADS')
            # Lista os arquivos XML no diret�rio de downloads
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

            # Inicializa uma lista para armazenar os dicion�rios
            data = []
            # Itera sobre cada elemento 'OR�AMENTO' no XML
            for item in root.iter('OR�AMENTO'):
                # Inicializa um dicion�rio para armazenar os dados do elemento 'OR�AMENTO'
                dados = {}
                # Itera sobre cada filho do elemento 'OR�AMENTO'
                for child in item:
                    # Adiciona a tag e o texto do filho ao dicion�rio
                    # Se o texto for None (tag vazia), substitui por uma string vazia
                    dados[child.tag] = child.text if child.text is not None else ""
                # Adiciona o dicion�rio � lista
                data.append(dados)

            # Cria um DataFrame a partir da lista de dicion�rios
            dataframe = pd.DataFrame(data)

            def convert_date(date_str):
                try:
                    # Divida a string usando espa�os como separadores
                    partes = date_str.split()

                    # Extrai os elementos relevantes
                    dia = int(partes[-5])
                    mes = partes[-3].lower()  # Obt�m o nome do m�s em min�sculas
                    ano = int(partes[-1])

                    # Mapeia o nome do m�s para o n�mero do m�s
                    meses = {'janeiro': 1, 'fevereiro': 2, 'mar�o': 3, 'abril': 4,
                             'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                             'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12}
                    mes_numero = meses[mes]

                    # Constr�i o objeto datetime
                    data_formatada = datetime(ano, mes_numero, dia)
                    return data_formatada

                except (ValueError, IndexError, KeyError):
                    # Se houver algum erro, retorna a data original
                    return date_str

            dataframe['ULTDATA'] = dataframe['ULTDATA'].apply(convert_date)

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
            dataframe.to_csv(file_path, index=False, encoding='utf-8', sep=';')
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
