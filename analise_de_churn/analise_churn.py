import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px


def main():
    df = pd.read_csv("telecon_limpo.csv")
    print(df.describe())
    '''apenas cerca de 16% de idosos
    Tempo_como_Cliente com grande dispersão, com clientes que acabaram de entrar e outros com até 72 meses de permanência
    25% dos clientes possuem menos de 8 meses de contrato, muitos clientes novos
    pagamento mensal tem uma média próxima da mediana, distribuição relativamente equilibrada
    os valores variam de 18 até 118, diferentes níveis de planos, valor máximo muito superior à média,pode apresentar outliers
    Total_Pago com grande dispersão, o valor máximo muito superior à média, indicativo de outliers'''

    sns.countplot(x='Churn', data=df)
    plt.title("Distribuição de Churn")
    plt.show()
    '''aproximadamente:
    ~1800 clientes não saíram
    ~650 clientes saíram
    maior parte dos clientes permanece na empresa, enquanto uma parcela menor cancela o serviço.'''

    sns.histplot(df['Pagamento_Mensal'], bins=30)
    plt.title("Distribuição do pagamento mensal")
    plt.show()
    '''dois agrupamentos visíveis:
    planos mais baratos(~20)
    planos intermediários/altos(~70)'''

    sns.histplot(df['Tempo_como_Cliente'], bins=30)
    plt.title("Distribuição do tempo como cliente")
    plt.show()
    '''também dois picos visíveis:
    clientes novos(0–5 meses)
    clientes antigos(65–72 meses)'''

    sns.countplot(x='Tipo_Contrato', data=df)
    plt.title("Tipos de contrato")
    plt.xticks(rotation=45)
    plt.show()
    '''contrato mensal tem uma frequência muito maior que os outros tipos de contrato'''

    df['Idoso'] = df['Idoso'].map({0: 'No', 1: 'Yes'})
    for col in df.select_dtypes(include = 'str').columns:
        print("\n")
        print(df[col].value_counts(normalize=True))
    #das booleanas: churn(74%||26%),dependents(68.5%||31.5%) e idoso(83.8%||16.1%) tem um desbalanceamento

    #tratar outliers pagamento_mensal e total_pago
    #achatar os extremos para não enviesar modelos estatísticos, mas não exclui para não perder perfis de clientes
    df = tratar_outliers(df, 'Pagamento_Mensal')
    df = tratar_outliers(df, 'Total_Pago')

    #clientes com menor tempo de contrato cancelam mais?
    sns.boxplot(x='Churn', y='Tempo_como_Cliente', data=df)
    plt.title("Tempo como cliente por Churn")
    plt.xlabel("Churn")
    plt.ylabel("Tempo_como_Cliente")
    plt.show()
    '''clientes que cancelam têm tempo muito menor na empresa
    mediana do tempo de clientes com churn é ~10 meses, clientes que permanecem possuem mediana ~37 meses
    além disso, caixa de Churn = Yes está concentrada em valores baixos'''

    #clientes que pagam mais cancelam mais?
    sns.boxplot(x='Churn', y='Pagamento_Mensal', data=df)
    plt.title("Pagamento mensal por Churn")
    plt.xlabel("Churn")
    plt.ylabel("Pagamento_Mensal")
    plt.show()
    '''clientes com faturas mensais mais altas têm uma tendência maior a cancelar o serviço
    clientes que ficaram: A mediana está próxima de 65
    clientes que sairam: A mediana está próxima de 80
    o grupo de clientes fiéis é mais heterogêneo
    o cancelamento está concentrado em uma faixa mais elevada (~70-95)
    75% dos clientes que cancelaram pagavam mais do que a metade dos clientes que ficaram'''

    #idosos cancelam mais?
    sns.countplot(x='Idoso', hue='Churn', data=df)
    plt.title("Churn por faixa etária (idoso)")
    plt.show()
    '''entre os idosos a taxa dos que cancelam e os que não é similar, 
    enquanto não idosos tem uma taxa de retenção mais alta'''

    #suporte técnico influencia o churn?
    sns.countplot(x='Suporte_Tecnico', hue='Churn', data=df)
    plt.title("Churn por suporte técnico")
    plt.show()
    '''clientes sem suporte técnico possuem uma taxa de cancelamento muito maior,
    indica que esse serviço contribui para aumentar a retenção de clientes'''

    #tipo de contrato influencia o churn?
    sns.countplot(x='Tipo_Contrato', hue='Churn', data=df)
    plt.title("Churn por tipo de contrato")
    plt.xticks(rotation=45)
    plt.show()
    #clientes com contrato mensal possuem uma taxa de cancelamento muito maior

    '''As variáveis que parecem ter maior relação com o churn são:
    Tempo_como_Cliente, Tipo_Contrato, Pagamento_Mensal e Suporte_Tecnico
     porque mostram diferenças claras entre clientes que permanecem e clientes que cancelam'''

def tratar_outliers(df, coluna):
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    df[coluna] = np.where(df[coluna] < limite_inferior, limite_inferior, df[coluna])
    df[coluna] = np.where(df[coluna] > limite_superior, limite_superior, df[coluna])
    return df

main()