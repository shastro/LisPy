#Simple tool to return if a string is possibly a float
#Has important edge cases like NAN == float
def isFloat(string):
	try:
		float(string)
		return True
	except ValueError:
		return False