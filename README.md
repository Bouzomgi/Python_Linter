####################################################################################################################

Name: Brian Ouzomgi

Honors Option Final Project for CMPSC465

Basic Python Code Linter


Function:

This script (start.py) has a global variable "currFile", the name of any file in the same folder.
The code opens the file, reads the text, and scans line by line to detect style, indentation, declaration, and 
infinite loop errors. If there is an error, a corresponding message will print on screen and the script will 
terminate.

The code does not use any eval or try/accept function calls in attempt to raise efficiency (as an added challenge).
This script would be way easier to write if I used them.

-> Style

Raises errors if control statements lack a colon at the end, incorrect ordering of if/elif/else chains

-> Indentation

Raises errors if invalid number of spaces, incorrect tabbing after control statements, incorrect tabbing
after assignment statements, ending a program with a control statement

-> Assignment

Raises errors if attempting to use a variable in a condiditional if that variable has not been declared yet, 
if attempting to assign a variable to another variable that hasn't been declared yet.

-> Infinite Loops

If the code sees an infinte loop that is valid to enter, it will examine the conditional statement. It will 
store the conditional statement's variable's value as "oldValue", run through the while loop's code and 
store the adjusted conditional statement's value as "newValue". It will then check if the step from oldValue
to newValue is in the direction to break out of the loop. If not, it will deem it as infinite

EXAMPLE:

i = 1
while i > 0:
	i += 1

The program will know i is the conditional variable and store its value as oldValue (in this example, oldValue
would be 1). It will then run though the loop (i += 1, so i = 2). It will then store the conditional variable as
newValue (newValue = 2). Because newValue > oldValue, and the while loops condition will only be broken by decrementation, 
we deem this loop as infinite

***Due to how the code is implemented, there is actually 2 runs through the loop. It still works the way we want it to***

The script is somewhat intelligent. It will look at the conditions of "if" statements to judge if it actually should enter them 
or not. Hello6.py demonstrates this well (in that example, the code knows not to enter the if statement, allowing it to 
enter the infinite while loop like it should).

Implementation:
	
The script uses a stack to store each line to revisit old control statements easily and to compare each lines indentation to the previous's. 

There is also a queue implemented by way of two stacks. Infomation from my main stack is dumped into an inner stack, "conditionalStack", to form a queue I pull from in my infinite while loop check.

Limitations:

The infinite while loop section is only guarenteed to work with addition, subtraction, and multiplication/division of
same sign constants. I have not extensively bugtested for long selections of code. This script serves as a POC for 
short scripts. 


I have included 7 traces: hello1.py to hello7.py, all demonstrating a unique feature of this linter. To run, change the 
variable "currFile" to the name of the file you want to run, and then run the code through your command shell. Enjoy!


####################################################################################################################
