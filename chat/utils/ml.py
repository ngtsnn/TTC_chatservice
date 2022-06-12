import pickle

vectorizer = pickle.load(open("../ml/Vectorizer.sav", "rb"))
MNB = pickle.load(open("../ml/MNB.sav", "rb"))