import os
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt') # if necessary...


class CosineSimilarity:
    def normalize(self,text):
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))

    def __init__(self):
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')

    def cosine_sim(self,text1, text2):
        tfidf = self.vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]

    def stem_tokens(self,tokens):
        return [self.stemmer.stem(item) for item in tokens]





'''remove punctuation, lowercase, stem'''




