import sys
from SentenceProcessor import SentenceProcessor


def main():
    line = raw_input('Enter a sentence:')
    print line
    processor=SentenceProcessor(line,3)

    processor.processSentence()

if __name__ == "__main__":
    main()
