import sys

def senderror(x, linenumber, *resto):
	if linenumber == 0:
		linenumber = 1

	if x == 1:
		print("ERROR // Syntax at '%s'" % resto[0])
		print "-LINE //", linenumber
	elif x == 2:
		print("ERROR // Incompatible operation")
		print "-LINE //", linenumber
	elif x == 3:
		print("ERROR // Assignation type in '%s'" % resto[0])
		print "-LINE //", linenumber
	elif x == 4:
		print("ERROR // Variable <%s> not found" % resto[0])
		print "-LINE //", linenumber
	elif x == 5:
		print("ERROR // IF-ELSE requires boolean compare" % resto[0])
		print "-LINE //", linenumber
	elif x == 6:
		print("ERROR // Variable <%s> already assign with type %s" % (resto[0], resto[1]))
	elif x == 7:
		print("ERROR // Module <%s> not found" % resto[0])
		print "-LINE //", linenumber
	elif x == 8:
		print("ERROR // Parameter type %s is expected" % resto[0])
		print "-LINE //", linenumber
	elif x == 9:
		if resto[1] == 1:
			print("ERROR // Module <%s> expects %d parameter" % (resto[0], resto[1]))
		else:
			print("ERROR // Module <%s> expects %d parameters" % (resto[0], resto[1]))
		print "-LINE //", linenumber
	elif x == 10:
		print("ERROR // Type INT/FLOAT is expected")
		print "-LINE //", linenumber
	elif x == 11:
		print("ERROR // Module <%s> already exists") % resto[0]
		print "-LINE //", linenumber
	elif x == 12:
		print("ERROR // Dimension value must be greater than 0")
		print "-LINE //", linenumber
	elif x == 13:
		print("ERROR // Variable <%s> must be a matrix") % resto[0]
		print "-LINE //", linenumber
	elif x == 14:
		print("ERROR // Variable <%s> must be an array") % resto[0]
		print "-LINE //", linenumber
	elif x == 15:
		if resto[1] == 1:
			print("ERROR // Variable <%s> already assign as an array.") % resto[0]
		elif resto[2] == 2:
			print("ERROR // Variable <%s> already assign as a matrix.") % resto[0]
		print "-LINE //", linenumber
	elif x == 16:
		print("ERROR // Variable <%s> not declared as array/matrix") % resto[0]
		print "-LINE //", linenumber
	elif x == 17:
		if resto[1] != None:
			print("ERROR // Module <%s> returns <%s>") % (resto[0], resto[1])
		else:
			print("ERROR // Module <%s> should have no RETURN value") % resto[0]
		print "-LINE //", linenumber
	elif x == 18:
		print("ERROR // No RETURN should be at WORKSPACE")
		print "-LINE //", linenumber
	elif x == 19:
		print("ERROR // Module <%s> expects RETURN value") % resto[0]
	elif x == 20:
		print("ERROR // Module <%s> should have no RETURN value") % resto[0]
	sys.exit()