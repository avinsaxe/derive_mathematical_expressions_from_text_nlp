import sys
import nltk
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from CosineSimilarity import CosineSimilarity

class SentenceProcessor:

    def __init__(self,sentence,window_size):
        self.sentence=sentence
        self.tags=dict()   #This will store the key as the word in the sentence and the appropriate tag as the value. less_than  is tagged as operator
        self.transformedSentence=None
        self.window=int(window_size)
        self.dictionaryFile='dictionary.txt'
        self.words=[]
        self.dictionary=[]
        self.phrases_k_size=[]
        self.tagged_operands=[]

        self.initializeDictionary()
        self.initializeSentence()
        self.initializePhrasesOfSizeK()
        self.cosineSim=CosineSimilarity()
        # This is a list and will store the transformed sentence made entirely of keys from the tags and relative position as in
        # the original sentence

    def initializeSentence(self):
        if self.sentence!=None:
            self.words=self.sentence.split()   #a list of words
            self.words = [word for word in self.words if word not in stopwords.words('english')]

    def initializeDictionary(self):
        with open(self.dictionaryFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\n")
                splits=splits[0:-1]   #removing the extra '' blank character getting added
                self.dictionary.append(splits)

    def initializePhrasesOfSizeK(self):
        for k in range(0,len(self.words)-self.window+1):  #possible starting points of the string
            phrase=self.words[k:k+int(self.window)]
            self.phrases_k_size.append(phrase)


    #processes a single sentence
    def processSentence(self):
        self.operandTagging()
        self.operatorTagging()

    #TODO Bhavesh
    def operatorTagging(self):
        print "Start the operator tagging"

    #TODO Avinash
    def operandTagging(self):
        print "Start the operand tagging"
        for i in range(len(self.phrases_k_size)):  #k size phrases in a sentence
            phrase=self.phrases_k_size[i]
            self.tagged_operands.append('')
            for dictionaryWordArr in self.dictionary:  #each line can have several similar meaning words
                for dictionaryWord in dictionaryWordArr:
                    word_split=dictionaryWord.split("_")
                    b=self.match(phrase,word_split)
                    if b==True:
                        self.tagged_operands[i]=dictionaryWord
        print "Tagged operator array ",self.tagged_operands


    def match(self,phrases,word_splits):
        text1=str(phrases)
        text2=str(word_splits)
        sim=self.cosineSim.cosine_sim(text1,text2)
        if sim>0.75:
            print phrases, " and ",word_splits,"  matches"
            return True
        print phrases, " and ",word_splits,"  dont match"
        return False





