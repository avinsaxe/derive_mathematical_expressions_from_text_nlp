import sys

class SentenceProcessor:

    def __init__(self,sentence,window_size):
        self.sentence=sentence
        self.tags=dict()   #This will store the key as the word in the sentence and the appropriate tag as the value. less_than  is tagged as operator
        self.transformedSentence=None
        self.window=window_size
        print "Initialized"
        # This is a list and will store the transformed sentence made entirely of keys from the tags and relative position as in
        # the original sentence

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

