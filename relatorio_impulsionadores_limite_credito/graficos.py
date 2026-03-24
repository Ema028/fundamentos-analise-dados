import matplotlib.pyplot as plt
import pandas as pd

#o objetivo é identificar quais fatores são os principais impulsionadores
# para aqueles que tem limite de crédito alto
data = {
    'Nome': ['Alice', 'Joao', 'Charlie', 'David', 'Eva', 'Diego', 'Denize', 'Claudio'],
    'Idade': [25, 30, 35, 40, 45, 60, 22, 24],
    'Profissão': ['Engenheiro', 'Médico', 'Professor', 'Advogado', 'Médico','Engenheiro', 'Estudante','Estudante'],
    'Salário': ['4500', '8000', '5000', '10000', '12000','15000', '1200','1500'],
    'Limite_Credito': ['2500', '4000', '4000', '1000', '10000','2000', '500','250'],
    'Historico_Inadimplencia': ['0', '0', '0', '1', '0','1', '0','1'],
    'Estado_Civil': ['Casamento', 'Casamento', 'Solteiro', 'Solteiro', 'Casamento','Solteiro', 'Solteiro','Solteiro'],
    'Imovel_Proprio': ['0', '0', '0', '1', '1','1', '0','0']
}

df = pd.DataFrame(data)
df['Salário'] = pd.to_numeric(df['Salário'], errors='coerce')
df['Limite_Credito'] = pd.to_numeric(df['Limite_Credito'], errors='coerce')
df['Historico_Inadimplencia'] = pd.to_numeric(df['Historico_Inadimplencia'], errors='coerce')
df['Imovel_Proprio'] = pd.to_numeric(df['Imovel_Proprio'], errors='coerce')

#gráfico de dispersão é adequado para analisar a relação entre
#duas variáveis numéricas contínuas, porque ele permite observar a correlação visual
plt.figure(figsize=(10, 6))
plt.scatter(df['Salário'], df['Limite_Credito'], color='blue', alpha=0.5)
plt.title('Relação entre Salário e Limite de Credito')
plt.xlabel('Salário')
plt.ylabel('Limite_Credito')
plt.show()
#indivíduos com salários mais elevados tendem a possuir limites maiores
#salário é um forte impulsionador positivo

plt.figure(figsize=(8,5))
plt.scatter(df['Idade'], df['Limite_Credito'])
plt.title('Relação entre Idade e Limite de Crédito')
plt.xlabel('Idade')
plt.ylabel('Limite')
plt.show()

media_prof = df.groupby('Profissão')['Limite_Credito'].mean()
media_prof.plot(kind='bar')
plt.title('Média de Limite por Profissão')
plt.ylabel('Limite Médio')
plt.show()

#comparar médias de forma direta
df.groupby('Imovel_Proprio')['Limite_Credito'].mean().plot(kind='bar')
plt.title('Média de Limite por Imóvel Próprio')
plt.ylabel('Limite Médio')
plt.show()
#o grupo com imóvel próprio apresenta limites médios superiores,
# isso indica que garantia patrimonial influencia positivamente a concessão de crédito.

df.groupby('Historico_Inadimplencia')['Limite_Credito'].mean().plot(kind='bar')
plt.title('Média de Limite por Historico de Inadimplência')
plt.ylabel('Limite Médio')
plt.show()
#indivíduos com histórico de inadimplência apresentam, em média,
# limites significativamente menores
# inadimplência atua como impulsionador negativo