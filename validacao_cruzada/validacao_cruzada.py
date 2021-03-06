# -*- coding: utf-8 -*-
"""validacao_cruzada.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tvbsxbHpq2Ydd4AQMG3c0XExP8sMoXVL
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

dados_treino = pd.read_csv('treino.csv', index_col='Id')
dados_teste = pd.read_csv('teste.csv', index_col='Id')

X = dados_treino.copy()
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice
X.drop(['SalePrice'], axis=1, inplace=True)

colunas_numericas = [coluna for coluna in X.columns if X[coluna].dtype in ['int64', 'float64']]

X = X[colunas_numericas]
X_test = dados_teste[colunas_numericas].copy()

pipeline_1 = Pipeline(steps=[
    ('preprocessador', SimpleImputer()),
    ('modelo', RandomForestRegressor(n_estimators=50, random_state=42))
])

from sklearn.model_selection import cross_val_score

maes = cross_val_score(pipeline_1, 
                         X, y,
                         cv=5,
                         scoring='neg_mean_absolute_error')

print("Média do MAE:", maes.mean())

maes = -1 * cross_val_score(pipeline_1, 
                         X, y,
                         cv=5,
                         scoring='neg_mean_absolute_error')

print("Média do MAE:", maes.mean())

"""Podemos usar a validação cruzada também para ter uma idéia de qual o melhor número de árvores na nossa floresta.

Para isso, vamos fazer uma função que itere pelos 50 estimators e plote um gráfico.
"""

def obter_maes(n_estimators):
    pipeline_maes = Pipeline(steps=[
        ('preprocessor', SimpleImputer()),
        ('model', RandomForestRegressor(n_estimators, random_state=0))])
    scores = -1 * cross_val_score(pipeline_maes, 
                                  X, y,
                                  cv=3,
                                  scoring='neg_mean_absolute_error')
    return scores.mean()

resultados = {}
for i in range(1, 9):
  resultados[50*i] = obter_maes(50*i)

resultados

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

plt.plot(resultados.keys(), resultados.values())
plt.show()

melhor_n_estimators = min(resultados, key=resultados.get)

melhor_n_estimators