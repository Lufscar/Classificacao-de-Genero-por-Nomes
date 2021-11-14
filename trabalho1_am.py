# -*- coding: utf-8 -*-
"""Trabalho1_AM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yftwuiucE_hRhv_XJRm4MewqZ3BOMa6l

---
<p align="left">
  <big>
    <b>
      <pre>
Camila Manara Ribeiro                - RA: 760465 
Júlia Aparecida Sousa de Oliveira    - RA: 769707 
Luciana Oliveira de Souza Gomes      - RA: 743569
Rafael Vinicius Polato Passador      - RA: 790036 
      </pre>
      <br>
      Disciplina: Aprendizado de Máquina
      <br>
      Professor: Prof. Dr. Diego Furtado Silva
      <br>
    </b>
  </big>
</p>


---

<h1 align="center"><b><big>Projeto de Implementação 01- Classificação de nomes por gênero</big></b></h1>




#**Introdução**

<br>

Neste documento será apresentado o código utilizado para implementação do trabalho proposto: um problema representado por dados estruturados e que possa ser resolvido com algoritmos de AM supervisionado vistos em aula

Dessa forma, para realização desta tarefa, escolheu-se um conjunto de nomes rotuládos como masculinos e femininos que serviu como dataset para classificação de gênero, utilizando, para isso, diversas features que serão abordadas durante o código. 

Assim sendo, serão apresentados os códigos utilizados, bem como as descrições das criações destes. Ademais, apresentam-se, também, as interpretações e documentações da problemática.

Link para a apresentação:

# IMPORT
"""

#Imports de bibliotecas necessárias que foram utilizadas durante a execução do código

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import random
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, accuracy_score
from sklearn.metrics import confusion_matrix

"""# CARREGAR O DATASET

Carregamento do dataset com plot gráfico evidenciando o desbalanceamento entre classes
"""

dataset = pd.read_csv('name_gender_dataset.csv')

dataset.pivot_table(index='Gender', aggfunc='size').plot(kind='bar', title = 'Class distribution')

"""# RANDOM OVERSAMPLING

Como se tratava de um dataset com dados desbalanceados, admitiu-se uma estratégia para contornar esse possível entrave que possibilitaria uma classificação tendenciosa, uma vez que, o número de nomes considerados "femininos" era consideravelmente superior aos masculinos.

Nesse contexto, utiliza-mos uma função de Random OverSampling, em que, aleatoriamente, duplica-se exemplos da classe minoritária (nomes masculinos)
"""

def oversampler(dataset):
    classes = dataset.Gender.value_counts().to_dict()
    maior = max(classes.values())
    classes_lista = []
    for key in classes:
        classes_lista.append(dataset[dataset['Gender'] == key]) 
    classes_exemplo = []
    for i in range(1,len(classes_lista)):
        classes_exemplo.append(classes_lista[i].sample(maior, replace=True))
    dataset_prov = pd.concat(classes_exemplo)
    final_dataset = pd.concat([dataset_prov,classes_lista[0]], axis=0)
    final_dataset = final_dataset.reset_index(drop=True)
    return final_dataset

dataset = oversampler(dataset)

print(dataset)

dataset.head()

dataset.dtypes

M_data = dataset[dataset.Gender == 'M']
F_data = dataset[dataset.Gender == 'F']

print(M_data)
print(F_data)

M_nomes = M_data[M_data.columns[0]].tolist()
F_nomes = F_data[F_data.columns[0]].tolist()

"""Como podemos observar, a distribuição de dados entre as classes está, agora, balanceada"""

dataset.pivot_table(index='Gender', aggfunc='size').plot(kind='bar', title = 'Class distribution')

"""# TREINAMENTO TF-IDF

Nessa seção, apresentaremos o código do treinamento realizado a partir do valor de TF-IDF como feature.
O Tf–idf é uma medida estatística que tem o intuito de indicar a importância de uma palavra de um documento em relação ao dataset, ou seja, calcula-se um valor baseado na sua incidência e admite isso como feature. 

Como classificador, utilizou-se o Naive Bayes.
"""

