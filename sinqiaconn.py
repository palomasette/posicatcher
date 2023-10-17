from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import shutil
import time
from datetime import datetime
from credentials import URL_SINQIA
root_dir = os.getcwd()
data_hoje = datetime.today().strftime("%d%m%Y")

class Connect:
    def __init__(self) -> None:
        self.user = None
        self.download_dir = os.path.expanduser('~') + '\\Downloads'

    
    def get_224(self, cd_cliente, cd_fundo, user, password):
        service = Service(
            fr'Chromedriver\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        #driver.maximize_window()
        #driver.switch_to.window(driver.current_window_handle)
        driver.get(URL_SINQIA)
        long_time_ago = str(
            (datetime.today() - timedelta(days=5000)).strftime("%d%m%Y"))
        data_hoje = datetime.today().strftime("%d%m%Y")
        wait = WebDriverWait(driver, 10)

        # XPath do input de usuários - psette
        input_user = driver.find_element(by=By.XPATH, value='//*[@id="Usr"]')
        input_user.send_keys(user)
        inputPassword = driver.find_element(
            by=By.XPATH, value='//*[@id="Pwd"]')  # XPath do input de senha
        inputPassword.send_keys(password)
        # clicando no botão "entrar" para acessar a Sinqia
        driver.find_element("xpath", '//*[@id="btnSubmit"]').click()
        sleep(1)
        inputBuscaProcessos = driver.find_element(
            by=By.XPATH, value='//*[@id="txArgBusca"]')  # textbox busca de processos na Sinqia
        inputBuscaProcessos.send_keys("224")  # enviando 224 para a textbox
        # clicando na lupa para a busca de processos
        driver.find_element(
            "xpath", '//*[@id="search-bar"]/table/tbody/tr/td[2]/a/img').click()
        # *******************************************************************************

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="td_rbClassificacao_0_label"]/label')))
        xpath_class_cod_cli = driver.find_element(
            'xpath', value='//*[@id="td_rbClassificacao_0_label"]/label').click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/fieldset/table/tbody/tr[1]/td/table/tbody/tr/td/input')))
        xpath_tipo_mov_todos = driver.find_element(
            'xpath', value='/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/fieldset/table/tbody/tr[1]/td/table/tbody/tr/td/input').click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id = "el_ipPortfolio_tdiiCod"]/input')))
        xpath_carteira = driver.find_element(
            by=By.XPATH, value='//*[@id = "el_ipPortfolio_tdiiCod"]/input')
        sleep(1)
        for dig in cd_fundo:
            xpath_carteira.send_keys(dig)
            sleep(1)
        sleep(2)

        input_data_ini = driver.find_element(
            'xpath', value='//*[@id="el_cp_irdtPeriodoi_dateField"]').click()
        sleep(1)
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        sleep(1)
        for num in long_time_ago:
            ActionChains(driver)\
                .send_keys(num)\
                .perform()
        sleep(1)
        input_data_fim = driver.find_element(
            'xpath', value='//*[@id="el_cp_irdtPeriodof_dateField"]').click()
        sleep(1)
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        sleep(1)
        for num in data_hoje:
            ActionChains(driver)\
                .send_keys(num)\
                .perform()
            
        xpath_cliente_inicial = driver.find_element(
            'xpath', value='/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td[2]/input').click()
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        for letra in cd_cliente:
            ActionChains(driver)\
                .send_keys(letra)\
                .perform()
            sleep(1)
        sleep(2)
        xpath_cliente_final = driver.find_element(
            'xpath', value='/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[2]/td[2]/input').click()
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        for letra in cd_cliente:
            ActionChains(driver)\
                .send_keys(letra)\
                .perform()
            sleep(1)

        sleep(1)
        # caixa de seleção do formato de saída
        driver.find_element("xpath", '//*[@id="el_irotOutputType_selROT"]').click()
        ActionChains(driver)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ENTER)\
            .perform()

        # clicando na checkbox de Download
        driver.find_element("xpath", '//*[@id="chk42"]').click()
        # clicando em 'OK'
        driver.find_element(
            "xpath", '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/button').click()
        
        def arquivo_mais_recente(pasta):
            arquivos = glob.glob(os.path.join(pasta, '*'))
            arquivos.sort(key=os.path.getmtime, reverse=True)
            
            if arquivos:
                if ".crdownload" not in arquivos[0]:
                    return arquivos[0]
            else:
                return None

        #funçao para certificar de que será considerado o arquivo correto
        # o ultimo arquivo baixado precisa ter "Posição de Cotistas" e não ter
        # a extensão '.crdownload' no final. E também precisa ter sido baixado há menos
        # de 5 segundos atrás
        def atende_condicoes(arquivo):
            tempo_atual = time.time()
            cinco_segundos_atras = tempo_atual - 5
            if os.path.getmtime(arquivo) < cinco_segundos_atras:
                return False
            if "Mapa de Movimentos" not in arquivo:
                return False
            if arquivo.endswith(".crdownload"):
                return False
            return True

        def verifica_diretorio_downloads(download_dir):
            while True:
                arquivo_mais_novo = arquivo_mais_recente(download_dir)
                #print(f"arquivo mais recente: {arquivo_mais_novo}")
                if arquivo_mais_novo and atende_condicoes(arquivo_mais_novo):
                    return arquivo_mais_novo
                sleep(1)
                    
        arquivo_45_pos_cot = verifica_diretorio_downloads(self.download_dir)
        return arquivo_45_pos_cot


    def get_45(self, cd_cliente, cd_fundo, user, password):
        try:
            service = Service(
                fr'Chromedriver\chromedriver.exe')
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            #driver.maximize_window()
            driver.switch_to.window(driver.current_window_handle)
        except:
            erro = 1
            print('erro ao abrir chrome')
        driver.get(URL_SINQIA)
        wait = WebDriverWait(driver, 10)

        xpath_carteira = '//*[@id="el_ip_tdiiCod"]/input'
        xpath_cliente_inicial = '//*[@id="el_iis_iaInitial"]/input'
        xpath_cliente_final = '//*[@id="el_iis_iaFinal"]/input'
        xpath_data = '//*[@id="el_cp_idtDataEmis_dateField"]'
        xpath_selec_filetype = '//*[@id="el_irotOutputType_selROT"]'
        xpath_check_download = '//*[@id="chk11"]'
        xpath_bt_ok = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[3]/button'
        
        day_past = str(
            (datetime.today() - timedelta(days=7)).strftime("%d%m%Y"))
        
        # XPath do input de usuários
        input_user = driver.find_element(by=By.XPATH, value='//*[@id="Usr"]')
        input_user.send_keys(user)
        inputPassword = driver.find_element(
            by=By.XPATH, value='//*[@id="Pwd"]')  # XPath do input de senha
        inputPassword.send_keys(password)
        # clicando no botão "entrar" para acessar a Sinqia
        driver.find_element("xpath", '//*[@id="btnSubmit"]').click()
        sleep(1)
        inputBuscaProcessos = driver.find_element(
            by=By.XPATH, value='//*[@id="txArgBusca"]')  # textbox busca de processos na Sinqia
        inputBuscaProcessos.send_keys("45")  # enviando 224 para a textbox
        # clicando na lupa para a busca de processos
        driver.find_element(
            "xpath", '//*[@id="search-bar"]/table/tbody/tr/td[2]/a/img').click()
        # *******************************************************************************

        input_carteira = driver.find_element(
            by=By.XPATH, value=xpath_carteira)
        for dig in cd_fundo:
            input_carteira.send_keys(dig)
            sleep(1)
        
        input_cliente_inicial = driver.find_element(
            'xpath', value=xpath_cliente_inicial).click()
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        for letra in cd_cliente:
            ActionChains(driver)\
                .send_keys(letra)\
                .perform()
            sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_cliente_final)))

        input_cliente_final = driver.find_element(
            'xpath', value=xpath_cliente_final).click()
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        for num in cd_cliente:
            ActionChains(driver)\
                .send_keys(num)\
                .perform()
            sleep(1)
        
        input_data = driver.find_element(
            'xpath', value=xpath_data).click()
        sleep(1)
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('A')\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.BACKSPACE)\
            .perform()
        sleep(1)
        for num in day_past:
            ActionChains(driver)\
                .send_keys(num)\
                .perform()

        # caixa de seleção do formato de saída
        driver.find_element("xpath", xpath_selec_filetype).click()
        ActionChains(driver)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ARROW_DOWN)\
            .send_keys(Keys.ENTER)\
            .perform()

        # clicando na checkbox de Download
        driver.find_element("xpath", xpath_check_download).click()
        # clicando em 'OK'
        driver.find_element(
            "xpath", xpath_bt_ok).click()
        
        def arquivo_mais_recente(pasta):
            arquivos = glob.glob(os.path.join(pasta, '*'))
            arquivos.sort(key=os.path.getmtime, reverse=True)
            
            if arquivos:
                if ".crdownload" not in arquivos[0]:
                    return arquivos[0]
            else:
                return None

        #funçao para certificar de que será considerado o arquivo correto
        # o ultimo arquivo baixado precisa ter "Posição de Cotistas" e não ter
        # a extensão '.crdownload' no final. E também precisa ter sido baixado há menos
        # de 5 segundos atrás
        def atende_condicoes(arquivo):
            tempo_atual = time.time()
            cinco_segundos_atras = tempo_atual - 5
            if os.path.getmtime(arquivo) < cinco_segundos_atras:
                return False
            if "Posição de Cotistas" not in arquivo:
                return False
            if arquivo.endswith(".crdownload"):
                return False
            return True

        def verifica_diretorio_downloads(download_dir):
            while True:
                arquivo_mais_novo = arquivo_mais_recente(download_dir)
                #print(f"arquivo mais recente: {arquivo_mais_novo}")
                if arquivo_mais_novo and atende_condicoes(arquivo_mais_novo):
                    return arquivo_mais_novo
                sleep(1)
                    
        arquivo_45_pos_cot = verifica_diretorio_downloads(self.download_dir)
        return arquivo_45_pos_cot
    

# cliente = '24724'
# fundo = '53779'

# con = Connect()
# folder_cli = cliente
# file_name45 = f"45_cliente{cliente}.txt"
# file_name224 = f"224_cliente{cliente}.txt"

# # Verifica se a pasta para o cliente existe
# cli_folder = os.path.join('clientes', cliente)
# if not os.path.exists(cli_folder):
#     # Se não existir, cria a pasta 'exemplo1'
#     os.mkdir(cli_folder)

# file224 = con.get_224(cliente, fundo, 'psette', 'Ativa!@#001')
# shutil.copy(file224, os.path.join(cli_folder, file_name224))

# file45 = con.get_45(cliente, fundo, 'psette', 'Ativa!@#001')
# shutil.copy(file45, os.path.join(cli_folder, file_name45))
