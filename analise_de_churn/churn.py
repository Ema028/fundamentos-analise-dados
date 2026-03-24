import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("telecon.csv", delimiter=';')

#print(df.head(10))
print(df.info())

missing = df.isnull().sum()
percent = (missing / len(df)) * 100

missing_table = pd.DataFrame({
    'Missing': missing,
    'Percent (%)': percent
}).sort_values(by='Missing', ascending=False)

print(missing_table.head(5))

#excluir linhas churn e genero faltante
#churn é a variável que queremos prever com só 0.2% dos dados faltando, evitar introduzir valor artificial
#genero só 0.48% dos dados faltando exclusão dessas linhas também não compromete o dataset
df = df.dropna(subset=['Churn'])
df = df.dropna(subset=['Genero'])

#variável numérica com 13% dos dados faltando
#substituição pela média para manter a distribuição geral da variável sem perda significativa de dados.
df['Pagamento_Mensal'] = df['Pagamento_Mensal'].fillna(df['Pagamento_Mensal'].mean())

#remover a coluna PhoneService, mais de 59% dos dados faltantes, evitar distorcer os dados
df = df.drop(columns=['PhoneService'])

#genero(4 M, 4 f, 3 F, 1212 Female, 1265 Male) e servico_internet (835 DSL, 7 dsl) precisam de padronização
'''for column in df.select_dtypes(include='object').columns:
    print("\n\n")
    print(df[column].value_counts())'''

df['Genero'] = df['Genero'].replace({
    'M': 'Male',
    'f': 'Female',
    'F': 'Female'
})

df['Servico_Internet'] = df['Servico_Internet'].replace({
    'dsl': 'DSL',
})

df.to_csv("telecon_limpo.csv", index=False)