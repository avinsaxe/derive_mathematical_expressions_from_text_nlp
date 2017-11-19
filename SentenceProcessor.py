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
        self.operandDictionaryFile= 'operandDictionary.txt'
        self.operatorDictionaryFile='operatorDictionary.txt'
        self.words=[]
        self.operandDictionary=[]
        self.operatorDictionary=[]
        self.phrases_k_size=[]
        self.tagged_operands=[]
        self.tagged_operators=[]
        self.phrases_1_size_operator=[]
        self.initializeDictionary()
        self.initializeSentence()
        self.initializePhrasesOfSizeK()
        self.initializePhrasesOfSize1Operator()
        self.cosineSim=CosineSimilarity()
        # This is a list and will store the transformed sentence made entirely of keys from the tags and relative position as in
        # the original sentence

    def initializeSentence(self):
        if self.sentence!=None:
            self.words=self.sentence.split()   #a list of words
            self.words = [word for word in self.words if word not in stopwords.words('english')]
            print self.sentence

    def initializeDictionary(self):
        with open(self.operandDictionaryFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\n")
                splits=splits[0:-1]   #removing the extra '' blank character getting added
                self.operandDictionary.append(splits)

        with open(self.operatorDictionaryFile,"r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split(",")
                arr=splits[0:-2]
                arr.append(splits[-1][0:-1])
                self.operatorDictionary.append(arr)



    def initializePhrasesOfSizeK(self):
        for k in range(0,len(self.words)-self.window+1):  #possible starting points of the string
            phrase=self.words[k:k+int(self.window)]
            self.phrases_k_size.append(phrase)

    def initializePhrasesOfSize1Operator(self):
        for k in range(0,len(self.words)):  #possible starting points of the string
            phrase=self.words[k:k+1]
            self.phrases_1_size_operator.append(phrase)
        print "?????",self.phrases_1_size_operator


    #processes a single sentence
    def processSentence(self):
        self.operandTagging()
        self.operatorTagging()

    #TODO Bhavesh
    def operatorTagging(self):
        print "Start the operator tagging "# plus,add,sum,addition:+
        for i in range(len(self.phrases_1_size_operator)):
            operatorPhrase=self.phrases_1_size_operator[i]  #this will give me the phrase. greater than the
            self.tagged_operators.append('')
            for j in range(len(self.operatorDictionary)):
                for k in range(len(self.operatorDictionary[j])-1): #we want to avoid the last character
                    operatorTag=self.operatorDictionary[j][k]
                    operatorTag += ' cd'
                    text=" ".join(str(x) for x in operatorPhrase)
                    b=self.match(operatorTag,text,0.45)
                    if b==True:
                        print "*********",self.operatorDictionary[j][-1]
                        self.tagged_operators[i]=self.operatorDictionary[j][-1]
                        break
        print "Tagged operator array ",self.tagged_operators

    #TODO Avinash
    def operandTagging(self):
        print "Start the operand tagging"
        for i in range(len(self.phrases_k_size)):  #k size phrases in a sentence
            phrase=self.phrases_k_size[i]
            self.tagged_operands.append('')
            for dictionaryWordArr in self.operandDictionary:  #each line can have several similar meaning words
                for dictionaryWord in dictionaryWordArr:
                    word_split=dictionaryWord.split("_")
                    b=self.match(phrase,word_split,0.75)
                    if b==True:
                        self.tagged_operands[i]=dictionaryWord
        print "Tagged operand array ",self.tagged_operands


    def match(self,phrases,word_splits,threshold):
        if phrases==None or word_splits==None or len(phrases)==0 or len(word_splits)==0:
            return False
        text1=str(phrases)
        text2=str(word_splits)
        try:
            sim=self.cosineSim.cosine_sim(text1,text2)
        except:
            print text1, text2
            sim=self.cosineSim.cosine_sim(text1,text2)
            pass
        print "similarity between", text1, text2, sim
        if sim>threshold:
            print phrases, " and ",word_splits,"  matches"
            return True
        print phrases, " and ",word_splits,"  dont match"
        return False





