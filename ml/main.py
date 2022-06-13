import matplotlib.pyplot as plt
import numpy as np
import re 
import pandas as pd
import string
import seaborn as sns

# nltk stuff
import nltk
from nltk.corpus import stopwords  # Remove useless words
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem.lancaster import LancasterStemmer  # Convert words to base form; aggressive
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
# nltk.download("stopwords")
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

## Import packages that help us to create document-term matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# Import tools to split data and evaluate model performance
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import f1_score, precision_score, recall_score, mean_squared_error
# Import ML algos
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.utils import shuffle

# for saving model
import pickle

# Functions and utilities
## lemmatization and remove stopwords
lemmatizer = WordNetLemmatizer()
def lemmatize_and_remove_stopwords(sentence):
  words = nltk.word_tokenize(sentence)
  res_words = []
  for word in words:
    if word in {*stops, *list(string.ascii_lowercase)}:
      continue
    res_words.append(lemmatizer.lemmatize(word)) 
  return " ".join(res_words)

## Text preprocessing steps - remove numbers, capital letters, punctuation, '\n'
## remove all numbers with letters attached to them
remove_alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)

## '[%s]' % re.escape(string.punctuation),' ' - replace punctuation with white space
## .lower() - convert all strings to lowercase 
punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())

## Remove all '\n' in the string and replace it with a space
remove_n = lambda x: re.sub("\n", " ", x)

## Remove all non-ascii characters 
remove_non_ascii = lambda x: re.sub(r'[^\x00-\x7f]',r' ', x)

## Remove redundant spaces 
remove_redundant_spaces = lambda x: re.sub(" +", " ", x)
## Apply all the lambda functions wrote previously through .map on the comments column
def preprocess(x):
  x = remove_alphanumeric(x)
  x = remove_n(x)
  x = remove_non_ascii(x)
  x = punc_lower(x)
  x = remove_redundant_spaces(x)
  x = lemmatize_and_remove_stopwords(x)
  return x


# Pre-processing

## get stopwords
stops = set(stopwords.words('english'))

## get data
data = pd.read_csv('./data/train.csv', delimiter=",")

## replace labels
labelVals = data.iloc[:, 2:]
labelColumns = list(labelVals.columns)
labelColumns

## preprocess text
data['comment_text'] = data['comment_text'].map(preprocess)

## merge toxic classes into one class
data["temp"] = (data[labelColumns] > 0).sum(axis = 1)
data["toxic_class"] = data["temp"] > 0
data["toxic_class"] = data["toxic_class"].astype(int)
data.drop(["temp", *labelColumns], inplace=True, axis=1)


## balancing the dataset
data = shuffle(data)
data_toxic = data[data['toxic_class'] == 1]
data_non_toxic = data[data['toxic_class'] == 0].iloc[:data_toxic.shape[0], :]

data_train = pd.concat([data_toxic, data_non_toxic], axis=0)
data_train = shuffle(data_train)


# Build model

## split data set into X and y
X = data_train["comment_text"]
y = data_train["toxic_class"]
## Split our data into training and test data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# vectorize text to transform them into bag of words
vectorizer = TfidfVectorizer(ngram_range=(2,2), stop_words='english')

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
pickle.dump(vectorizer, open("./Vectorizer.sav", "wb"))



## train the models
MNB = MultinomialNB()
MNB.fit(X_train, y_train)
pickle.dump(MNB, open("./MNB.sav", "wb"))


## test model
X_test = ["Fuck you, and your mommy, and your sister, and your car, every body fuck off"]
X_test_transformed = vectorizer.transform(X_test)

res = MNB.predict(X_test_transformed)

print(res)