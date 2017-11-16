import sys

class SentenceProcessor:
    def __init__(self,sentence):
        self.sentence=sentence
        self.tags=dict()   #This will store the key as the word in the sentence and the appropriate tag as the value. less_than  is tagged as operator
        self.transformedSentence=None
        # This is a list and will store the transformed sentence made entirely of keys from the tags and relative position as in
        # the original sentence

    #processes a single sentence
    def processSentence(self,sentence):
        self.operandTagging()
        self.operatorTagging()

    #TODO Bhavesh
    def operatorTagging(self,sentence):
        print "Start the operator tagging"

    #TODO Avinash
    def operandTagging(self,sentence):
        print "Start the operand tagging"