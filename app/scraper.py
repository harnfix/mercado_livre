# app/scraper.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import sqlite3

def scrape_mercado_livre(search_query):
    driver = webdriver.Chrome(executable_path='caminho_para_seu_chromedriver.exe')
    driver.get(f'https://lista.mercadolivre.com.br/{search_query}')

    # Simular scroll para carregar todos os resultados (opcional)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Aguardar o carregamento

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    items = []
    results = soup.find_all('li', class_='ui-search-layout__item')

    for result in results:
        title = result.find('h2', class_='ui-search-item__title').text.strip()
        price = result.find('span', class_='price-tag-fraction').text.strip()
        link = result.find('a', class_='ui-search-item__group__element')['href']

        items.append({'title': title, 'price': price, 'link': link})

    driver.quit()
    return items

if __name__ == '__main__':
    items = scrape_mercado_livre('chuveiro')
    print(items)
