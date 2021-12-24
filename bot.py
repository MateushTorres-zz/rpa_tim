import time
import csv
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

# import os
# import json
# import io
# import subprocess


def gravar():
    tabela.to_csv(saida)  

def ler_arquivo(arquivo):
    numeros=[]
    
    with open(arquivo) as f:
        csv_reader = csv.DictReader(f, delimiter=',')
    
        for row in csv_reader:
            numeros.append( row)
        
    return numeros

def gravar_arquivo(arquivo, tabela):
    keys = tabela[0].keys()
    with open(arquivo,'w') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(tabela)


print( '--------- iniciando ----------')
GRAVAR_A_CADA = 10
caminho = ''

        
print ('# Lendo config.ini')
# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

GRAVAR_A_CADA = int(config["bot"]["gravar_a_cada"])
caminho = config["bot"]["caminho_webdriver"]
endereco = config["bot"]["endereco"]
arquivo = config["bot"]["arquivo"]
saida = config["bot"]["arquivo_saida"]


print('# Gravar a cada', GRAVAR_A_CADA)
print('# Caminho', caminho)
print('# Endereco', endereco)
print('# Arquivo', arquivo)

print('# Carregando tabela ' + arquivo)
tabela = ler_arquivo(arquivo)
tabela_saida = []

#opt = Options()
#opt.add_experimental_option("debuggerAddress", "localhost:7777")
driver = webdriver.Chrome(executable_path=caminho)

driver.get(endereco)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

print('# Aguardando login.... 30 segs')
time.sleep(30)

driver.get(driver.current_url)
driver.refresh()

wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="TIM_Buttom_Alt_PDV"]'))).click()

time.sleep(10)

print('# Aguardando seleção da mesa.... 10 segs')
driver.find_element(By.ID,"tb_-1").click() 

i = 0

for linha in tabela:
    telefone = linha['NUMERO']
    print("# Número: {}".format(telefone))
    i += 1

    wait.until(EC.visibility_of_element_located((By.NAME, "s_2_1_16_0")))
    driver.find_element(By.NAME, "s_2_1_16_0").click()
    driver.find_element(By.NAME, "s_2_1_16_0").send_keys(str(telefone))
    driver.find_element(By.ID,"s_2_1_4_0_Ctrl").click() 

    tem_alerta= ""
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("# Alerta aceito")
        tem_alerta = "Sim"
    except TimeoutException:
        pass
        
    time.sleep(1)
    plano = ''
    status = ''

    try:
        wait.until(EC.visibility_of_element_located((By.ID,"1TIM_Plano"))).get_attribute("value")
        plano = driver.find_element_by_xpath('//*[@id="1TIM_Plano"]').text
        status =  driver.find_element(By.ID,"1TIM_StatusAcesso").text

    except Exception as e:
        print("# Erro ao localizar plano do número {}".format( telefone))    
        #traceback.print_exc()
        driver.find_element(By.ID,"tb_-1").click() 
        time.sleep(5)
    else:
        print( '# Dados capturados ', telefone, plano, status)

        tabela_saida.append( { 'NUMERO': telefone, 'Plano': plano, 'Status': status, 'Alerta':tem_alerta} )
        
        if i % GRAVAR_A_CADA == 0:
            print('# arquivo gravado.')
            gravar_arquivo(saida, tabela_saida)

        driver.find_element(By.ID,"tb_-1").click() 

print(' --------- Fim da Execucao ----------')

