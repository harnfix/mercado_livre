# appl.py
from flask import Flask, render_template, request, redirect, url_for
from database import criar_tabela, salvar_produtos, listar_produtos, remover_produto

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def buscar_produtos_palavra_chave(palavra_chave, quantidade):
    chrome_driver_path = 'C:\\Users\\chromedriver-win64\\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    try:
        url_base = 'https://lista.mercadolivre.com.br/'
        url = url_base + palavra_chave
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-search-result')))

        produtos = driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')
        resultados = []
        precos = []

        for produto in produtos[:quantidade]:
            nome = produto.find_element(By.CSS_SELECTOR, '.ui-search-item__title').text
            preco = produto.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction').text.replace('.', '')
            link = produto.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            imagem = produto.find_element(By.CSS_SELECTOR, '.ui-search-result-image__element').get_attribute('src')
            
            # Tentativa inicial de encontrar o vendedor
            vendedor_element = produto.find_elements(By.CSS_SELECTOR, '.ui-search-official-store-label')
            vendedor = vendedor_element[0].text if vendedor_element else None
            
            # Alternativa para encontrar o vendedor através da div com classe 'ui-seller-data-header__title-container'
            if not vendedor:
                vendedor_container = produto.find_elements(By.CSS_SELECTOR, '.ui-seller-data-header__title-container')
                if vendedor_container:
                    vendedor = vendedor_container[0].find_element(By.TAG_NAME, 'span').text
                else:
                    vendedor = 'N/A'

            parcelas = produto.find_element(By.CSS_SELECTOR, '.ui-search-item__group__element.ui-search-installments').text if produto.find_elements(By.CSS_SELECTOR, '.ui-search-item__group__element.ui-search-installments') else 'N/A'
            avaliacao = produto.find_element(By.CSS_SELECTOR, '.ui-search-reviews__ratings').get_attribute('aria-label') if produto.find_elements(By.CSS_SELECTOR, '.ui-search-reviews__ratings') else 'N/A'
            quantidade_avaliacoes = produto.find_element(By.CSS_SELECTOR, '.ui-search-reviews__amount').text if produto.find_elements(By.CSS_SELECTOR, '.ui-search-reviews__amount') else '0'
            cupons_desconto = produto.find_element(By.CSS_SELECTOR, '.ui-search-item__highlight-label__text').text if produto.find_elements(By.CSS_SELECTOR, '.ui-search-item__highlight-label__text') else ''

            resultados.append({
                'nome': nome,
                'preco': preco,
                'link': link,
                'imagem': imagem,
                'vendedor': vendedor,
                'parcelas': parcelas,
                'avaliacao': avaliacao,
                'quantidade_avaliacoes': quantidade_avaliacoes,
                'cupons_desconto': cupons_desconto
            })
            precos.append(int(preco))

        salvar_produtos(resultados)  # Salva apenas os produtos até a quantidade desejada

        media_precos = sum(precos) / len(precos) if precos else 0

        return resultados, media_precos

    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        quantidade = int(request.form.get('quantidade', 3))  # Valor padrão de 3 se não especificado
        resultados, media_precos = buscar_produtos_palavra_chave(search_term, quantidade)
        return render_template('index.html', resultados=resultados, search_term=search_term, media_precos=media_precos)
    return render_template('index.html')

@app.route('/produtos', methods=['GET'])
def lista_produtos():
    produtos_salvos = listar_produtos()
    return render_template('produtos.html', produtos_salvos=produtos_salvos)

@app.route('/remover_produto/<int:produto_id>', methods=['POST'])
def remover_produto_route(produto_id):
    remover_produto(produto_id)
    return redirect(url_for('lista_produtos'))

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
