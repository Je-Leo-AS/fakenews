# -*- coding: utf-8 -*-
"""Fake News BigPET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-VO36YFQpbndQaLw85y5f7juVyig9AQb
"""

from webbrowser import get
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

#nltk.download('wordnet')
#nltk.download('punkt')
#
import os


#Notícias Verdadeiras Drive PET
X = []
y = []

N = 3600 # Número de notícias coletadas do banco de "notícias genuínas"

i = 0

while i < N:
    j = i + 1 
    try:
        file = open("/dataset/true/"+str(j)+".txt")
        # Os arquivos contidos na pasta apresentam como identidade um número mais a extensão .txt
        X.append(file.readlines())
        y.append(True)
        file.close()
    except:
        print('Erro na leitura ou ausência do arquivo: ', j)
        # Sequencialmente, cada arquivos será checado, um a um
        X.append([None])
        y.append([None])
    i += 1

news = pd.DataFrame(data = list(zip(X, y)), columns = ['Conteúdo', 'Veredicto'])
news.index = np.arange(len(news))     
print('Validação completa')

#Notícias Verdadeiras Drive Leonardo
X = []
y = []

N = 3600 # Número de notícias coletadas do banco de "notícias genuínas"

i = 0

while i < N:
    j = i + 1 
    try:
        file = open("/dataset/true/"+str(j)+".txt")
        # Os arquivos contidos na pasta apresentam como identidade um número mais a extensão .txt
        X.append(file.readlines())
        y.append(True)
        file.close()
    except:
        print('Erro na leitura ou ausência do arquivo: ', j)
        # Sequencialmente, cada arquivos será checado, um a um
        X.append([None])
        y.append([None])
    i += 1

news = pd.DataFrame(data = list(zip(X, y)), columns = ['Conteúdo', 'Veredicto'])
news.index = np.arange(len(news))     
print('Validação completa')

#Tratando os Dados
#Subsituição de caracteres invalidos das noticias verdadeiras 
news_np = pd.DataFrame.to_numpy(news['Conteúdo'])
lista = []
for i in range(len(news_np)):
  lista.append(news_np[i])
  if lista[i][0] != None:
    lista[i][0] = lista[i][0].replace('\n', '') #Removendo/alterando caracteres
    lista[i][0] = lista[i][0].replace('é', 'e')
    lista[i][0] = lista[i][0].replace('ê', 'e')
    lista[i][0] = lista[i][0].replace('á', 'a')
    lista[i][0] = lista[i][0].replace('â', 'a')
    lista[i][0] = lista[i][0].replace('à', 'a')
    lista[i][0] = lista[i][0].replace('ã', 'a')
    lista[i][0] = lista[i][0].replace('õ', 'o')
    lista[i][0] = lista[i][0].replace('ó', 'o')
    lista[i][0] = lista[i][0].replace('ô', 'o')
    lista[i][0] = lista[i][0].replace('ú', 'u')
    lista[i][0] = lista[i][0].replace('í', 'i')
    lista[i][0] = lista[i][0].replace('ç', 'c')
  lista[i] = lista[i][0]
news['Conteúdo'] = lista

# Dataset de notícias verdadeiras

news.head(10)

#Notícias Falsas
X = []
y = []

N = 3600  # Número de notícias coletadas do banco de "notícias falsas"
i = 0
while i < N:
    try:
        file = open("/dataset/fake/"+str(i+1)+".txt")
        # Os arquivos contidos na pasta apresentam como identidade um número mais a extensão .txt
        X.append(file.readlines())
        y.append(False)
        file.close()
    except:
        print('Erro na leitura ou ausência do arquivo: ', i)
        # Sequencialmente, cada arquivos será checado, um a um
        X.append([None])
        y.append([None])
    i += 1
fakenews = pd.DataFrame(data = list(zip(X, y)), columns = ['Conteúdo', 'Veredicto'])
fakenews.index = np.arange(len(fakenews)) + len(news)
print('Validação completa')

#Tratando os Dados
#Subsituição de caracteres invalidos das noticias falsas
news_np = pd.DataFrame.to_numpy(fakenews['Conteúdo'])
lista = []
for i in range(len(news_np)):
  lista.append(news_np[i])
  if lista[i][0] != None:
    lista[i][0] = lista[i][0].replace('\n', '') #Removendo/alterando caracteres
    lista[i][0] = lista[i][0].replace('é', 'e')
    lista[i][0] = lista[i][0].replace('ê', 'e')
    lista[i][0] = lista[i][0].replace('á', 'a')
    lista[i][0] = lista[i][0].replace('â', 'a')
    lista[i][0] = lista[i][0].replace('à', 'a')
    lista[i][0] = lista[i][0].replace('ã', 'a')
    lista[i][0] = lista[i][0].replace('õ', 'o')
    lista[i][0] = lista[i][0].replace('ó', 'o')
    lista[i][0] = lista[i][0].replace('ô', 'o')
    lista[i][0] = lista[i][0].replace('ú', 'u')
    lista[i][0] = lista[i][0].replace('í', 'i')
    lista[i][0] = lista[i][0].replace('ç', 'c') 
  lista[i] = lista[i][0]
