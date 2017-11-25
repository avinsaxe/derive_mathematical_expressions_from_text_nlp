import sys
from SentenceProcessor import SentenceProcessor


def main():
    #line = raw_input('Enter a sentence:')
    line = 'The a vehicle speed has to be less an than the vehicle speed.'
    line = 'The speed of the vehicle is more than a displacement of the vehicle'
    line = 'Distance between vehicle and vehicle should be within the range 10m and 70m.'
    #line = 'Speed of vehicle X should be less than Speed of vehicle Y by 10m/sec'
    #print line
    processor=SentenceProcessor(line,3)
    processor.processSentence()


if __name__ == "__main__":
    main()
