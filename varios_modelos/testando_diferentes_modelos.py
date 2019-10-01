# -*- coding: utf-8 -*-
"""testando_diferentes_modelos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cmIEbdM3VC49qKDnWDI7vo3N3h-8UmYS

Será que esse modelo de árvore de decisão é nossa melhor escolha? Podemos optar por usar não apenas uma árvore, mas uma floresta inteira, o que geralmente dá melhores resultados. Vamos fazer isso.

Vamos aproveitar e dar uma organizada no nosso código. Primeiro, todos os imports que fizemos no esquenta.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import mean_absolute_error

"""Então carregamos os arquivos de treino e teste."""

dados_treino = pd.read_csv('treino.csv', index_col='Id')
dados_teste = pd.read_csv('teste.csv', index_col='Id')

"""Escolhemos as características."""

caracteristicas = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 
                   'FullBath', 'BedroomAbvGr','TotRmsAbvGrd']

"""Fazemos a copia dos dados."""

X = dados_treino[caracteristicas].copy()
y = dados_treino.SalePrice

"""Dividimos os nossos dados entre treino e validação."""

X_treino, X_valid, y_treino, y_valid = train_test_split(X, y, 
                                                    train_size=0.8, 
                                                    test_size=0.2, 
                                                    random_state=42)

"""Temos o nosso modelo simples de árvore. Vamos fazer um com a floresta agora."""

modelo_1 = tree.DecisionTreeRegressor(random_state=42)

from sklearn.ensemble import RandomForestRegressor

modelo_2 = RandomForestRegressor(random_state=42)

"""Vamos ver como está o erro desses modelos."""

modelo_1.fit(X_treino, y_treino)
preds_1 = modelo_1.predict(X_valid)
mae_1 = mean_absolute_error(y_valid, preds_1)
mae_1

modelo_2.fit(X_treino, y_treino)
preds_2 = modelo_2.predict(X_valid)
mae_2 = mean_absolute_error(y_valid, preds_2)
mae_2

"""Podemos mostrar os erros de uma maneira organizada, e repare que o modelo da floresta, como esperado, tem um erro menor."""

print('MAE do modelo de árvore: %d'% mae_1)
print('MAE do modelo de floresta: %d'% mae_2)

"""Será que esse erro pode ser menor ainda? Como podemos fazer isso? Podemos alterar o que passamos para o nosso modelo e escolhermos um modelo com o menor resultado de erro."""

modelo_3 = RandomForestRegressor(n_estimators=50, random_state=42)
modelo_4 = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_5 = RandomForestRegressor(n_estimators=100, criterion='mae', random_state=42)
modelo_6 = RandomForestRegressor(n_estimators=200, min_samples_split=20, random_state=42)
modelo_7 = RandomForestRegressor(n_estimators=100, max_depth=7, random_state=42)

"""Repare que definimos mais cinco modelo de floresta com parâmetros diferentes, agora para o nosso código ficar menos repetitivos, podemos agrupa-los em uma lista."""

modelos = [modelo_3, modelo_4, modelo_5, modelo_6, modelo_7]

"""Agora, para cada modelo na nossa lista de modelos, podemos fazer o fit, predict e imprimir o mae."""

for i in range(0, len(modelos)):
  modelos[i].fit(X_treino, y_treino)
  preds = modelos[i].predict(X_valid)
  mae = mean_absolute_error(y_valid, preds)
  print('MAE do modelo_%d: %d' % (i+3, mae))

"""Repare que o melhor modelo que temos é o modelo_3"""

melhor_modelo = modelo_3

"""Agora que sabemos qual é um melhor modelo, podemos predizer os resultados com ele e salvá-los.
Para isso, vamos definir X_teste.
"""

X_teste = dados_teste[caracteristicas].copy()

melhor_modelo.fit(X,y)
predicoes_teste = melhor_modelo.predict(X_teste)

"""Vamos montar nosso dicionário e salvá-lo em um arquivo."""

resultados_floresta = {'Id': X_teste.index, 'SalePrice': predicoes_teste}

resultados = pd.DataFrame(resultados_floresta)

resultados.to_csv('resultados_floresta.csv', index=False)