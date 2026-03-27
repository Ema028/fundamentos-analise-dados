import pandas as pd
import sqlite3

df_vendas = pd.read_csv("vendas.csv", delimiter=';')
conn = sqlite3.connect(':memory:')
df_vendas.to_sql('vendas', conn, index=False, if_exists='replace')

def run_query(query):
    return pd.read_sql_query(query, conn)

#todos os dados
query = "SELECT * FROM vendas;"
print(run_query(query))

#10 linhas coluna produto
query = "SELECT produto FROM vendas LIMIT 10;"
print(run_query(query))

#média valor da unidade e unidades vendidas
query = ("SELECT AVG(VALOR_UNID) AS MEDIA_VALOR_UNID,"
         "AVG(UNIDADES) AS MEDIA_UNID_POR_VENDA FROM vendas;")
print(run_query(query))

#não temos valor total por compra, mas tem quantidade vendida e valor do produto
#retornar id compra, id cliente e total gasto
query = ("SELECT ID_COMPRA, ID_CLIENTE, "
         "(VALOR_UNID * UNIDADES) AS VALOR_TOTAL_GASTO FROM vendas;")
print(run_query(query))

#nomes dos produtos distintos que temos na base de venda
query = "SELECT DISTINCT(produto) FROM vendas;"
print(run_query(query))

#contagem dos clientes distintos que temos na nossa base
query = "SELECT count(DISTINCT(ID_CLIENTE)) as N_CLIENTES FROM vendas;"
print(run_query(query))

#coluna com os produtos distintos e o valor_unid de cada, apenas para produtos com valor_unid maior ou igual a 50 reais
query = ("SELECT DISTINCT(produto), VALOR_UNID "
         "FROM vendas WHERE(VALOR_UNID >= 50);")
print(run_query(query))

#produtos e a média do preço da unidade dos produtos, ordenando do maior para o menor
query = ("SELECT produto, "
         "AVG(valor_unid) AS media_preco FROM vendas"
         " GROUP BY produto ORDER BY media_preco DESC;")
print(run_query(query))

#id dos 3 clientes da base de vendas que mais relalizaram compras e a quantidade de compras realizadas
query = ("SELECT ID_CLIENTE, "
         "COUNT(ID_COMPRA) AS quantidade_compras "
         "FROM vendas GROUP BY ID_CLIENTE ORDER BY quantidade_compras DESC LIMIT 3;")
print(run_query(query))