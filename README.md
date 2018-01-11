### Extracting Mathematical Expressions from Text

#### How to run

```python starterkit.py```

Input your mathematical sentence, and let the code run for it to give you a possible mathematical representation quickly.

#### Introduction

The project titled ‘Automatic Mathematical Expression Extraction from Text Using NLP Based Approaches’ works on generating mathematical expressions from text, by applying Natural Language based approaches. The project aims to identify mathematical expressions from a domain of text available from Mechanical Engineering department lab. The kind of content that mechanical engineering department is handling, is associated with identification of a limited set of mathematical expressions.


#### About

The entire project is implemented in Python, for utilizing the enormous utilities in Natural Language domain. To execute the code, directly run the main code, after downloading required libraries.  As the project is for mechanical engineering department, and his entire focus is on speed and not on reinventing the wheel, we chose to move ahead with existing cosine similarity rule. 


#### Approach

##### Step 1: Preprocess the input data
The identification of the operators is done utilizing regular expression matching based approach. The approach we used was to create a dictionary of all the entries of all the possible text that could mean an operator in mathematics. 
For example, in the dictionary of operators, greater than or equal to, greater than equal to, can map to ‘≥’. In addition to that, the text data, sum of, addition, add, plus, etc. maps to the operator ‘+’.
For identification of operators, we first developed a window based approach, where we analyzed all the possible substrings of length in the original string input. We used cosine similarity rule to match all the possible operators with the text, using cosine similarity rule. 
The identification was optimal, but we were struggling to cope up with step 3 of the algorithm, i.e. identify the exact position of the operators in the window. As the length of the window could vary from 2 to 5, the fixed window size approach was not going to be useful. For e.g. “the speed of the vehicle” (size 5), “speed of vehicle” (size 3), “vehicle speed” (size 2). Operands could overlap these windows, identifying whether operator or operand comes first in that specific window became very tough.
We later came up with the idea of identifying operators in-place in the input string, and replacing all the matching words in the window, with the exact operator, hence reducing the total size of string to be considered for the approach.
This approach helped significantly, as now relative positions were automatically correct, and operators were placed in almost correct relative positions.


##### Step 2: Identify the operators

The identification of the operators is done utilizing regular expression matching based approach. The approach we used was to create a dictionary of all the entries of all the possible text that could mean an operator in mathematics. 
For example, in the dictionary of operators, greater than or equal to, greater than equal to, can map to ‘≥’. In addition to that, the text data, sum of, addition, add, plus, etc. maps to the operator ‘+’.
For identification of operators, we first developed a window based approach, where we analyzed all the possible substrings of length in the original string input. We used cosine similarity rule to match all the possible operators with the text, using cosine similarity rule. 
The identification was optimal, but we were struggling to cope up with step 3 of the algorithm, i.e. identify the exact position of the operators in the window. As the length of the window could vary from 2 to 5, the fixed window size approach was not going to be useful. For e.g. “the speed of the vehicle” (size 5), “speed of vehicle” (size 3), “vehicle speed” (size 2). Operands could overlap these windows, identifying whether operator or operand comes first in that specific window became very tough.
We later came up with the idea of identifying operators in-place in the input string, and replacing all the matching words in the window, with the exact operator, hence reducing the total size of string to be considered for the approach.
This approach helped significantly, as now relative positions were automatically correct, and operators were placed in almost correct relative positions.


##### Step 3: Identify the operands

The operands are varied, and can take various forms that are beyond the scope of pattern matching and regular expression matching. Thus, regular expression based matching will not work for identifying the operands.
Instead, we used the window of size k, approach to identify operands. After completing step 3.2.1, we would be left with string of the following form:
<text><operator><text><operator><text>

As operator and their relative positions are already know, we act upon the text to identify the operands.
For identification of operands, We created a dictionary of various possible operands in context of the mechanical engineering lab.

The list contains possible operands in the form of text1_text2, i.e. an ‘_’ separated text data, representing an operand.
For example, vehicle_speed is an operand, made from the words vehicle and speed, and separated by an ‘_’.
For each window of ‘k’ size, we traverse through all the possible operands in the list, and break the operands on the ‘_’, to form another string. We then match both the substring obtained from the window, and the operand obtained after splitting on the ‘_’, and match both the strings for their similarity. We defined a threshold of 0.9 for similarity, below which, the two strings won’t be considered similar, and above which they will be considered similar. We chose the operand that has the maximum matching coefficient amongst the entire list, as the most probable operand.

For getting the similarity coefficient, we used the cosine similarity rule to identify short sentences. We used nltk vectorizer, to vectorize the two sentences, followed by comparing them based on the cosine similarity between them.

Cosine similarity leads to a good measure of similarity between short sentences, and so far, the identification has been close to perfect in most of the case.

We utilized similarity rules, instead of direct parsing, as the text may not have all the words in the respective operand, but can still match.

For example, the sentence the velocity of the vehicle, will still match to ‘vehicle_speed’, when considering the window ‘velocity vehicle’ (stop words removed). Velocity being a synonym of speed, will be given higher score in the match.

##### Example Runs:

The vehicle speed has to be less than the truck speed.
vehicle_speed< truck_speed

The speed of the vehicle is more than displacement

vehicle_speed > vehicle_displacement

Distance between vehicle X and vehicle Y should be between 10m and 20m

distance{vehicleX}-distance{vehicley} in [10,20]m

Speed of vehicle X should be less than speed of vehicle Y by 10m/s

speed_vehicle_X=speed_vehicle_Y-10m/s

Speed of vehicle X should be more than speed of vehicle Y by 10m/s

speed_vehicle_X= Speed_vehicle_Y+10m/s


