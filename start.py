#AUTHOR: Brian Ouzomgi

import math

currFile = "hello7.py"

keyWordSet = {"while", "if", "elif", "else", "for", "def"}
conditionalSet = {"<", ">", ">=", "<=", "=="}
operatorSet = {"+", "-", "/", "*", "=", "+=", "-="}

#Returns the keyword in a line (keywords being whie, if, elif, else, for, or def)
#If there is no keyword, return NONE
def getKeyword(lineInfo):
	if not lineInfo: return None

	if isinstance(lineInfo, tuple): lineInfo = lineInfo[0]

	firstWord = ""
	for char in lineInfo:
		if char == ' ' or char == ':':
			break
		firstWord += char
	return firstWord if firstWord in keyWordSet else None

#Returns the content between the keyword and the ':'
#EX: "for i < 2:" -> returns "i < 2"
def getConditional(lineInfo):
	if not lineInfo: return None

	if isinstance(lineInfo, tuple): lineInfo = lineInfo[0]

	start = lineInfo.find(" ")
	return lineInfo[start+1: -1]

#Takes in a string. If it is an integer, converts it to an integer type
#Otherwise, just returns that string
def convertToInt(value):
	if isinstance(value, str) and (value[0] == "-") and value[1:].isnumeric():
		return int(value)
	
	elif isinstance(value, str) and not value.isnumeric(): 
		return value

	return int(value)

#Returns a boolean corresponding whether the input is a list or not
def isList(value):
	if value[0] == '[' and value[-1] == ']':
		return True
	return False

#Takes in a traditional assignment or conditional three part line and 
#returns the associated variable, operation, and operatee
#EX "i = 4" returns i as the variable, = as the operation, and 4 as the operatee
def extractContent(lineInfo):
	variable = ""
	operatee = ""

	if isinstance(lineInfo, int): return None

	for i in range(len(lineInfo)):
		if (lineInfo[i] in operatorSet) or (lineInfo[i] in conditionalSet):
			break
		if not lineInfo[i].isspace():
			variable += lineInfo[i]

	operation = lineInfo[i]
	if (i+1 < len(lineInfo)) and lineInfo[i+1] == "=":
		operation += "="
		i += 1

	for j in lineInfo[i + 1:]:
		if not j.isspace():
			operatee += j

	if not variable or not operation or not operatee: return None

	variable = convertToInt(variable)
	operatee = convertToInt(operatee)

	return variable, operation, operatee

#Converts variables to their numeric values and performs the operation 
#beteen those variables or numbers. Returns the output of that operation
def operate(dictionary, variable, operation, operatee):
	if variable in dictionary: variable = dictionary[variable]
	if operatee in dictionary: operatee = dictionary[operatee]

	if operation == "+":
		return variable + operatee
	elif operation == "-":
		return variable - operatee
	elif operation == "*":
		return variable * operatee
	elif operation == "/":
		return variable / operatee

#Likwise, converts variables to their numeric values and performs the conditional operation 
#beteen those variables or numbers. Returns the boolean response of that operation.
def evaluate(dictionary, variable, operation, operatee):
	if variable in dictionary: variable = dictionary[variable]
	if operatee in dictionary: operatee = dictionary[operatee]

	if operation == "<":
		return variable < operatee
	elif operation == ">":
		return variable > operatee
	elif operation == "<=":
		return variable <= operatee
	elif operation == ">=":
		return variable >= operatee
	elif operation == "==":
		return variable == operatee

#Checks for an assignment. If so, calls extractContent to pull relavent information and 
#performs the operation with operate. The final answer is then assigned to the initial variable
#by way of the variable dictionary
def checkEquality(dictionary, line, currLine, lineCount):
	#If the line includes assignment, add it to the variable dictionary
	if "=" in line and not "==" in line:
		variable, operation, operatee = extractContent(line)
		if extractContent(operatee):
			operatee = operate(dictionary, *extractContent(operatee))
		elif operation == "+=" or operation == "-=":
			if variable not in dictionary: 
				print(f'Assignment Error on line {lineCount}: {line}')
				return
			operatee = convertToInt(operatee)
			operatee = operate(dictionary, variable, operation[0], operatee)

		if variable.isnumeric():
			print(f'Assignment Error on line {lineCount}: {line}')
			return

		if not isinstance(operatee, int) and not isList(operatee):
			if operatee not in dictionary:
				print(f'Assignment Error on line {lineCount}: {line}')
				return
			operatee = dictionary[operatee]

		if not isinstance(operatee, int) and isList(operatee):
			operatee = [convertToInt(i) for i in operatee[1:-1].split(",")]
		
		dictionary.update({variable: operatee})
	return 1

#Traditional peek of a stack
def peek(stack, depth = 1):
	return stack[-depth] if stack else None

