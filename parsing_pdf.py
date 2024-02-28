import os
import pandas as pd
import pdfplumber


class ParsePdf:
    """
    Classe para analisar um arquivo PDF e extrair os dados da tabela.
    """
    def __init__(self):
        self.folder = self.prepara_folder()
        self.pdf_file = self.encontra_arquivo()

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
        Encontra o arquivo PDF no diretório de downloads.
        :return: O caminho do arquivo PDF
        """
        try:
            # Diretório de downloads
            downloads = os.path.join(os.getcwd(), 'DOWNLOADS')
            # Lista os arquivos XML no diretório de downloads
            file_list = [downloads + "\\" + f for f in os.listdir(downloads) if f.endswith(".pdf")]
            pdf_file = file_list[0]
            return pdf_file
        except Exception as e:
            print(f"Erro ao encontrar o arquivo: {e}")
            return None

    @staticmethod
    def parse_pdf(file_path):
        """
        Analisa o arquivo PDF e retorna um DataFrame com os dados da tabela.
        :param file_path:
        :return: DataFrame com os dados da tabela
        """
        try:
            # Lista para armazenar todos os DataFrames
            valores = []

            with pdfplumber.open(file_path) as pdf:
                # Iterar sobre todas as páginas do PDF
                for page in pdf.pages:
                    # Extrair a tabela da página atual
                    table = page.extract_table()
                    for item in table:
                        # Inserir na lista
                        valores.append(item)

            # Concatenar todos os DataFrames na lista em um único DataFrame
            dataframe = pd.DataFrame(valores, columns=valores[0])
            # Remover a linha 0 (Antigo cabeçalho)
            dataframe = dataframe.drop([0])
            # Remover Coluna None
            dataframe.drop(columns=[None], inplace=True)
            return dataframe
        except Exception as e:
            print(f"Erro ao analisar o PDF: {e}")
            return None

    def salva_arquivo(self, dataframe):
        """
        Salva o DataFrame em um arquivo CSV.
        :param dataframe: DataFrame com os dados da tabela
        """
        try:
            # Salvar o DataFrame em um arquivo CSV
            file_path = os.path.join(self.folder, 'CENTRO_DE_CUSTO.csv')
            dataframe.to_csv(file_path, index=False, encoding='ANSI', sep=';')
            print(f"Arquivo salvo em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")


if __name__ == '__main__':

    try:
        execute = ParsePdf()
        pdf_file = execute.encontra_arquivo()
        if pdf_file is not None:
            df = execute.parse_pdf(pdf_file)
            if df is not None:
                execute.salva_arquivo(df)

    except Exception as e:
        print(f"Erro ao executar o programa: {e}")
