import sys

def senderror(x, *resto):
	if x == 1:
		print("ERROR // Syntax at '%s'" % resto[0])
	elif x == 2:
		print("ERROR // Incompatible operation")
	elif x == 3:
		print("ERROR // Assignation type in '%s'" % resto[0])
	elif x == 4:
		print("ERROR // VAR not found" % resto[0])
	elif x == 5:
		print("ERROR // IF-ELSE requires boolean compare" % resto[0])
	sys.exit()