def main():
	stack = [("", 0)]
	variableDict = {}
	conditionalStack = []
	stallUntil = math.inf
	with open(currFile,"r") as file:
		comment = False
		lineCount = 1

		for line in file.readlines():

			#The code ignores comments
			if '"""' in line or "'''" in line:
				comment = not comment
				lineCount += 1
				continue

			if comment or line[0] == '#':
				lineCount += 1
				continue

			#Deals with indentations. Counts 
			if not line.isspace():
				indent = 0
				for character in line:
					if character == " ":
						indent += 0.25
					elif character == "\t":
						indent += 1
					else:
						break

				#The indentation of each line must be a multiple of 1 (if each space counts as 0.25)
				if indent%1 != 0:
					print(f'Invalid indentation scheme on line {lineCount}')
					return

				line = line.replace("\n", "").replace("\t","").strip()

				#Control Statements must end with a colon
				if getKeyword(line):
					if line[-1] != ':':
						print(f'Declaration Error on line {lineCount}: {line}')
						return
					elif extractContent(getConditional(line))[0] not in variableDict:
						print(f'Did not declare variable on line {lineCount}: {line}')
						return

				#Ensures that every elif or else is under an if statement
				if getKeyword(line) in {"elif", "else"}:
					currIndex = 1
					while (peek(stack, currIndex)[1] != indent):
						currIndex += 1
					if getKeyword(peek(stack, currIndex)) not in {"if", "elif"}:
						print(f'If/Elif/Else Error on line {lineCount}: {line}')

				#A line underneath a control statement must be indented once
				if getKeyword(peek(stack)):
					if peek(stack)[1] != indent - 1:
						print(f'HERE Indentation Error on line {lineCount}: {line}')
						return

				#Otherwise, the current line can only be at the same indentation level or less than the line above
				elif indent not in range(0, peek(stack)[1] + 1):
					print(f'Indentation Error on line {lineCount}: {line}')
					return

				#If the code does not satify a conditional, the linter should not execute that code or any other
				#lines indented beyond it
				if ((getKeyword(line) in {"if", "elif", "while"}) and (not evaluate(variableDict, *extractContent(getConditional(line)))) \
					and stallUntil == math.inf):
					stallUntil = indent

				elif (indent <= stallUntil):
					stallUntil = math.inf

				#Removes irrelevant indent content from the stack
				if peek(stack)[1] > indent:
					conditionalStack = []
					while indent != peek(stack)[1]:
						conditionalStack.append(stack.pop())

					keyword = getKeyword(peek(stack))

					if keyword == "while":

						keyVariable, keyCondition, keyConstant = extractContent(getConditional(peek(stack)))

						#Extracts the conditional variable and stores its value as oldValue.
						#Repeats operations stored in the while loop. Checks the conditional variable's value again
						#If that value does not move towards the final breaking point of the loop, claim the
						#loop is infinite and exit the program
						if (keyCondition in {"<", "<="}) and evaluate(variableDict, keyVariable, keyCondition, keyConstant):

							oldAssignment = variableDict[keyVariable]
							newDict = variableDict.copy()

							for i in conditionalStack[::-1]:
								if not checkEquality(newDict, i[0], line, lineCount): return

							oldValue = variableDict[keyVariable]
							newValue = newDict[keyVariable]

							if oldValue > newValue:
								lineInfo = peek(stack)
								print(f'Infinite While Loop on line {lineInfo[2]}: {lineInfo[0]}')
								return

						elif (keyCondition in {">", ">="}) and evaluate(variableDict, keyVariable, keyCondition, keyConstant):

							oldAssignment = variableDict[keyVariable]
							newDict = variableDict.copy()

							for i in conditionalStack[::-1]:
								if not checkEquality(newDict, i[0], line, lineCount): return

							oldValue = variableDict[keyVariable]
							newValue = newDict[keyVariable]

							if oldValue < newValue:
								lineInfo = peek(stack)
								print(f'Infinite While Loop on line {lineInfo[2]}: {lineInfo[0]}')
								return

						elif (keyCondition == "==") and evaluate(variableDict, keyVariable, keyCondition, keyConstant):

							oldAssignment = variableDict[keyVariable]
							newDict = variableDict.copy()

							for i in conditionalStack[::-1]:
								if not checkEquality(newDict, i[0], line, lineCount): return

							oldValue = variableDict[keyVariable]
							newValue = newDict[keyVariable]

							if oldValue == newValue:
								lineInfo = peek(stack)
								print(f'Infinite While Loop on line {lineInfo[2]}: {lineInfo[0]}')
								return

				#If the previous control statement is not entered, do not evaluate the content inside
				if (indent <= stallUntil):
					if not checkEquality(variableDict, line, line, lineCount): return
					stack.append((line, indent, lineCount))

				else:
					stack.append(("pass", indent, lineCount))

			lineCount += 1
			
		#File can't end with a control statement
		if getKeyword(peek(stack)):
			print(f'Indentation Error on line {peek(stack)[2]}: {peek(stack)[0]}')
			return

main()



