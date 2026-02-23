import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('ecommerce.csv')

#histograma
plt.figure(figsize=(8,5))
plt.hist(df['Preço'], bins=20)
plt.title('Distribuição dos Preços dos Produtos')
plt.xlabel('Preço')
plt.ylabel('Frequência')
plt.show()

#gráfico de dispersão
plt.figure(figsize=(10, 6))
plt.scatter(df['Nota'], df['Desconto'], color='blue', alpha=0.5)
plt.title('Relação entre Nota e Desconto')
plt.xlabel('Nota')
plt.ylabel('Desconto')
plt.show()

#mapa de calor
cols_importantes = ['Nota', 'N_Avaliações', 'Desconto', 'Preço']
plt.figure(figsize=(8,6))
sns.heatmap(df[cols_importantes].corr(), annot=True, cmap='coolwarm')
plt.title('Correlação entre Nota, Número de Avaliações, Desconto e Preço')
plt.show()

#gráfico de barras
top_marcas = df['Marca'].value_counts().head(10)
plt.figure(figsize=(10,6))
top_marcas.plot(kind='bar')
plt.title('Top 10 Marcas com Mais Produtos')
plt.xlabel('Marca')
plt.ylabel('Quantidade de Produtos')
plt.show()

#gráfico de pizza
generos_principais = df['Gênero'].value_counts().nlargest(7).index

#agrupar categorias com baixa expressão em Outros
df['Gênero_Ajustado'] = df['Gênero'].apply(lambda x: x if x in generos_principais else 'Outros')
genero_counts = df['Gênero_Ajustado'].value_counts()
plt.figure(figsize=(7,7))
plt.pie(genero_counts, labels=genero_counts.index, autopct='%1.1f%%')
plt.title('Distribuição de Produtos por Gênero')
plt.show()

#gráfico de densidade
plt.figure(figsize=(8,5))
sns.kdeplot(df['Nota'], fill=True)
plt.title('Densidade das Notas dos Produtos')
plt.xlabel('Nota')
plt.ylabel('Densidade')
plt.show()

#gráfico de regressão
plt.figure(figsize=(8,5))
sns.regplot(x='Preço', y='Desconto', data=df)
plt.title('Regressão entre Preço e Desconto')
plt.xlabel('Preço')
plt.ylabel('Desconto')
plt.show()
