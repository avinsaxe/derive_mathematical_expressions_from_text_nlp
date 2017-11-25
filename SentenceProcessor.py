import sys
import re
import nltk
nltk.download('wordnet')
#from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from CosineSimilarity import CosineSimilarity

# the only stop words in our sentences
stopwords = ['the', 'a', 'an'] # caution, don't use "A" in the sentence. ex. Vehicle A < Vehicle B

# all these does not help in coverting from natural language to maths, so remove these
replacements = ['should', 'would', 'shall', 'will', 'must', 'might', 'to be', 'could', 'is', 'has', 'have', 'be',
                'should be', 'would be', 'shall be', 'will be', 'must be', 'might be', 'could be']

# first remove those having more length
# e.g. we should first check if "should be" exists or not and then check for "should"
# Nevertheless, this is not required as I have implemented it now. Don't remove to be on safe side
replacements = sorted(replacements, key=lambda x: -len(x))

# currently this is the only word which I could think of that we need to preserve. This will help in converting < or > to =
reserved_words = ['by', 'is']


class SentenceProcessor:

    def __init__(self,sentence,window_size):
        self.sentence=sentence.lower()
        self.tags=dict()   #This will store the key as the word in the sentence and the appropriate tag as the value. less_than  is tagged as operator
        self.transformedSentence=None
        self.window=int(window_size)
        self.operandDictionaryFile= 'operandDictionary.txt'
        self.operatorDictionaryFile='operatorDictionary.txt'
        self.words=[]
        self.operandDictionary=[] 
        self.operatorDictionary=[] # not used anymore, not needed. Make the code which uses this inactive, but don't remove 
        self.operatorMapping=[] # this is a list of tuples e.g. ('plus', '+'), ('add', '+'), ('times', '*')
        self.operators = [] # list of operators that we support
        self.tokens = [] # this is the final list of tokens after processing
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

        #print replacements
        
        print "original:", self.sentence
        # remove articles/stop words
        for _ in stopwords:
            self.sentence = re.sub(" "+_+" ", ' ', self.sentence)
            if (self.sentence.split(' ',1)[0] == _):
                self.sentence = self.sentence.split(' ',1)[1]
        
        print "after removing articles:", self.sentence
        
        # remove "replacements"
        for _ in replacements:
            self.sentence = re.sub(" "+_+" ", ' ', self.sentence)
        self.sentence = re.sub('is is is', 'is', self.sentence)
        self.sentence = re.sub('is is', 'is', self.sentence)

        print "after removing replacements:", self.sentence

        # replace text with actual operators
        for _ in self.operatorMapping:
            self.sentence = re.sub(_[0], " " + _[1] + " ", self.sentence)
        print "after replacing text with operators:", self.sentence

        # change <number><unit> to <number> e.g. 10meters --> 10
        self.sentence = re.sub('(\d+)[^ \d]*', ' \g<1>', self.sentence)
        print "after changing numbers:", self.sentence

        if self.sentence!=None:
            self.words=self.sentence.split()   #a list of words
            print "after splitting the processed sentence:", self.words

        # This is for merging the parts of string 
        # e.g. we have all words in the sentence as a list at this moment.
        # after this step, we will have <part A> <operator> <part B>
        self.tokens = []
        n = len(self.words)
        i = 0
        token = ""
        while i<n:
            if self.words[i] in self.operators or self.words[i] in reserved_words:
                self.tokens.append(token.strip())
                token = ""
                self.tokens.append(self.words[i])
            else:
                token += " "+self.words[i]
            i += 1
        self.tokens.append(token)
        print "After merging the parts of sentence together:", tokens

        # now we need to process the each element of "self.tokens" list
        # for each element:
        #   if it is not an operator and not in reserved word:
        #        if it is "[]":
        #           split the next token on "and". we will get the lower and upper limit which might be numbers or variable names                
        #        else:
        #           use cosine similarity to get the actual variable name from the natural language description
        #           remember, we might not need the window of 3 approach anymore, don't remove it though
        #   else:
        #       keep operators and reserved words as is for future processing, we 
        #       will come back to these once we have the actual variables in the sentence 



    def initializeDictionary(self):
        with open(self.operandDictionaryFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\n")
                splits=splits[0:-1]   #removing the extra '' blank character getting added
                self.operandDictionary.append(splits)

        array = []
        with open(self.operatorDictionaryFile,"r") as ins:
            for line in ins.readlines():
                #print line
                splits=line.split(",")
                self.operators.append(splits[-1][0:-1].strip())
                for _ in splits[0:-1]:
                    array.append((_.strip(), splits[-1][0:-1]))
        #print array
        self.operatorMapping = sorted(array, key=lambda x:-len(x[0]))
        print self.operators
        #print array
        

    def initializePhrasesOfSizeK(self):
        for k in range(0,len(self.words)-self.window+1):  #possible starting points of the string
            phrase=self.words[k:k+int(self.window)]
            self.phrases_k_size.append(phrase)

    def initializePhrasesOfSize1Operator(self):
        for k in range(0,len(self.words)):  #possible starting points of the string
            phrase=self.words[k:k+1]
            self.phrases_1_size_operator.append(phrase)
        # print "?????",self.phrases_1_size_operator


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
                        #print "*********",self.operatorDictionary[j][-1]
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
        #print "similarity between", text1, text2, sim
        if sim>threshold:
            #print phrases, " and ",word_splits,"  matches"
            return True
        #print phrases, " and ",word_splits,"  dont match"
        return False





