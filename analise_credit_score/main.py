import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

#df = pd.read_csv("credit_score.csv", delimiter=';') income é str, precisa ser float64
df = pd.read_csv('credit_score.csv', sep=';', decimal=',', thousands='.') #lê números "brasileiros" como numeros, income é float
#print(df.head(10))
print(df.info())

missing = df.isnull().sum()
percent = (missing / len(df)) * 100

missing_table = pd.DataFrame({
    'Missing': missing,
    'Percent (%)': percent
}).sort_values(by='Missing', ascending=False)

#print(missing_table)
#único com valores faltando é age, 34 missing -> 20.73%, valor expressivo
#substituição pela mediana para manter a distribuição geral da variável sem perda significativa de dados
#antes foram preenchidos pela média, mas gerou concentração artificial de valores
df['Age'] = df['Age'].fillna(df['Age'].median())

'''for column in df.select_dtypes(include='object').columns:
    print("\n\n")
    print(df[column].value_counts())'''
#já padronizados

print(df.describe())
#income com desvio muito alto, possível outliers
#age com desvio baixo, distribuição bem comportada, mediana muito perto da média
#Number of children com muitos zeros , mediana = 0, possível outliers, distribuição muito concentrada
sns.histplot(df['Income'], bins=30)
plt.title("Distribuição de renda")
plt.show()
#distribuição assimétrica à direita com valores altos menos frequentes

sns.histplot(df['Number of Children'], bins=30)
plt.title("Distribuição de crianças per capita")
plt.show()
#distribuição muito desbalanceada: forte concentração em 0 filhos e poucos casos com 1, 2 ou 3, faz sentido -> não mexer outliers

sns.countplot(x='Credit Score', data=df)
plt.title("Distribuição de pontuação de crédito")
plt.show()
#maioria com crédito alto, perfil de crédito bom

sns.countplot(x='Home Ownership', data=df)
plt.title("Distribuição de posse de imóvel")
plt.show()
#mais pessoas com casa própria, perfil mais estável financeiramente

sns.countplot(x='Education', data=df)
plt.title("Distribuição de escolaridade")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()
#bem distribuído, com leve pico em bacharelado

sns.countplot(x='Marital Status', data=df)
plt.title("Distribuição de estado civil")
plt.show()
#equilíbrio entre solteiros e casados

sns.countplot(x='Gender', data=df)
plt.title("Distribuição de gênero")
plt.show()
#balanceado

#log em vez de IQR pois a renda tem cauda longa, suavizar outliers sem perder informação
df['Income_log'] = np.log(df['Income'])

#clientes com casa própria tendem a ter um score mais alto?
sns.countplot(x='Home Ownership', hue='Credit Score', data=df)
plt.title("Pontuação de crédito por posse de imóvel")
plt.show()
#entre clientes com casa própria grande maioria tem um score alto com poucos casos de score médio
#clientes morando em propriedade alugada se concentram em score médio (principalmente) e baixo, com poucos scores altos

#O salário parece influenciar no Score de Crédito?
sns.boxplot(x='Credit Score', y='Income', data=df)
plt.title("Salário por pontuação de crédito")
plt.xlabel("Credit Score")
plt.ylabel("Income")
plt.show()
#salários de clientes de crédito alto possuem rendas significativamente maiores
#dispersão salarial e valores brutos aumentam progressivamente de high para average para low

#O salário parece influenciar na idade?
sns.scatterplot(data=df, x='Age', y='Income')
plt.title("Relação entre idade e renda")
plt.show()
#tendência positiva, indivíduos mais velhos concentrando maiores salários
#variabilidade dentro das faixas etárias

#Existe relação entre a idade e o status civil?
sns.countplot(x='Marital Status', hue='Age', data=df)
plt.title("Idade por status civil")
plt.show()
#menos casados dentre as categorias mais jovens, concentrados em solteiros
#proporção de casados aumenta nas faixas etárias mais altas

#Qual a relação entre o score de crédito e o nível de escolaridade?
sns.countplot(x='Education', hue='Credit Score', data=df)
plt.title("Pontuação de crédito por escolaridade")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()
#níveis mais altos de escolaridade associados a scores de crédito mais altos
#níveis educacionais mais baixos com maior concentração em scores médios e baixos, sugere uma relação

#qual a relação entre renda e a posse de imóveis?
sns.boxplot(x='Home Ownership', y='Income', data=df)
plt.title("Renda por posse de imóvel")
plt.show()
#clientes com casa própria apresentam rendas mais altas em média
#os que alugam se concentram em faixas de renda mais baixas

#qual a relação entre renda e escolaridade?
sns.boxplot(x='Education', y='Income', data=df)
plt.title("Renda por nível de escolaridade")
plt.xticks(rotation=30, ha='right')
plt.show()
#níveis mais altos de escolaridade associados a maiores rendas medianas
#diploma de ensino médio apresenta a maior dispersão de renda, grande variabilidade, de rendas muito baixas até muito altas
#associate’s Degree se concentra em faixas salariais mais baixas, com menor variabilidade

#qual a relação entre idade e score de crédito?
sns.boxplot(x='Credit Score', y='Age', data=df)
plt.title("Idade por pontuação de crédito")
plt.xlabel("Credit Score")
plt.ylabel("Age")
plt.show()
#clientes com score de crédito mais alto tendem a ser mais velhos em média

sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Matriz de correlação")
plt.show()
#idade e renda possuem alta correlação, faz sentido pela progressão de carreira com a idade

#one-hot encoding: cria colunas binárias para cada categoria, evita falsa ordem hierárquica como em label encoding
cat_cols = df.select_dtypes(include=['str']).columns
df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)
df_encoded.head()

sns.heatmap(df_encoded.corr(), cmap='coolwarm', center=0)
plt.title("Matriz de correlação com variáveis categóricas")
plt.show()
'''Income e Credit Score_High, correlação positiva,renda aumenta, a probabilidade de ter um pontuação de crédito alta também
Marital Status_Single e Home Ownership_Rented, correlação positiva moderada, pessoas solteiras têm uma tendência maior a morar em imóveis alugados
Income e Home Ownership_Rented, correlação negativa considerável, pessoas com rendas maiores têm menos probabilidade de morar em casas alugadas
Age e Marital Status_Single, correlação negativa moderada, idade aumenta, a probabilidade de a pessoa ser solteira diminui'''

#alvo é pontuação de crédito
X = df_encoded.drop(columns=['Credit Score_High'])  # ajuste conforme seu target
y = df_encoded['Credit Score_High']

#base dividida em conjuntos de treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

sns.countplot(x=y_train)
plt.title("Distribuição da pontuação de crédito(treino)")
plt.xlabel("Credit Score Alto")
plt.ylabel("Quantidade")
plt.show()
#desbalanceamento, com muito mais clientes de credit score alto
#pode enviesar o modelo dificultando identificar corretamente clientes com score mais baixo

smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

# Verificar balanceamento
print(y_train.value_counts())
print("\nDepois do SMOTE:\n")
print(y_train_bal.value_counts())