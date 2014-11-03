from tabvars import TabVars
from error import senderror

class DirMods:

	def __init__(self):
		self.data = {}

	def add(self, key, params, xints, yfloats, zbools, tabvalores, quad, tints, tfloats, tbools, tabtemporales):
		self.data[key]=[params, xints, yfloats, zbools, tabvalores, quad, tints, tfloats, tbools, tabtemporales]

	def getParams(self, key):
		return self.data[key][0]

	def getParamsNum(self, key):
		lista = list()
		for i in self.data[key][0]:
			if (i == 'int'):
				lista.append(0)
			elif (i == 'float'):
				lista.append(1)
			elif (i == 'bool'):
				lista.append(2)
		return lista

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def getTable(self, key):
		return self.data[key][4]

	def getTableTemp(self, key):
		return self.data[key][9]

	def echo(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(30) + "|".ljust(5) + "No. QUAD".ljust(15) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5) + "------------------------------".ljust(30) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(30) + "|".ljust(5) + str(self.data[key][5]).ljust(15) + "|".ljust(5)
	
	def echoV(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "# INTS".ljust(10) + "|".ljust(5) + "# FLOATS".ljust(10) + "|".ljust(5) + "# BOOLS".ljust(10) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5) + str(self.data[key][2]).ljust(10) + "|".ljust(5) + str(self.data[key][3]).ljust(10) + "|".ljust(5)

	def echoT(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "# TINTS".ljust(10) + "|".ljust(5) + "# TFLOATS".ljust(10) + "|".ljust(5) + "# TBOOLS".ljust(10) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][6]).ljust(10) + "|".ljust(5) + str(self.data[key][7]).ljust(10) + "|".ljust(5) + str(self.data[key][8]).ljust(10) + "|".ljust(5)

	def write(self):
		f = open('out-dir_mods', 'w')
		print >> f, "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(25) + "|".ljust(5) + "# Var INTS".ljust(15) + "|".ljust(5) + "# Var FLOATS".ljust(15) + "|".ljust(5) + "# Var BOOLS".ljust(15) + "|".ljust(5)
		print >> f, "---------------".ljust(15) + "|".ljust(5) + "-------------------------".ljust(25) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in self.data:
			print >> f, key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(25) + "|".ljust(5) + str(self.data[key][1]).ljust(15) + "|".ljust(5) + str(self.data[key][2]).ljust(15) + "|".ljust(5) + str(self.data[key][3]).ljust(15) + "|".ljust(5)
		f.close()

	def echotables(self):
		for key in self.data:
			print "VARIABLES", key.ljust(15)
			self.data[key][4].echo()
			print "\n"

	def echotablestemp(self):
		for key in self.data:
			print "TEMPORALES", key.ljust(15)
			self.data[key][9].echo()
			print "\n"

	def __str__(self):
		return repr(self.data)

def dirmod(dir_modulos, nombre, params, conti, contf, contb, tab_valores, quad, tempi, tempf, tempb, tab_temporales, linea):
	if dir_modulos.lookup(nombre)!=True and tab_valores.lookup(nombre)!=True:
		dir_modulos.add(nombre, params, conti, contf, contb, tab_valores, quad, tempi, tempf, tempb, tab_temporales)
	else:
		senderror(11, linea, nombre)
	return dir_modulos