# Projeto 2 - Como pegar dados de um site com Python? - Pegando dados de ETFs do mundo inteiro.
from IPython.core.display_functions import display
# Desafio:

# - Construir um código que vá no site etf.com e busque dados de todos os etfs do mercado americano e,
# consequentemente, do mundo. Rentabilidades, patrimônio, gestora, taxa...
# - Lembrar de sempre trazer outros tipos de cenários onde a pessoa precisa pegar dados de sites etc.

# Passo a passo:

# Passo 1 - Definir um navegador que você irá utilizar para navegar com o Python.
# O navegador utilizado sera o google Chrome

# Passo 2 - Importar os módulos e bibliotecas.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Passo 3 - Entender como funcionam requisições na internet.

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.etf.com/etfanalytics/etf-finder')

# Passo 4 - Conhecer e mapear o processo de coleta de dados no site do ETF.com.

# Passo 5 - Achar todos os elementos necessários dentro do HTML do site.

time.sleep(5)

botao_100 = driver.find_element("xpath",
                                '/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div['
                                '2]/section[2]/div[1]/div/div[4]/button/label/span')

# botao_100.click()
time.sleep(5)
driver.execute_script("arguments[0].click();", botao_100)

numero_paginas = int(driver.find_element("xpath", '//*[@id="totalPages"]').text.replace("of ", ""))

# Passo 6 - Ler a tabela de dados.

lista_tabela_por_pagina = []

for pagina in range(1, numero_paginas + 1):
    html_tabela = driver.find_element("xpath", '//*[@id="finderTable"]').get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]

    lista_tabela_por_pagina.append(tabela)

    botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')

    # botao_avancar_pagina.click()
    driver.execute_script("arguments[0].click();", botao_avancar_pagina)

tabela_cadastro_etfs = pd.concat(lista_tabela_por_pagina)

formulario_de_voltar_pagina = driver.find_element("xpath", '//*[@id="goToPage"]')

formulario_de_voltar_pagina.clear()
formulario_de_voltar_pagina.send_keys("1")
formulario_de_voltar_pagina.send_keys(u'\ue007')

botao_mudar_pra_performance = driver.find_element("xpath",
                                                  '/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div['
                                                  '2]/section[2]/div[2]/ul/li[2]/span')
botao_mudar_pra_performance.click()

lista_tabela_por_pagina = []
elemento = driver.find_element("xpath", '//*[@id="finderTable"]')

for pagina in range(1, numero_paginas + 1):
    html_tabela = elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]

    lista_tabela_por_pagina.append(tabela)

    botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')

    driver.execute_script("arguments[0].click();", botao_avancar_pagina)

tabela_rentabilidade_etfs = pd.concat(lista_tabela_por_pagina)

driver.quit()
# print(tabela_cadastro_etfs, tabela_rentabilidade_etfs)

# Passo 7 - Construir a tabela final.

tabela_rentabilidade_etfs = tabela_rentabilidade_etfs.set_index("Ticker")
tabela_rentabilidade_etfs = tabela_rentabilidade_etfs[['1 Year', '3 Years', '5 Years']]
tabela_cadastro_etfs = tabela_cadastro_etfs.set_index("Ticker")

base_de_dados_final = tabela_cadastro_etfs.join(tabela_rentabilidade_etfs, how='inner')

# print(base_de_dados_final)
display(base_de_dados_final)