fakenews['Conteúdo'] = lista

# Dataset de notícias falsas
fakenews.head(10)

# Removendo os poucos valores inválidos
news = news.dropna() 
fakenews = fakenews.dropna()


# Unindo conjunto fakenews e news
df = pd.concat([news, fakenews], ignore_index = True) 
df.index = np.arange(len(df))

# Importando palavras mais comuns do Português

file = open('stopwords.txt')
stopwords = file.readlines()
for i in range(len(stopwords)):
  stopwords[i] = stopwords[i].replace(' ', '')
  stopwords[i] = stopwords[i].replace('\n', '')
  stopwords[i] = stopwords[i].replace('é', 'e')
  stopwords[i] = stopwords[i].replace('ê', 'e')
  stopwords[i] = stopwords[i].replace('á', 'a')
  stopwords[i] = stopwords[i].replace('â', 'a')
  stopwords[i] = stopwords[i].replace('à', 'a')
  stopwords[i] = stopwords[i].replace('ã', 'a')
  stopwords[i] = stopwords[i].replace('õ', 'o')
  stopwords[i] = stopwords[i].replace('ô', 'o')
  stopwords[i] = stopwords[i].replace('ó', 'o')
  stopwords[i] = stopwords[i].replace('ú', 'u')
  stopwords[i] = stopwords[i].replace('í', 'i')
  stopwords[i] = stopwords[i].replace('ç', 'c') 
file.close()

stopwords = stopwords[:50]

#definindo função que remove as stopwords do texto
stop = stopwords
def remove_stopwords(text):
    final_text = []
    text = text.lower()
    for i in text.split():
        if i.strip() not in stop:
            final_text.append(i.strip())
    return " ".join(final_text)

#aplicaando a função remove_stopwords
df['Conteúdo']=df['Conteúdo'].apply(remove_stopwords)

#lemmatization
# Inicia Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()

#A função remove as terminações flexionais e retorna a forma base da palavra que é conhecida como lema.
def lemmatize_text(text):
    token_words=word_tokenize(text) 
    lemma_sentence=[]
    for word in token_words:
        lemma_sentence.append(lemmatizer.lemmatize(word))
        lemma_sentence.append(" ")
    return "".join(lemma_sentence)

#aplicando a função a coluna conteudo
df['Conteúdo']=df['Conteúdo'].apply(lemmatize_text)


#criando word cloud para as fake news
cloud = WordCloud(max_words = 500, stopwords = STOPWORDS, background_color = "white").generate(" ".join(df[df.Veredicto == True].Conteúdo))
plt.figure(figsize=(10, 10))
plt.imshow(cloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

cloud = WordCloud(max_words = 500, stopwords = STOPWORDS, background_color = "white").generate(" ".join(df[df.Veredicto == False].Conteúdo))
plt.figure(figsize=(10, 10))
plt.imshow(cloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

#achando os  n-grams
texts = ''.join(str(df['Conteúdo'].tolist()))

# pega as palavras individualmente 
tokenized = texts.split()

#unigram
unigram = (pd.Series(nltk.ngrams(tokenized, 1)).value_counts())[:20]
unigram.sort_values().plot.barh(width=.9, figsize=(12, 8))
plt.title('20 Bigramas mais frequentemente ocorridos')
plt.ylabel('Unigrama')
plt.xlabel('# de Ocorrencias')

#bigrams
bigram = (pd.Series(nltk.ngrams(tokenized, 2)).value_counts())[:20]
bigram.sort_values().plot.barh(width=.9, figsize=(12, 8))
plt.title('20 Bigramas mais frequentemente ocorridos')
plt.ylabel('Bigrama')
plt.xlabel('# de Ocorrências')

#modelando 
def get_prediction(vectorizer, classifier, X_train, X_test, y_train, y_test):
    pipe = Pipeline([('vector', vectorizer),
                    ('model', classifier)])
    model = pipe.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuarcy: {}".format(round(accuracy_score(y_test, y_pred)*100,2)))
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix: \n", cm)
    return model

#implementando pipeline 
Conteudo = df['Conteúdo']
Conteudo = Conteudo.astype(str)

Veredicto = df['Veredicto']
Veredicto = Veredicto.astype(bool)

X_train, X_test, y_train, y_test = train_test_split(Conteudo, Veredicto, test_size = 0.3, random_state= 0)
classifiers = [LogisticRegression(),KNeighborsClassifier(n_neighbors=5), DecisionTreeClassifier(), GradientBoostingClassifier(),RandomForestClassifier()]

def remove_stopwords(text):
    final_text = []
    text = text.lower()
    for i in text.split():
        if i.strip() not in stop:
            final_text.append(i.strip())
    return " ".join(final_text)

def prediction(X_predict, model):
    X_predict=X_predict.apply(remove_stopwords)
    y_pred = model.predict(X_predict)
    print(f'Veredictor: {y_pred}')
    return y_pred

