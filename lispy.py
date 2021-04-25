# import argparse
import operator as op
import math
from pprint import pprint
import sys


class DebugException(Exception):
    pass


def plispyList(llist):
    print("(", end='')
    for item in llist:
        if type(item) == list:
            plispyList(item)
        else:
            if item == llist[-1]:
                print(item, end="")
            elif item == llist[0]:
                print(item, end=" ")
            else:
                print("", item, end=" ")

    print(")",end='')


def buildMap(args, evalArgs, expr):
    dmap = {}
    for arg, evalArg in zip(args, evalArgs):
        dmap.update({arg:evalArg})
        
    return dmap

def recursive_Repl(dmap, llist):
    newlst = llist[:]
    for index, item in enumerate(llist):
        if type(item) is list:
            newlst[index] = recursive_Repl(dmap, llist[index])
            
        elif isinstance(item, (str, int, float)):
            if llist[index] in dmap:
                newlst[index] = dmap[llist[index]]
    return newlst
#This interpreter will assume atoms are integers floats or strings (Symbols)
#Expressions (s-expressions) will either be atoms or lists
#Lisp lists will be python lists

Atom = (int, str, bool)
Expr = (Atom, list) 
SENTINEL_EXPR_ERR = float("-inf")

class Env:
    
    def __init__(self, inheritEnv):
        self.env = {}
        self.env.update({
            '+': op.add, '-': op.sub, '*': op.mul, '/':op.truediv,
            'car': lambda a: a[0],
            'cdr': lambda a: a[1:],
            'cons': lambda a,b: [a] + b,
            'sqrt': lambda a: math.sqrt(a),
            'pow': lambda a, b: math.pow(a, b),
            '>': op.gt, '<': op.lt, 
            '=': op.eq, "!=": op.ne,
            "and": lambda a, b: a and b,
            "or": lambda a, b: a or b,
            "not": lambda a: not a,
            '>=': op.ge, '<=':op.le
            # tuple("foo"): [["a","b"], ["*", "a", "b"]]
        



        })
        self.env.update(inheritEnv)

    def appendEnv(self, key, value):
        self.env.update({key: value})

    def isDefined(self, key):
        return key in self.env

    def getEnv(self):
        return self.env

