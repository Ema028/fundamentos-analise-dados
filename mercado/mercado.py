import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

df = pd.read_csv("mercado.csv", delimiter=',')
df.head(10)

stats_precos = df.groupby('Categoria')['Preco_Normal'].agg(['mean', 'median']).reset_index()

#identificando categorias com média acima ou abaixo da mediana: comidas-preparadas é a única com média abaixo da mediana
stats_precos['Comparacao'] = stats_precos.apply(lambda x: 'média alta' if x['mean'] > x['median'] else 'média baixa', axis=1)
#axis 1 linhas e axis 0 colunas

print("Média e Mediana por Categoria:")
print(stats_precos)

stats_precos['Desvio_Padrao'] = stats_precos['Categoria'].map(df.groupby('Categoria')['Preco_Normal'].std())
print("\n\n\n")
print(stats_precos.sort_values(by='Desvio_Padrao', ascending=False))
#quanto maior o desvio a média  tende a se afastar significativamente da mediana, indica dispersão de valores

#boxplot da categoria com maior desvio
#lacteos tem o maior desvio padrão, tendo a média muito superior à mediana
#a maioria dos produtos possui preços mais perto da mediana, mas outliers aumentam a média
maior_desvio = stats_precos.loc[stats_precos['Desvio_Padrao'].idxmax(), 'Categoria']
plt.figure(figsize=(10, 6))
df_filtro = df[df['Categoria'] == maior_desvio]
sns.boxplot(x='Preco_Normal', data=df_filtro, color='pink')
plt.title(f'Distribuição de Preços: {maior_desvio} (Maior Desvio Padrão)')
plt.xlabel('Preço Normal ($)')
plt.show()

media_descontos = df.groupby('Categoria')['Desconto'].mean().sort_values(ascending=False).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='Categoria', y='Desconto', data=media_descontos, palette='viridis')
plt.title('Média de Descontos Aplicados por Categoria')
plt.ylabel('Desconto Médio')
plt.xlabel('Categoria')
plt.xticks(rotation=45)
plt.show()

df_mapa = df.groupby(['Categoria', 'Marca'])['Desconto'].mean().reset_index()
fig = px.treemap(
    df_mapa, 
    path=['Categoria', 'Marca'], 
    values='Desconto',
    color='Desconto',
    color_continuous_scale='RdYlGn',
    title='Mapa Interativo: Média de Desconto por Categoria e Marca')
fig.show()
