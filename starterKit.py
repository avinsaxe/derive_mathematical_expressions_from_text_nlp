import sys
from SentenceProcessor import SentenceProcessor


def main():

    while True:
        print "Input -1 to exit"
        line = raw_input('Enter a sentence:')
        #line = 'The a vehicle speed has to be less an than the vehicle speed.'
        #line = 'The speed of the vehicle is more than displacement of the vehicle'
        #line = 'Distance between vehicle X and vehicle Y should be within the range 10m and 70m.'
        #line = 'The speed of vehicle X plus speed of vehicle Y is equal to2 times displacement of vehicle'
        #line = 'Speed of vehicle X should be less than Speed of vehicle Y by 10m/sec'
        #print line
        #line = 'The product of 2 and 178'
        #line = 'The sum of vehicle speed and vehicle displacement'
        #line = 'The sum of vehicle speed and product of distance of vehicle and vehicle speed'
        #line = 'The sum of X and C multiply D divide E'
        #Speed of vehicle X should be less than equal to Speed of vehicle Y by 10m/sec
        #Speed of vehicle X should be greater than equal to Speed of vehicle Y by 10m/sec
        #Speed of vehicle X should be greater than Speed of vehicle Y by 10m/sec
        #Age of Avinash is more than Age of Guds by 5 years
        #vehicle speed is 2 times as fast as truck speed
        #truck acceleration is 2 times more than vehicle_acceleration  --Not working

        if line=="-1":
            break;
        processor=SentenceProcessor(line,3)


if __name__ == "__main__":
    main()
