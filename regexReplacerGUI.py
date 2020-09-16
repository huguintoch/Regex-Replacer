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

# Main function

def replaceRegex(inputStr, regex, replacement):

  FSA = Automata(regex)
  res = ""
  i = j = 0
  size = len(inputStr)

  if(size == 0 and FSA.initialState in FSA.finalStates):
    res = replacement
  else: 
    while j < size:
        currentOutput = prevOutput = FSA.initialState.applySymbol(inputStr[j])
        while currentOutput != None and j < len(inputStr):
            j+=1
            prevOutput = currentOutput
            if j <= size-1:
                currentOutput = currentOutput.applySymbol(inputStr[j])
        if prevOutput in FSA.finalStates:
            res += replacement
        else:
            if i == j:
                j+=1
            res += inputStr[i:j]
        i=j

  return res

# WebApp

"""
MIT License
Copyright (c) 2018 Claude SIMON (https://q37.info/s/rmnmqd49)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk as Atlas

head = """
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">

  <title>Regex Replacer</title>
"""

body = """
  <div class="container-fluid">
    <div class="row justify-content-center">
      <h1>Regex replacer</h1>
      <br><br><br>
      <div class="col-12">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">Input string</span>
          </div>
          <input id="input" type="text" class="form-control" data-xdh-onevent="Replace">
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-6">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">Regular expression</span>
          </div>
          <input id="regex" type="text" class="form-control">
        </div>
      </div>
      <div class="col-6">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">String replacement</span>
          </div>
          <input id="replacement" type="text" class="form-control">
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-12">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">Result string</span>
          </div>
          <input id="output" type="text" class="form-control" readonly data-xdh-onevent="Replace">
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <button type="button" class="btn btn-primary" data-xdh-onevent="Replace">Replace</button>
      <button type="button" class="btn btn-secondary" data-xdh-onevent="Clear">Clear</button>
    </div>
  </div>
  <!-- Optional JavaScript -->
  <!-- jQuery first, then Popper.js, then Bootstrap JS -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
"""

def ac_connect(dom):
  dom.inner("", body)
  dom.focus( "input")

def ac_replace(dom):
  regex = dom.get_content("regex")
  if not validRegex(regex):
    dom.alert("Invalid regex. Supported operators: + and *")
  else:
    inputStr = dom.get_content("input")
    regex = dom.get_content("regex")
    replacement = dom.get_content("replacement")
    res = replaceRegex(inputStr, regex, replacement)
    dom.set_content("output", res)
  dom.focus("output")

def ac_clear(dom):
  dom.set_content("input", "" )
  dom.set_content("regex", "" )
  dom.set_content("replacement", "" )
  dom.set_content("output", "" )
  dom.focus("input")

def validRegex(regex):
  size = len(regex)
  if size == 0:
    return False
  for i in range(size):
    if i == 0 and (regex[i] == "*" or regex[i] == "+"):
      return False
    elif i < size-1:
      if regex[i] == "*":
        if i == size-2 and (regex[i+1] == "+" or regex[i+1] == "*"):
          return False
        elif regex[i+1] == "*":
          return False
      elif regex[i] == "+" and (regex[i+1] == "+" or regex[i+1] == "*"):
        return False
  return True
  
callbacks = {
  "": ac_connect,
  "Replace": ac_replace,
  "Clear": ac_clear,
}

Atlas.launch(callbacks, None, head)