class Parser:
    def __init__(self):
        self.ast = []

    def tokenize(self, string):
        #Remove replace "(/)" with spaces then split on spaces to get list of
        #whitespace deliminated objects
        tokenized = string.replace('(', " ( ").replace(")", " ) ").replace("'", " ' ").split()
        openCount = 0
        for token in tokenized:
            if token == "(":
                openCount += 1
            elif token == ")":
                openCount -= 1

        if openCount != 0:
            if openCount > 0:
                print("SyntaxError: missing )")
            else:
                print("SyntaxError: missing (")
            return SENTINEL_EXPR_ERR
        else:
            return tokenized


    def buildAST(self, tokenized):
        if tokenized == SENTINEL_EXPR_ERR:
            return SENTINEL_EXPR_ERR

        if len(tokenized) == 0:
            print("SyntaxError: unexpected EOF while parsing")
            return SENTINEL_EXPR_ERR
        #Pop first
        token = tokenized.pop(0) 
        if token == '(':
            currentexpr = []
            try:
                while tokenized[0] != ')':
                    currentexpr.append(self.buildAST(tokenized))
                tokenized.pop(0)
                return currentexpr
            except IndexError:
                print("SyntaxError: missing )")
                return SENTINEL_EXPR_ERR
        elif token == ")":
            print("SyntaxError: unexpected )")
            return SENTINEL_EXPR_ERR
        #TODO UNFINISHED
        elif token == "'":
            currentexpr = ["'"]
            currentexpr.append(self.buildAST(tokenized))
            return currentexpr
        else:
            return self.isAtom(token)

    def isAtom(self, token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                if(token.lower() == "t"):
                    return True
                elif(token.lower() == "nil"):
                    return False
                    
                else:
                    #Token is a symbol
                    return str(token)




    def parse(self, string):
        tokenized = self.tokenize(string)
        self.ast = self.buildAST(tokenized)
        return self.ast


# Container for interpreter state
class LispInterpreter:
    #Anything here shared by all instances
    def __init__(self):
        print("Welcome to LisPy! A simple Lisp Interpreter! Skyler Hughes - CSE324")
        print("Use DEBUG to see abstract syntax tree, call invocations, and env")
        print("Use QUIT to quit")       
        self.rawInputLine = None
        self.debug = False

        # self.outfile = open("output.file", "w")
        # sys.stdout = self.outfile
        #Need some kind of structure to hold expressions for now use list 

        self.ast = [] #List with each index going one level deeper into the parseTree
        self.parser = Parser()
        self.env = Env({})

    def getInput(self):
        self.rawInputLine = input(">")
        # self.outfile.write(">" + self.rawInputLine)

    #For now just assume we have only one expression
    #Goal! Create parseTree
    def parse(self):
        if(self.rawInputLine == "QUIT"):
            # self.outfile.close()
            exit()
        elif(self.rawInputLine == "DEBUG"):
            self.debug = not self.debug
            print("DEBUG:", self.debug)
            print(self.rawInputLine)
            raise DebugException
        else:
            self.ast = self.parser.parse(self.rawInputLine)

            if self.debug:
                print("ast", self.ast)

    #Handles evaluation of expression tree
    #Will need to be recursive at some point
    #Base cases
    #Expr is atom
    #
    def eval(self, expr, env):
        
        if expr == []:
            return False


        elif isinstance(expr, (int, float)):
            return expr

        elif self.env.isDefined((expr[0],)):
            symbolDef = self.env.getEnv()[(expr[0],)]
            fname = expr[0]
            fargs = symbolDef[0]
            fbody = symbolDef[1]


            exprArgs = expr[1:]
            if(len(exprArgs) != len(fargs)):
                print(f"Environment Error: function \"{fname}\" expected {len(fargs)} args got {len(exprArgs)}")
                return SENTINEL_EXPR_ERR
            else:
                evalArgs = [self.eval(x, env) for x in exprArgs]
                if(self.debug):
                    print(f"invo <user-def function {fname}> args {evalArgs}")

                dmap = buildMap(fargs, evalArgs, fbody)
                fbody_new = recursive_Repl(dmap, fbody)
                return self.eval(fbody_new, env)

        elif isinstance(expr, str):
            try:
                symbolDef = self.env.getEnv()[expr] 
                return symbolDef
            except KeyError:
                print(f"Environment Error: {expr} undefined")
                return SENTINEL_EXPR_ERR

        elif expr[0] in ["define"]:

            self.env.appendEnv(expr[1], self.eval(expr[2], env))
            if self.debug:
                print("env", end="")
                pprint(self.env.getEnv())
            return self.eval(expr[2], env)   

        elif expr[0] == "set!":
            if(not self.env.isDefined(expr[1])):
                print(f"Environment Error: {expr[1]} undefined")
                return SENTINEL_EXPR_ERR
            else:
                value = self.eval(expr[2], env)  
                self.env.appendEnv(expr[1], value)
                if self.debug:
                    print("env", end="")
                    pprint(self.env.getEnv())
                return value

        #TODO implement local scoping
        elif expr[0] == "defun":
            fname = expr[1]
            args  = expr[2]
            body  = expr[3]
            self.env.appendEnv((fname,), [args, body])
            if(self.debug):
                print("env", end="")
                pprint(self.env.getEnv())

        elif expr[0] == "if":
            cond = self.eval(expr[1], env)
            return self.eval(expr[2], env) if cond else self.eval(expr[3], env)

        elif expr[0] == "'":
            return expr[1]

        else:
            try:
                func = self.eval(expr[0], env)
                args = [self.eval(x, env) for x in expr[1:]]

                if self.debug:
                    print(f"invo {func} args", args)
                return func(*args)

            except TypeError:
                print(f"{expr[0]} is not a function name; try using a symbol instead")
                return SENTINEL_EXPR_ERR

            except ZeroDivisionError:
                print("ERROR: division by zero")
                return SENTINEL_EXPR_ERR

    #begin READ EVAL PRINT LOOP
    def REPL(self):
        while True:
            self.getInput()
            # self.outfile.write(f"> {self.rawInputLine}")

            try:
                self.parse()
            except DebugException:
                continue

            evaluation = self.eval(self.ast, {})

            if evaluation == False:
                print("NIL")
                # self.outfile.write("NIL")
            elif evaluation == None:
                # print("")
                continue
            elif evaluation == SENTINEL_EXPR_ERR:
                continue
            #Quote operator
            elif type(evaluation) == list:
                # defaultStdOut = sys.stdout
                # sys.stdout = self.outfile
                plispyList(evaluation)
                print("\n", end="")
                # sys.stdout = defaultStdOut

            else:
                print(evaluation)
                # self.outfile.write(f"{evaluation}")
            # self.printEval()



    #Need way to print evaluations to the screen


# class constLiteral
def main():

    lpy = LispInterpreter()
    lpy.REPL()
    # REPL is the core of lisp, so i need a READ-EVAL-PRINT-LOOP







if (__name__ == "__main__"):
    main()