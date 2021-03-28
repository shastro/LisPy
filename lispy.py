# import argparse
import operator as op
import math


Atom = (int, str)
Exp = (Atom, list)



class Env:
	
	def __init__(self, inheritEnv):
		self.env = {}
		self.env.update(inheritEnv)
		self.env.update({

			'+': op.add, '-': op.sub, '*': op.mul, '/':op.floordiv,
			'car': lambda a: a[0],
			'cdr': lambda a: a[1:],
			'cons': lambda a,b: [a] + b,
			'sqrt': lambda a: math.sqrt(a),
			'pow': lambda a: math.pow(a),
			'>': op.gt, '<': op.lt, 
			'=': op.eq, "!=": op.ne,
			"and": lambda a, b: a and b,
			"or": lambda a, b: a or b,
			"not": lambda a: not a,
			"if": lambda test, conseq, alt: conseq if test else alt


		



		})

	def appendEnv(key, value):
		self.env.update({key: value})


class Parser:
	def __init__(self):
		self.ast = []

	def tokenize(self, string):
		return string.replace('(', " ( ").replace(")", " ) ").split()

	def buildAST(self, tokenized):
		if len(tokenized) == 0:
			raise SyntaxError("unexpected EOF while parsing")

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
				raise SyntaxError("missing )")

		elif token == ")":
			raise SyntaxError('unexpected )')
		else:
			return self.atom(token)

	def atom(self, token):
		try:
			int(token)
		except ValueError:
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
		self.rawInputLine = None

		#Need some kind of structure to hold expressions for now use list 

		self.ast = [] #List with each index going one level deeper into the parseTree
		self.symbolTable = {} #SymbolTable maps symbols to 
		self.parser = Parser()
		self.env = Env({})

	def getInput(self):
		self.rawInputLine = input(">")

	#For now just assume we have only one expression
	#Goal! Create parseTree
	def parse(self):
		if(self.rawInputLine == "quit()"):
			exit()

		else:
			self.ast = self.parser.parse(self.rawInputLine)
			print(self.ast)

	#Handles evaluation of expression tree
	#Will need to be recursive at some point
	def eval(self, expr):
		if expr

		self.ast = []


	def printEval(self):
		pass

	#begin READ EVAL PRINT LOOP
	def REPL(self):
		while True:
			self.getInput()
			self.parse()
			self.eval()
			self.printEval()



	#Need way to print evaluations to the screen

#Abstract class for expressions
# class Expression:

# 	def __init__(self):
# 		print("ERR DO NOT INSTANTIATE ABSTRACT CLASS EXPRESSION")
# 		exit(1)

# 	def eval(self):
# 		print("MUST OVERRIDE eval()")
# 		exit(1)

# 	def asString(self):
# 		print("MUST OVERRIDE asString()")
# 		exit(1)

# 	def printExpr(self):
# 		print("MUST OVERRIDE printExpr")
# 		exit(1)

# class Number(Expression, list):
# 	def __init__(self, strLiteral):
# 		self.strLiteral = strLiteral
# 		self.numConst = None

# 	def eval(self):
# 		self.numConst = int(self.strLiteral)
# 		return self.numConst

# 	def asString(self):
# 		return str(self.numConst)

# 	def printExpr(self):
# 		print(self.asString())

# class constLiteral
def main():

	# parser = argparse.ArgumentParser(description='A Simple Lisp Interpretor in Python - Skyler Hughes - CSE324')

	lpy = LispInterpreter()
	lpy.REPL()
	# REPL is the core of lisp, so i need a READ-EVAL-PRINT-LOOP







if (__name__ == "__main__"):
	main()