import sys

def senderror(x, linenumber, *resto):
	if x == 1:
		print("ERROR // Syntax at '%s'" % resto[0])
	elif x == 2:
		print("ERROR // Incompatible operation")
	elif x == 3:
		print("ERROR // Assignation type in '%s'" % resto[0])
	elif x == 4:
		print("ERROR // VAR %s not found" % resto[0])
	elif x == 5:
		print("ERROR // IF-ELSE requires boolean compare" % resto[0])
	elif x == 6:
		print("ERROR // Variable %s already assign with type %s" % (resto[0], resto[1]))
	elif x == 7:
		print("ERROR // Module %s not found" % resto[0])
	elif x == 8:
		print("ERROR // Parameter type %s is expected" % resto[0])
	elif x == 9:
		if resto[1] == 1:
			print("ERROR // Module %s expects %d parameter" % (resto[0], resto[1]))
		else:
			print("ERROR // Module %s expects %d parameters" % (resto[0], resto[1]))
	elif x == 10:
		print("ERROR // Type INT/FLOAT is expected")
	print "-LINE //", linenumber
	sys.exit()