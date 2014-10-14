class CodeGen:

	def __init__(self):
		self.x = 1
		self.t = 1
		self.data = {}

	def add(self, op, oper1, oper2):
		stmp=str(self.t)
		tmp='t' + stmp
		self.data[self.x]=[op, oper1, oper2, tmp]
		self.x=self.x+1
		self.t=self.t+1

	def addassign(self, op, oper1, oper2):
		self.data[self.x]=[op, oper1, -1, oper2]
		self.x=self.x+1

	def lasttemp(self):
		ltemp=self.t-1
		stmp=str(ltemp)
		tmp='t' + stmp
		return tmp

	def echo(self):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4)

	def __str__(self):
		return repr(self.data)

'''
z=CodeGen()
z.add('+','a','b')
z.add('+','t1',-1)
print z.lasttemp()
print z
'''