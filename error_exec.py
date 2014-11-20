import sys

def senderror(x, *resto):
	if x == 1:
		print("RUNTIME ERROR // Division by ZERO was found")
	elif x == 2:
		print("RUNTIME ERROR // Index variable is OUT OF BOUNDS")
	elif x == 3:
		print("RUNTIME ERROR // Out of MEMORY")
	elif x == 4:
		print("RUNTIME ERROR // An INPUT type <%s> was expected") % resto[0]
	sys.exit()