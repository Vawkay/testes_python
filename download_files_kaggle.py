import sys
import os
import logging
import time
import zipfile
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from webdriver import Driver

# Configura o nível de logging para INFO
# Modos de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(filename='download_files_kaggle.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class KaggleDownload:
    """
    Classe para realizar o download de arquivos do Kaggle.
    """
    def __init__(self):
        self.downloads = self.prepara_downloads()
        self.driver = Driver(download_directory=self.downloads).driver
        self.wait = WebDriverWait(self.driver, 10)
        self.user = os.getenv('KAGGLE_USERNAME')
        self.password = os.getenv('KAGGLE_PASSWORD')
        self.dataset = "https://www.kaggle.com/datasets/thomassimeo/contas-senior-neobpo"

    @staticmethod
    def prepara_downloads():
        """
        Cria o diretório de downloads e limpa os arquivos existentes.
        :return: O caminho do diretório de downloads
        """
        downloads = os.path.join(os.getcwd(), 'DOWNLOADS')
        if not os.path.exists(downloads):
            os.mkdir(downloads)

        [os.remove(os.path.join(downloads, arquivo))
         for arquivo in os.listdir(downloads)
         if os.path.isfile(os.path.join(downloads, arquivo))]
        return downloads

    def login(self):
        """
        Realiza o login via e-mail e senha no Kaggle.
        """
        driver = self.driver
        wait = self.wait
        try:
            driver.get("https://www.kaggle.com/account/login?phase=emailSignIn&returnUrl=%2F")
            # Usuário
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))).send_keys(self.user)
            # Senha
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))).send_keys(self.password)
            # Botão de login
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign In']"))).click()
            # Aguarda a tela inicial do Kaggle
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome')]")))
            logging.info('Login realizado com sucesso')

        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f'Erro ao tentar fazer login: {str(e)}')
            # Verifica se foi erro de senha ou usuário incorretos
            text_error = 'The username or password provided is incorrect.'
            error_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text_error}')]")
            print(error_element.text)
            if error_element:
                logging.error('Usuário ou senha incorretos')
            driver.quit()
            sys.exit(1)

    def aguardar_download(self):
        """Aguarda durante o tempo limite o arquivo ser baixado completamente antes de continuar"""
        ini = time.time()
        limit_time = 60  # Tempo limite em segundos
        while True:
            expected_file = [arquivo for arquivo in os.listdir(self.downloads) if arquivo.endswith('.zip')]
            crdownload_file = [arquivo for arquivo in os.listdir(self.downloads) if arquivo.endswith('.crdownload')]
            tmp_file = [arquivo for arquivo in os.listdir(self.downloads) if arquivo.endswith('.tmp')]
            if expected_file and not crdownload_file and not tmp_file:
                return
            if time.time() - ini >= limit_time:
                raise FileNotFoundError("Tempo limite atingido. O download não foi concluído.")
            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente

    def download(self):
        """Executa o download do arquivo do Kaggle em três tentativas"""
        driver = self.driver
        wait = self.wait
        # Realiza o login no Kaggle
        self.login()
        # Inicia a primeira tentativa de 3 para fazer o download
        for i in range(3):
            try:
                # Acessa a página de datasets da Neo
                driver.get(self.dataset)
                # Clica no botão de download
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='file_download']"))).click()
                # Aguarda o download ser concluído
                self.aguardar_download()
                logging.info('Download concluído')
                driver.quit()
                break
            except (NoSuchElementException, TimeoutException, FileNotFoundError) as e:
                logging.error(f'Tentativa {i + 1} de download falhou: {str(e)}')
            if i == 2:  # Se esta é a última tentativa
                logging.critical('Todas as 3 tentativas de download falharam.')
                driver.quit()
                sys.exit(1)

    def unzip(self):
        """Descompacta o arquivo zip baixado"""
        try:
            file = [arquivo for arquivo in os.listdir(self.downloads) if arquivo.endswith('.zip')][0]
            with zipfile.ZipFile(os.path.join(self.downloads, file), 'r') as zip_ref:
                zip_ref.extractall(self.downloads)
            logging.info('Arquivo descompactado')
        # Tratamento de erros conhecidos e desconhecidos
        except zipfile.BadZipFile:
            logging.error('Arquivo ZIP corrompido ou inválido.')
        except FileNotFoundError:
            logging.error('Arquivo ZIP não encontrado.')
        except Exception as e:
            logging.error(f'Erro desconhecido ao descompactar o arquivo ZIP: {str(e)}')
        # Encerra a instância do zipfile
        finally:
            if zip_ref:
                zip_ref.close()
        logging.info('Processo finalizado com sucesso')


if __name__ == '__main__':
    execute = KaggleDownload()
    execute.download()
    execute.unzip()
