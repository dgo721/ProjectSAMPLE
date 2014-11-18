import sys

def senderror(x, *resto):
	if x == 1:
		print("RUNTIME ERROR // Division by ZERO was found")
	elif x == 2:
		print("RUNTIME ERROR // Index variable is OUT OF BOUNDS")
	elif x == 3:
		print("RUNTIME ERROR // Out of MEMORY")
	sys.exit()