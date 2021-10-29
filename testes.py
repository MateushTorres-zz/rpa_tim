import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#opt = Options()
#opt.add_experimental_option("debuggerAddress","localhost:7777")
#driver = webdriver.Chrome(executable_path="C:\\Users\\mateu\\OneDrive\\Documentos\\rpa_tim\\chromedriver.exe",chrome_options=opt)

driver = webdriver.Chrome()

driver.get("https://tanarede.timbrasil.com.br/")


-----

'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
'''
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#opt = Options()
#opt.add_experimental_option("debuggerAddress","localhost:7777")
#driver = webdriver.Chrome(executable_path="C:\\Users\\mateu\\OneDrive\\Documentos\\rpa_tim\\chromedriver.exe",chrome_options=opt)

driver = webdriver.Chrome()


driver.get("https://tanarede.timbrasil.com.br/")
driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div[2]/div/button[2]').click()
time.sleep(13)
driver.find_element(By.ID, "btnSubmit").click()
time.sleep(5)
driver.execute_script("window.scrollBy(0, 800)","")
time.sleep(2)
#driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/ul/li[14]').click()
driver.find_element(By.XPATH, "//*[name()='svg' and @data-icon='laptop']/*[name()='path']").click()
#driver.find_element(By.XPATH, "//*[name()='svg']//*[name()='path']").click()
driver.find_element(By.ID, "s_4_1_0_0_icon").click()
driver.find_element(By.ID, "ui-id-95").click()
driver.find_element(By.CSS_SELECTOR, ".ant-tooltip-open").click()
time.sleep(20)
driver.find_element(By.ID,"tb_-1").click() 

time.sleep(10)



tabela = pd.read_excel("TIM TESTE.xlsx", index_col=0)

for index, row in tabela.iterrows():
    
    driver.find_element(By.NAME, "s_2_1_16_0").click()
    driver.find_element(By.NAME, "s_2_1_16_0").send_keys(str(index))
    driver.find_element(By.ID,"s_2_1_4_0_Ctrl").click() 

    # colocar o resultado 
    plano = 10
    status = 'Ativo'

    tabela.at[index, 'Plano'] = plano
    tabela.at[index, 'Status'] = status
    
    #volta para fazer nova consulta
    # código para voltar

tabela.to_csv('TIM_TESTE.csv')  