#Transformando os rótulos 'F' e 'M'
dataset_binario = dataset

dataset_binario.Gender.replace({'F':0,'M':1},inplace=True)

dataset_binario.Gender.unique()

#Vetorizando todos os nomes e extraindo seu valor de TF-IDF como feature, futuramente utilizada pelo Naive Bayes
Xfeatures = dataset_binario['Name']
convertor = TfidfVectorizer()

#Features
X = convertor.fit_transform(Xfeatures)
convertor.get_feature_names()
#Rotulos
y = dataset_binario.Gender

#Separando os dados entre treinamento e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y)

#Classificando o dataset a partir das features com o Naive Bayes
classifier = MultinomialNB()
classifier.fit(X_treino,y_treino)

final_results = classifier.predict(X_teste)
print(final_results)

#Calculando acurácia da amostra
print("Accuracy of Model",classifier.score(X_teste,y_teste)*100,"%")

print("Accuracy of Model",classifier.score(X_treino,y_treino)*100,"%")

print(y_teste)
print(final_results)

#Calculando o F1-Score da amotstra
print("F1: ", f1_score(y_teste, final_results))

conf_matrix = confusion_matrix(y_true=y_teste, y_pred=final_results)
#
# Print the confusion matrix using Matplotlib
#
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

"""# TREINAMENTO COM EXTRAÇÕES DE LETRAS

Nessa seção, apresentaremos o código do treinamento realizado a partir da extração de features gramaticais.
Realizamos a testagem considerando sufixos, prefixos e a combinação de ambos para averiguar qual configuração apresentava melhores resultados e, posteriormente, evidencia-se as features mais relevantes

Como classificador, tambéum utilizou-se o Naive Bayes.
"""

#feature considerando o sufixo
def feature_sufixo(x):
    return {'sufixo1': x[-1:],
            'sufixo2': x[-2:],
            }
feature_sufixo('Josephine')

#feature combinando prefixo e sufixo
def feature_prefixosufixo(x):
    return {'sufixo1': x[-1:],
            'sufixo2': x[-2:],
            'prefixo': x[:2],
            }
feature_prefixosufixo('Josephine')

#feature considerando o prefixo
def feature_prefixo(x):
    return {
            'prefixo': x[0],
            'prefixo2': x[:2],
            }
feature_prefixo('Josephine')

final_dataset = dataset.iloc[:,[0,1]]

dataset_features = final_dataset

print(dataset_features)

M_data2 = dataset_features[dataset_features.Gender == 1]
F_data2 = dataset_features[dataset_features.Gender == 0]


M_nomes2 = M_data2[M_data2.columns[0]].tolist()
F_nomes2 = F_data2[F_data2.columns[0]].tolist()

"""##Treinamento utilizando o prefixo dos nomes como features para o classificador"""

#Treinamento com as features sendo PREFIXO (rodar somente 1 dos blocos)


nomes_rotulados = ([(Name, 1) for Name in M_nomes2] + [(Name, 0) for Name in F_nomes2])
print(nomes_rotulados)
#random.shuffle(nomes_rotulados)

set_features = [(feature_prefixo(n), Gender) for (n, Gender) in nomes_rotulados]
set_treino, set_teste = set_features[50000:], set_features[:50000]
classifier = nltk.NaiveBayesClassifier.train(set_treino)

print(nltk.classify.accuracy(classifier, set_teste))

classifier.show_most_informative_features(15)

#Treinamento com as features sendo PREFIXO (rodar somente 1 dos blocos)

vetor = []
for (name, tag) in nomes_rotulados:
  guess = classifier.classify(feature_prefixo(name))
  vetor.append(guess)
print(vetor)

