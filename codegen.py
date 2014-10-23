class CodeGen:

	def __init__(self):
		self.x = 1
		self.t = 1
		self.data = {}
		self.pilaSaltos = []

	def add(self, op, oper1, oper2, asigna):
		if oper2 != -1:
			stmp=str(self.t)
			tmp='t' + stmp
			self.data[self.x]=[op, oper1, oper2, tmp]
			self.x=self.x+1
			self.t=self.t+1
		else:
			self.data[self.x]=[op, oper1, oper2, asigna]
			self.x=self.x+1

	def addQ(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3]
		self.x=self.x+1

	def addGoTo(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3]
		self.pilaSaltos.append(self.x)
		self.x=self.x+1

	def addGoToE(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3]
		quadro = self.pilaSaltos.pop()
		self.pilaSaltos.append(self.x)
		self.x=self.x+1
		self.data[quadro][3] = self.x

	def addcontinueG(self):
		quadro = self.pilaSaltos.pop()
		self.data[quadro][3] = self.x

	def addcontinueW(self):
		salida = self.pilaSaltos.pop()
		retorno = self.pilaSaltos.pop()
		self.data[self.x]=['goTo', -1, -1, retorno]
		self.x=self.x+1
		self.data[salida][3] = self.x

	def addcontinueR(self, cte):
		temporal = self.pilaSaltos.pop()
		regreso = self.pilaSaltos.pop()
		stmp=str(self.t)
		tmp='t' + stmp
		self.data[self.x]=['+', temporal, 1, tmp]
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['=', tmp, -1, temporal]
		self.x=self.x+1
		stmp=str(self.t)
		tmp='t' + stmp
		self.data[self.x]=['==', temporal, cte, tmp]
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['goToF', tmp, -1, regreso]
		self.x=self.x+1

	def addGoToW(self):
		self.pilaSaltos.append(self.x)

	def addGoToR(self):
		stmp=str(self.t)
		tmp='t' + stmp
		self.data[self.x]=['=', 0, -1, tmp]
		self.x=self.x+1
		self.t=self.t+1
		self.pilaSaltos.append(self.x)
		self.pilaSaltos.append(tmp)

	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	def getQuad(self, key):
		return self.data[key]

	def getX(self):
		return self.x - 1

	def getnextX(self):
		return self.x

	def lasttemp(self):
		ltemp=self.t-1
		stmp=str(ltemp)
		tmp='t' + stmp
		return tmp

	def empty(self):
		self.x = 1
		self.t = 1
		self.data = {}

	def echo(self):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4)

	def write(self):
		f = open('out-quads', 'w')
		print >> f, "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print >> f, "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print >> f, str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4)
		f.close()

	def echoQ(self, tabvar, tabconst):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for a in self.data:
			quad = self.getQuad(a)
			q = list()
			i = 0
			for x in quad:
				if (tabvar.lookup(x)==True):
					q.append(tabvar.getDir(x))
				elif (tabconst.lookup(x)==True):
					q.append(tabconst.getDir(x))
				else:
					q.append(quad[i])
				i = i + 1
			print str(a).rjust(4) + "|".ljust(4) + str(q[0]).ljust(4) + "|".ljust(4) + str(q[1]).ljust(4) + "|".ljust(4) + str(q[2]).ljust(4) + "|".ljust(4) + str(q[3]).ljust(4) + "|".ljust(4)

	def writeQ(self, tabvar, tabconst):
		f = open('quads.smo', 'w')
		for a in self.data:
			quad = self.getQuad(a)
			q = list()
			i = 0
			for x in quad:
				if (tabvar.lookup(x)==True):
					q.append(tabvar.getDir(x))
				elif (tabconst.lookup(x)==True):
					q.append(tabconst.getDir(x))
				else:
					q.append(quad[i])
				i = i + 1
			print >> f, str(a) + "|" + str(q[0]) + "|" + str(q[1]) + "|" + str(q[2]) + "|" + str(q[3])
		f.close()

	def __str__(self):
		return repr(self.data)

'''
z=CodeGen()
z.add('+','a','b')
z.add('+','t1',-1)
print z.lasttemp()
print z
'''