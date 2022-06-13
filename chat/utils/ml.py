import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords  # Remove useless words
import string
import re

stops = set(stopwords.words('english'))
vectorizer = pickle.load(open("ml/Vectorizer.sav", "rb"))
MNB = pickle.load(open("ml/MNB.sav", "rb"))

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