enumerate(vetor)
for i, item in enumerate(vetor):
    if item == 'F':
        vetor[i] = 0
    elif item == 'M':
        vetor[i] = 1

print(vetor)

lista_generos = [Gender for (n, Gender) in nomes_rotulados]
print(lista_generos)

enumerate(lista_generos)
for i, item in enumerate(lista_generos):
    if item == 'F':
        lista_generos[i] = 0
    elif item == 'M':
        lista_generos[i] = 1

print(lista_generos)

print("F1: ", f1_score(lista_generos, vetor))

conf_matrix = confusion_matrix(y_true=lista_generos, y_pred=vetor)
#
# Print the confusion matrix using Matplotlib
#
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

"""##Treinamento utilizando a combinação prefixo e sufixo dos nomes como features para o classificador"""

#Treinamento com as features sendo PREFIXO+SUFIXO

nomes_rotulados = ([(Name, 1) for Name in M_nomes2] + [(Name, 0) for Name in F_nomes2])
print(nomes_rotulados)
#random.shuffle(nomes_rotulados)

set_features = [(feature_prefixosufixo(n), Gender) for (n, Gender) in nomes_rotulados]
set_treino, set_teste = set_features[500:], set_features[:500]
classifier = nltk.NaiveBayesClassifier.train(set_treino)

print(nltk.classify.accuracy(classifier, set_teste))

classifier.show_most_informative_features(15)

#Treinamento com as features sendo PREFIXO+SUFIXO

vetor = []
for (name, tag) in nomes_rotulados:
  guess = classifier.classify(feature_prefixosufixo(name))
  vetor.append(guess)
print(vetor)

enumerate(vetor)
for i, item in enumerate(vetor):
    if item == 'F':
        vetor[i] = 0
    elif item == 'M':
        vetor[i] = 1

print(vetor)

lista_generos = [Gender for (n, Gender) in nomes_rotulados]
print(lista_generos)

enumerate(lista_generos)
for i, item in enumerate(lista_generos):
    if item == 'F':
        lista_generos[i] = 0
    elif item == 'M':
        lista_generos[i] = 1

print(lista_generos)

print("F1: ", f1_score(lista_generos, vetor))

conf_matrix = confusion_matrix(y_true=lista_generos, y_pred=vetor)
#
# Print the confusion matrix using Matplotlib
#
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

"""##Treinamento utilizando o sufixo dos nomes como features para o classificador"""

#Treinamento com as features sendo SUFIXO


nomes_rotulados = ([(Name, 1) for Name in M_nomes2] + [(Name, 0) for Name in F_nomes2])
print(nomes_rotulados)
#random.shuffle(nomes_rotulados)

set_features = [(feature_sufixo(n), Gender) for (n, Gender) in nomes_rotulados]
set_treino, set_teste = set_features[50000:], set_features[:50000]
classifier = nltk.NaiveBayesClassifier.train(set_treino)

print(nltk.classify.accuracy(classifier, set_teste))

classifier.show_most_informative_features(15)

#Treinamento com as features sendo SUFIXO

vetor = []
for (name, tag) in nomes_rotulados:
  guess = classifier.classify(feature_sufixo(name))
  vetor.append(guess)
print(vetor)

enumerate(vetor)
for i, item in enumerate(vetor):
    if item == 'F':
        vetor[i] = 0
    elif item == 'M':
        vetor[i] = 1

print(vetor)

lista_generos = [Gender for (n, Gender) in nomes_rotulados]
print(lista_generos)

enumerate(lista_generos)
for i, item in enumerate(lista_generos):
    if item == 'F':
        lista_generos[i] = 0
    elif item == 'M':
        lista_generos[i] = 1

print(lista_generos)

print("F1: ", f1_score(lista_generos, vetor))

conf_matrix = confusion_matrix(y_true=lista_generos, y_pred=vetor)
#
# Print the confusion matrix using Matplotlib
#
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()