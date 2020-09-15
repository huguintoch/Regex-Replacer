# Regex replacer project
# Hugo Isaac Valdez Ruvalcaba - A01631301

# Classes

class State:
    def __init__(self, name):
        self.name = name
        self.transitions = { }

    def addTransition(self, symbol, state):
        self.transitions[symbol] = state

    def applySymbol(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        else:
            return None


class Automata:
    def __init__(self, regex):
        self.regex = regex
        self.finalStates = []
        self.states = self.buildStates()
        self.initialState = self.states[0]
        
    def buildStates(self):
        divExp = self.splitRegex()
        states = [State("q0")]
        nState = 1
        for i in divExp:
            finalStates = []
            prev = current = states[0]
            for j in range(len(i)):
                if current.applySymbol(i[j][0]) == None:
                    newState = State("q"+str(nState))
                    current.addTransition(i[j][0], newState)
                    states.append(newState)
                    nState += 1
                current = current.applySymbol(i[j][0])
                prev.addTransition(i[j][0], current)
                if "*" not in i[j]:
                    prev = current
                    if j == len(i)-1 or j < len(i)-1 and "*" not in i[j+1]:
                        finalStates = []
                else:
                    current.addTransition(i[j][0], current)
                    finalStates.append(current)
                    finalStates.append(prev)
            finalStates.append(current)
            self.addFinalStates(finalStates)
        return states

    def addFinalStates(self, finalStates):
        for state in finalStates:
            if state not in self.finalStates:
                self.finalStates.append(state)
    
    def splitRegex(self):
        divExp = []
        union = self.regex.split("+")
        for i in union:
            symbols = []
            for j in range(len(i)):
                if j+1 < len(i) and i[j+1] == "*":
                    symbols.append(i[j]+"*")
                elif i[j] != "*":
                    symbols.append(i[j])
            divExp.append(symbols)
        return divExp

    def printAutomata(self):
        for i in self.states:
            print(i, i.name, i.transitions)
        print(self.initialState)
        print(self.finalStates)

FSA = Automata("a*c")
FSA.printAutomata()
inputStr = "aaaaaaaac"
replacer = "x"
res = ""

i = j = 0
while j < len(inputStr):
    currentOutput = prevOutput = FSA.initialState.applySymbol(inputStr[j])
    while currentOutput != None and j < len(inputStr):
        j+=1
        prevOutput = currentOutput
        if j <= len(inputStr)-1:
            currentOutput = currentOutput.applySymbol(inputStr[j])
    if prevOutput in FSA.finalStates:
        res += replacer
    else:
        if i == j:
            j+=1
        res += inputStr[i:j]
    i=j
print(res)
