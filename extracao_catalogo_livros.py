import requests
from bs4 import BeautifulSoup
import pandas as pd
requests.packages.urllib3.disable_warnings()

url = 'https://books.toscrape.com/'
requisicao = requests.get(url)
requisicao.encoding = 'utf-8'

extracao = BeautifulSoup(requisicao.text, 'html.parser')

contar_livros = 0
catalogo = []

for artigo in extracao.find_all('article', class_='product_pod'):
    livro = {}
    titulo = artigo.find('h3').text.strip()
    livro['Título'] = titulo
    preco = artigo.find('p', 
    class_='price_color').text.strip()
    livro['Preço'] = preco
    catalogo.append(livro)
    contar_livros += 1

print('Total livros:', contar_livros)
