import sys

def senderror(x, *resto):
	if x == 1:
		print("RUNTIME ERROR // Division by ZERO was found")
	elif x == 2:
		print("RUNTIME ERROR // Dim variable is OUT OF BOUNDS")
	sys.exit()