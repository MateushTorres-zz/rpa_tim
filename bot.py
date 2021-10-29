'''
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
'''
import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException


opt = Options()
opt.add_experimental_option("debuggerAddress", "localhost:7777")
driver = webdriver.Chrome(executable_path="C:\\Users\\mateu\\OneDrive\\Documentos\\rpa_tim\\chromedriver.exe", chrome_options=opt)
driver.get("https://siebelcrm.timbrasil.com.br/mobile_ptb/start.swe?SWECmd=GotoView&SWEView=TIM+Vendas+21+-+Change+Position+View&SWERF=1&SWEHo=siebelcrm.timbrasil.com.br&SWEBU=1&SWEApplet0=TIM+Vendas+21+-+GFA+Change+Position+Form+Applet&SWERowId0=VRId-0")
driver.maximize_window()
wait = WebDriverWait(driver, 10)

time.sleep(15)

driver.get(driver.current_url)
driver.refresh()

wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="TIM_Buttom_Alt_PDV"]'))).click()

time.sleep(10)

driver.find_element(By.ID,"tb_-1").click() 

tabela = pd.read_excel("TIM TESTE.xlsx", index_col=0)


for index, row in tabela.iterrows():
    wait.until(EC.visibility_of_element_located((By.NAME, "s_2_1_16_0")))
    driver.find_element(By.NAME, "s_2_1_16_0").click()
    driver.find_element(By.NAME, "s_2_1_16_0").send_keys(str(index))
    driver.find_element(By.ID,"s_2_1_4_0_Ctrl").click() 

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("Alerta aceito")
    except TimeoutException:
        print("")
        
    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.ID,"1TIM_Plano"))).get_attribute("value")
    plano = driver.find_element_by_xpath('//*[@id="1TIM_Plano"]').text
    status =  driver.find_element(By.ID,"1TIM_StatusAcesso").text

    print( plano, status)

    tabela.at[index, 'Plano'] = plano
    tabela.at[index, 'Status'] = status
    
    driver.find_element(By.ID,"tb_-1").click() 

tabela.to_csv('TIM_TESTE.csv')  
