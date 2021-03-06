import sys
import re
import nltk
nltk.download('wordnet')
#from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
nltk.download('averaged_perceptron_tagger')
from CosineSimilarity import CosineSimilarity
from autocorrect import spell
from nltk.corpus import wordnet as wn

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
reserved_words = ['by', 'is','range']


class SentenceProcessor:

    def __init__(self,sentence,window_size):

        self.operands=[]
        self.nouns=[]
        self.sentence=sentence.lower()
        self.autocorrect()
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
        self.cosineSim=CosineSimilarity()
        self.initializeDictionary()
        self.initializeSentence()

        #self.initializePhrasesOfSizeK()
        #self.initializePhrasesOfSize1Operator()

        self.merger=[]

        # This is a list and will store the transformed sentence made entirely of keys from the tags and relative position as in
        # the original sentence
    def autocorrect(self):
        line=''
        for word in self.sentence.split(' '):
	    if word.isdigit():
		line=line+' '+word
	    else:
            	line=line+' '+spell(word)
        self.sentence=line

    def initializeNouns(self):
        self.tokens = nltk.word_tokenize(' '.join(self.words))
        self.tagged = nltk.pos_tag(self.words)
        self.nouns = [word for word,pos in self.tagged \
                      if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        self.nouns = [x.lower() for x in self.nouns]

    #USED
    def initializeDictionary(self):
        with open(self.operandDictionaryFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\n")
                splits=splits[0:-1]   #removing the extra '' blank character getting added
                self.operandDictionary.append(splits)
                self.operands.append(splits[0])

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


    def initializeSentence(self):
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
        print "After merging the parts of sentence together:", self.tokens
        self.processTokens()
        print "After processing of tokens ",self.tokens
        if self.tokens!=None and len(self.tokens)>0 and self.tokens[0]!=None:
            self.expression=' '.join(self.tokens)
        print "The mathematical expression is ",self.expression


    def processTokens(self):
        isRange=False
        isOfType=False  #manages subtraction of, product of, i.e. sum of A and B types
        isOfTypeOp=''  #stores the operator being considered
        prevNoun=''
        for i in range(0,len(self.tokens)):
            token=self.tokens[i]
            if token not in self.operators and token not in reserved_words:
                if isRange: #i.e. we are talking about ranges
                    list=token.split('and')
                    operand1=''
                    operand2=''
                    if len(list)>=2:
                        operand1=list[0].strip()
                        operand2=list[1].strip()

                    if(operand1.isdigit()==True and operand2.isdigit()==True):
                        self.tokens[i-1]='in ['+operand1+','
                        self.tokens[i]=operand2+']'
                        isRange=False
                        continue
                    else:
                        operand1=self.operandMatching(operand1,0.7)
                        operand2=self.operandMatching(operand2,0.7)
                        self.tokens[i-1]=prevNoun.upper()+'{'+operand1+'} - '
                        self.tokens[i]=prevNoun.upper()+'{'+operand2+'}'
                        isRange=False
                        continue
                if isOfType==True:
                    list=token.split('and')
                    operand1=list[0]
                    operand2=list[1]
                    self.tokens[i-1]='('+operand1+' '+isOfTypeOp
                    self.tokens[i]=operand2+')'
                    isOfType=False
                    isOfTypeOp=''
                    continue

                operand=self.operandMatching(token,0.7)
                if operand!='':
                    self.tokens[i]=operand
                    continue
                if token.strip().isdigit():
                    continue
                prevNoun=token  #if everything fails, this means that this has to be a noun
                self.tokens[i]=''
            elif token=='[':
                isRange=True
            elif token=='++' or token=='--' or token=='//' or token=='**':
                isOfType=True
                isOfTypeOp=token[0:-1]
            elif token=='by':
                prevOperatorPos=self.prevOperator()
                if self.tokens[prevOperatorPos]=='>' or self.tokens[prevOperatorPos]=='>=':
                  self.tokens[i]='+'
                  self.tokens[prevOperatorPos]='='
                elif self.tokens[prevOperatorPos]=='<' or self.tokens[prevOperatorPos]=='<=':
                  self.tokens[i]='-'
                  self.tokens[prevOperatorPos]='='

    def prevOperator(self):
        operand=''
        pos=-1
        for i in range(0,len(self.tokens)):
            token=self.tokens[i]
            if token in self.operators:
                operand=token
                pos=i
        return pos

    def convertToSynset(self,phrase):
        list=phrase.strip().split()
        maxSize=10
        mat=[['' for x in range(len(list))] for y in range((maxSize))]

        for col in range(0,len(list)):
            li=wn.synsets(list[col])
            print li
            for row in range(0,maxSize):
                str=''
                if list[col].isdigit():
                    mat[row][col]=list[col]
                elif row<len(li) and col<len(mat[0]) and row<len(mat):
                    str=li[row].name()
                    posOfDot=str.index('.')
                    str=str[:posOfDot]
                    mat[row][col]=str
        # for r in range(0,len(mat)):
        #     for c in range(0,len(mat[0])):
        #         print mat[r][c]+' '
        #     print '\n'
        return mat

    def operandMatching(self,phrase,threshold):
        if len(phrase)<3:
            if len(phrase.strip().split(' '))>0:
                return ('_').join(phrase.strip().split(' '))
            return phrase
        maxMatch=0
        operand=''
        phrases=[[]]
        phrases=self.convertToSynset(phrase)  #2 D matrix of synonyms
        self.maxMatch=0
        self.threshold=0.8
        self.operand=''
        print "The phrases are ",phrases
        for dictionaryWordArr in self.operandDictionary:  #each line can have several similar meaning words
            text1=dictionaryWordArr[0].split('_')
            text1=' '.join(text1)
            text1=text1.lower()
            visited=[[False for x in range(len(phrases[0]))] for y in range((len(phrases)))]
            self.DFS(visited,phrases,0,0,'',text1,dictionaryWordArr[0],phrase)

        return self.operand

        #         phrase=' '.join(phrases[row])
        #         print "Phrase is ",phrase
        #         b=self.match1(phrase,text1)
        #         if b>threshold and b>maxMatch or (text1.lower()==phrase.lower()):
        #             maxMatch=b
        #             operand=dictionaryWordArr[0]
        # if operand!='':
 	    #     return operand
        # phrase=phrase.strip()
        # list=phrase.split(' ')
        # if list[0].isdigit():
        #     return phrase

        #return '_'.join(phrase.strip().split(' '))

    def check(self,phrase,text1,operan,originalStr):
        print "Tried matching ",phrase,text1
        if phrase=='':
            return
        b=self.match1(phrase,text1)
        if b>self.threshold and b>self.maxMatch or (text1.lower()==phrase.lower()):
            self.maxMatch=b
            self.operand=operan
        if self.operand!='':
            return self.operand
        originalStr=originalStr.strip()
        list=originalStr.split(' ')
        if list[0].isdigit():
            self.operand=phrase
            return self.operand
        if phrase!='':
            self.operand='_'.join(phrase.strip().split(' '))

        return self.operand

    def DFS(self,visited,phrases,row,col,phrase,text1,operand,originalStr):
        if len(originalStr)<3:
            return originalStr
        if col==len(visited[0]) and row<len(visited) and phrases!='':
            self.check(phrase,text1,operand,originalStr) #TODO
            return
        if col>=len(visited[0]) or row>=len(visited):
            return
        if visited[row][col]==True:
            return

        visited[row][col]=True
        phrase1=phrase+' '+phrases[row][col]
        self.DFS(visited,phrases,row,col+1,phrase1,text1,operand,originalStr)
        visited[row][col]=False
        self.DFS(visited,phrases,row+1,col,phrase,text1,operand,originalStr) #backtracking


    def match1(self,s1,s2):
        sim=0
        try:
            sim=self.cosineSim.cosine_sim(s1,s2)
        except:
            pass
        #print "similarity between", text1, text2, sim
        return sim




    def match(self,phrases,word_splits):
        if phrases==None or word_splits==None or len(phrases)==0 or len(word_splits)==0:
            return False
        text1=''
        text2=''
        for w1 in phrases:
            if len(w1)!=0 and w1!='[]':
                text1=w1+" "+text1
        for w2 in word_splits:
            if len(w2)!=0 and w2!='[]':
                text2=w2+" "+text2

        try:
            sim=self.cosineSim.cosine_sim(text1.lower(),text2.lower())
        except:
            print text1, text2
            sim=self.cosineSim.cosine_sim(text1.lower(),text2.lower())
            pass
        #print "similarity between", text1, text2, sim
        return sim



    #processes a single sentence
    def processSentence(self):

        #self.operatorTagging()
        self.operandTagging()
        self.merge()

    def initializePhrasesOfSizeK(self):
        for k in range(0,len(self.words)-self.window+1):  #possible starting points of the string
            phrase=self.words[k:k+int(self.window)]
            self.phrases_k_size.append(phrase)

    def initializePhrasesOfSize1perator(self):
        for k in range(0,len(self.words)):  #possible starting points of the string
            phrase=self.words[k:k+1]
            self.phrases_1_size_operator.append(phrase)

    def merge(self):
        self.merger=[]
        prevWasOperator=False
        prevWasOperand=False
        prevOperatorIndex=-1
        prevOperandIndex=-1
        prevLeftOutOperandIndex=-1
        prevLeftOutOperatorIndex=-1
        for i in range(0,len(self.words)):
            operand=self.tagged_operands[i]
            operator=self.tagged_operators[i]
            self.merger.append('')
            if operand=='' and operator=='': #check if any variable name associated, nouns are important
                if self.words[i].lower() in self.nouns:
                    self.merger[i]=self.words[i]

            if operand=='' and operator=='':
                if self.words[i].isdigit():
                    self.merger[i]=self.words[i]

            if operator=='' and operator=='':
                if self.words[i].lower()=='by':
                    if prevOperatorIndex>=0 and  self.merger[prevOperatorIndex]=='>' or self.merger[prevOperatorIndex]=='>=':
                        self.merger[i]='+'
                        self.merger[prevOperatorIndex]='='
                        prevOperatorIndex=i
                    elif prevOperatorIndex>=0 and self.merger[prevOperatorIndex]=='<' or self.merger[prevOperatorIndex]=='<=':
                        self.merger[i]='-'
                        self.merger[prevOperatorIndex]='='
                        prevOperatorIndex=i


            if prevWasOperand==False and prevWasOperator==False:
                if operand!='' and len(operand)>=1:
                    self.merger[i]=operand
                    prevWasOperand=True
                    prevWasOperator=False
                    prevOperandIndex=i

            if prevWasOperand:
                if operator!='' and len(operator)>=1:
                    if prevLeftOutOperandIndex>=0:
                        self.merger[prevLeftOutOperandIndex]=operator
                        self.merger[i]=self.tagged_operands[prevLeftOutOperandIndex]
                        prevWasOperator=False
                        prevWasOperand=True
                        prevOperatorIndex=prevLeftOutOperandIndex
                        prevOperandIndex=i
                        prevLeftOutOperandIndex=-1
                    else:
                        self.merger[i]=operator
                        prevWasOperator=True
                        prevWasOperand=False
                        prevOperatorIndex=i
                if operand!='' and len(operand)>=1 and not (prevOperandIndex>=0 and operand==self.merger[prevOperandIndex]):
                    prevLeftOutOperandIndex=i #this operand has been left out, as we are only looking for operator right now, also check that this should not be a repeating operand
            if prevWasOperator:
                if operand!='' and len(operand)>=1:
                    if prevLeftOutOperatorIndex>=0:
                        self.merger[prevLeftOutOperatorIndex]=operand
                        self.merger[i]=self.tagged_operators[prevLeftOutOperatorIndex]
                        prevWasOperator=True
                        prevWasOperand=False
                        prevOperatorIndex=prevLeftOutOperandIndex
                        prevOperandIndex=i
                        prevLeftOutOperandIndex=-1
                    else:
                        self.merger[i]=operand
                        prevWasOperator=False
                        prevWasOperand=True
                        prevOperandIndex=i
                if operator!='' and len(operator)>=1 and not (prevOperatorIndex>=0 and operator==self.merger[prevOperatorIndex]):
                    prevLeftOutOperatorIndex=i #this operand has been left out, as we are only looking for operator right now, also check that this should not be a repeating operand

        print self.merger #all singly occurring words are nouns, merge all before and after any operator
        self.convertToScietific()
        print self.expression

    def convertToScietific(self):
        self.expression=''
        prevWasOperator=False
        prevWasOperand=False
        prevWasNoun=False
        for i in range(0,len(self.merger)):
            word=self.merger[i]
            if word in self.operands:   #means its an operand
                if prevWasOperand==False:
                    if prevWasNoun==True:
                        self.expression=self.expression+')'
                        prevWasNoun=False
                    self.expression=self.expression+' '+word
                    prevWasOperand=True
                    prevWasOperator=False
            elif word in self.operators:
                if prevWasOperator==False:
                    if prevWasNoun==True:
                        self.expression+=')'
                        prevWasNoun=False
                    self.expression+=' '+word
                    prevWasOperator=True
                    prevWasOperand=False
            elif word.lower() in self.nouns:
                if prevWasNoun==False:  #we can add a bracket and start writing the name
                    self.expression+='('+word.upper()
                    prevWasNoun=True
                elif prevWasNoun==True:
                    self.expression+=' '+word.upper()
                    prevWasNoun=True
            else:
                self.expression+=' '+word
        if prevWasNoun==True:
            self.expression+=')'



    #TODO Avinash
    def operandTagging(self):
        print "Start the operand tagging"
        for i in range(len(self.words)):
            if self.words[i].isdigit():
                self.tagged_operands.append(self.words[i])
            else:
                self.tagged_operands.append('')
        for i in range(len(self.phrases_k_size)):  #k size phrases in a sentence
            phrase=self.phrases_k_size[i]
            phrase=' '.join(phrase)
            threshold=0.9
            maxMatch=0
            for dictionaryWordArr in self.operandDictionary:  #each line can have several similar meaning words
                text1=dictionaryWordArr[0].split('_')
                text1=' '.join(text1)
                b=self.match(phrase,text1)
                if b>threshold and b>maxMatch:
                    maxMatch=b
                    for i1 in range(i,i+self.window):
                        if self.tagged_operands[i1].isdigit()==False:
                            self.tagged_operands[i1]=dictionaryWordArr[0]
                            break
        print "Tagged operand array ",self.tagged_operands
        print self.words

    #TODO Bhavesh. Not used
    def operatorTagging(self):
        print "Start the operator tagging "# plus,add,sum,addition:+
        for i in range(len(self.words)):
            self.tagged_operators.append('')

        for i in range(len(self.phrases_k_size)):
            operatorPhrase=self.phrases_k_size[i][0:-1]  #this will give me the phrase. greater than the
            self.tagged_operators.append('')
            threshold=0.7
            maxMatch=0
            for key in self.operatorMapping: #we want to avoid the last character
                text=" ".join(str(x) for x in operatorPhrase)
                key1=key[0]
                b=self.match(key1,text)
                if b>=threshold and b>maxMatch:
                    maxMatch=b
                    self.tagged_operators[i]=key[-1]
        print "Tagged operator array ",self.tagged_operators
        print self.words



