from dirmods import DirMods
from tabvars import TabVars, tabvar
from tabdims import TabDims
from tabpointers import TabPointer

class CodeGen:

	def __init__(self):
		self.x = 1
		self.t = 1
		self.a = 1
		self.data = {}
		self.pilaSaltos = []
		self.scope = "*work*"

	def add(self, op, oper1, oper2, asigna):
		if oper2 != -1:
			stmp=str(self.t)
			tmp='_t' + stmp
			self.data[self.x]=[op, oper1, oper2, tmp, self.scope]
			self.x=self.x+1
			self.t=self.t+1
		else:
			self.data[self.x]=[op, oper1, oper2, asigna, self.scope]
			self.x=self.x+1

	def addQ(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
		self.x=self.x+1

	def addGoTo(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
		self.pilaSaltos.append(self.x)
		self.x=self.x+1

	def addGoToE(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
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
		self.data[self.x]=['goTo', -1, -1, retorno, self.scope]
		self.x=self.x+1
		self.data[salida][3] = self.x

	def addcontinueR(self, cte, tabtemp, linenumber):
		temporal = self.pilaSaltos.pop()
		regreso = self.pilaSaltos.pop()
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['+', temporal, 1, tmp, self.scope]
		tabtemp=tabvar(tabtemp, tmp, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['=', tmp, -1, temporal, self.scope]
		self.x=self.x+1
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['==', temporal, cte, tmp, self.scope]
		tabtemp=tabvar(tabtemp, tmp, 2, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['goToF', tmp, -1, regreso, self.scope]
		self.x=self.x+1
		return tabtemp

	def addGoToW(self):
		self.pilaSaltos.append(self.x)

	def addGoToR(self, tabtemp, linenumber):
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['=', 0, -1, tmp, self.scope]
		tabtemp=tabvar(tabtemp, tmp, 0, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.pilaSaltos.append(self.x)
		self.pilaSaltos.append(tmp)
		return tabtemp

	def addVer1(self, oper, iden, limite1, tabpointer, linenumber):
		self.data[self.x]=['ver1', oper, -1, limite1, self.scope]
		self.x=self.x+1
		stmp=str(self.a)
		tmp='_a' + stmp
		self.data[self.x]=['+dir', oper, iden, tmp, self.scope]
		tabpointer.add(tmp)
		self.x=self.x+1
		self.a=self.a+1
		return [tabpointer, tmp]

	def addVer2(self, oper1, oper2, iden, limite1, limite2, tabpointer, linenumber):
		self.data[self.x]=['ver1', oper1, -1, limite1, self.scope]
		self.x=self.x+1
		
		return [tabpointer, tmp]

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

	def gettemp(self):
		ltemp=self.t
		stmp=str(ltemp)
		tmp='_t' + stmp
		return tmp

	def lasttemp(self):
		ltemp=self.t-1
		stmp=str(ltemp)
		tmp='_t' + stmp
		return tmp

	def getScope(self):
		return self.scope

	def setScope(self, name):
		self.scope = name

	def empty(self):
		self.x = 1
		self.t = 1
		self.data = {}

	def echo(self):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4) + "SCOPE".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4) + str(self.data[key][4]).ljust(4) + "|".ljust(4)

	def write(self):
		f = open('out-quads', 'w')
		print >> f, "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print >> f, "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print >> f, str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4)
		f.close()

	def echoQ(self, dirmod, tabconst):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		tablaP = dirmod.getTable("*work*")
		tablatempP = dirmod.getTableTemp("*work*")
		for a in self.data:
			quad = self.getQuad(a)
			scope = quad[4]
			tabla = dirmod.getTable(scope)
			tablatemp = dirmod.getTableTemp(scope)
			q = list()
			i = 0
			if quad[0] == "goTo" or quad[0] == "ret" or quad[0] == "era" or quad[0] == "gosub":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "goToF" or quad[0] == "param" or quad[0] == "sample1":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True):
					q.append(tabla.getDir(quad[1]))
				elif (tablatemp.lookup(quad[1])==True):
					q.append(tablatemp.getDir(quad[1]))
				elif (tablaP.lookup(quad[1])==True):
					q.append(tablaP.getDir(quad[1]))
				elif (tablatempP.lookup(quad[1])==True):
					q.append(tablatempP.getDir(quad[1]))
				elif (tabconst.lookup(quad[1])==True):
					q.append(tabconst.getDir(quad[1]))
				else:
					q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "sample2":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				if (tabla.lookup(quad[3])==True):
					q.append(tabla.getDir(quad[3]))
				elif (tablatemp.lookup(quad[3])==True):
					q.append(tablatemp.getDir(quad[3]))
				elif (tablaP.lookup(quad[3])==True):
					q.append(tablaP.getDir(quad[3]))
				elif (tablatempP.lookup(quad[3])==True):
					q.append(tablatempP.getDir(quad[3]))
				elif (tabconst.lookup(quad[3])==True):
					q.append(tabconst.getDir(quad[3]))
				else:
					q.append(quad[3])
			else:
				for x in quad:
					#print x, a
					if (tabla.lookup(x)==True):
						q.append(tabla.getDir(x))
					elif (tablatemp.lookup(x)==True):
						q.append(tablatemp.getDir(x))
					elif (tablaP.lookup(x)==True):
						q.append(tablaP.getDir(x))
					elif (tablatempP.lookup(x)==True):
						q.append(tablatempP.getDir(x))
					elif (tabconst.lookup(x)==True):
						q.append(tabconst.getDir(x))
					else:
						q.append(quad[i])
					i = i + 1
			print str(a).rjust(4) + "|".ljust(4) + str(q[0]).ljust(4) + "|".ljust(4) + str(q[1]).ljust(4) + "|".ljust(4) + str(q[2]).ljust(4) + "|".ljust(4) + str(q[3]).ljust(4) + "|".ljust(4)

	def writeQ(self, dirmod, tabconst):
		f = open('sample.smo', 'a')
		tablaP = dirmod.getTable("*work*")
		tablatempP = dirmod.getTableTemp("*work*")
		for a in self.data:
			quad = self.getQuad(a)
			scope = quad[4]
			tabla = dirmod.getTable(scope)
			tablatemp = dirmod.getTableTemp(scope)
			q = list()
			i = 0
			if quad[0] == "goTo" or quad[0] == "ret" or quad[0] == "era" or quad[0] == "gosub":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "goToF" or quad[0] == "param" or quad[0] == "sample1":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True):
					q.append(tabla.getDir(quad[1]))
				elif (tablatemp.lookup(quad[1])==True):
					q.append(tablatemp.getDir(quad[1]))
				elif (tablaP.lookup(quad[1])==True):
					q.append(tablaP.getDir(quad[1]))
				elif (tablatempP.lookup(quad[1])==True):
					q.append(tablatempP.getDir(quad[1]))
				elif (tabconst.lookup(quad[1])==True):
					q.append(tabconst.getDir(quad[1]))
				else:
					q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "sample2":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				if (tabla.lookup(quad[3])==True):
					q.append(tabla.getDir(quad[3]))
				elif (tablatemp.lookup(quad[3])==True):
					q.append(tablatemp.getDir(quad[3]))
				elif (tablaP.lookup(quad[3])==True):
					q.append(tablaP.getDir(quad[3]))
				elif (tablatempP.lookup(quad[3])==True):
					q.append(tablatempP.getDir(quad[3]))
				elif (tabconst.lookup(quad[3])==True):
					q.append(tabconst.getDir(quad[3]))
				else:
					q.append(quad[3])
			else:
				for x in quad:
					#print x, a
					if (tabla.lookup(x)==True):
						q.append(tabla.getDir(x))
					elif (tablatemp.lookup(x)==True):
						q.append(tablatemp.getDir(x))
					elif (tablaP.lookup(x)==True):
						q.append(tablaP.getDir(x))
					elif (tablatempP.lookup(x)==True):
						q.append(tablatempP.getDir(x))
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