from error import senderror
from tabvars import TabVars
from tabpointers import TabPointer

class DirMods:

	#Inicializa clase DirMods
	def __init__(self):
		self.data = {}

	#Aniade nuevo indice / nombre de modulo, incluyendo tipo, cuadruplo, parametros, contadores de variables, contadores de temporales, tablas de variables, tablas de temporales y tablas de apuntadores
	def add(self, key, params, xints, yfloats, zbools, tabvalores, quad, tints, tfloats, tbools, tpoints, tabtemporales, tabpointers, tipo):
		self.data[key]=[params, xints, yfloats, zbools, tabvalores, quad, tints, tfloats, tbools, tpoints, tabtemporales, tabpointers, tipo]

	#Regresa la lista de parametros del modulo
	def getParams(self, key):
		return self.data[key][0]

	#Regresa la secuencia de parametros
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

	#Verifica si un modulo existe en el metodo
	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def remove(self, key):
		self.data.pop(key)

	#Regresa la tabla de variables del modulo
	def getTable(self, key):
		return self.data[key][4]

	#Regresa la tabla de temporales del modulo
	def getTableTemp(self, key):
		return self.data[key][10]

	#Regresa la tabla de apuntadores del modulo
	def getTablePoint(self, key):
		return self.data[key][11]

	#Regresa el tipo de retorno
	def getType(self, key):
		return self.data[key][12]

	#Impresion en pantalla de parametros y cuadruplo
	def echo(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(30) + "|".ljust(5) + "No. QUAD".ljust(15) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5) + "------------------------------".ljust(30) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(30) + "|".ljust(5) + str(self.data[key][5]).ljust(15) + "|".ljust(5)
	
	#Impresion en pantalla de variables en el modulo
	def echoV(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "# INTS".ljust(10) + "|".ljust(5) + "# FLOATS".ljust(10) + "|".ljust(5) + "# BOOLS".ljust(10) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5) + str(self.data[key][2]).ljust(10) + "|".ljust(5) + str(self.data[key][3]).ljust(10) + "|".ljust(5)

	#Impresion en pantalla de temporales en el modulo
	def echoT(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "# TINTS".ljust(10) + "|".ljust(5) + "# TFLOATS".ljust(10) + "|".ljust(5) + "# TBOOLS".ljust(10) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][6]).ljust(10) + "|".ljust(5) + str(self.data[key][7]).ljust(10) + "|".ljust(5) + str(self.data[key][8]).ljust(10) + "|".ljust(5)

	#Impresion en pantalla de apuntadores en el modulo
	def echoP(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "# TPOINTERS".ljust(10) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][9]).ljust(10) + "|".ljust(5)

	def write(self):
		f = open('out-dir_mods', 'w')
		print >> f, "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(25) + "|".ljust(5) + "# Var INTS".ljust(15) + "|".ljust(5) + "# Var FLOATS".ljust(15) + "|".ljust(5) + "# Var BOOLS".ljust(15) + "|".ljust(5)
		print >> f, "---------------".ljust(15) + "|".ljust(5) + "-------------------------".ljust(25) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in self.data:
			print >> f, key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(25) + "|".ljust(5) + str(self.data[key][1]).ljust(15) + "|".ljust(5) + str(self.data[key][2]).ljust(15) + "|".ljust(5) + str(self.data[key][3]).ljust(15) + "|".ljust(5)
		f.close()

	#Se almacena directorio de modulos en el archivo objeto
	def writeQ(self):
		f = open('sample.smo', 'w')
		for key in self.data:
			print >> f, key + "|" + str(self.data[key][0]) + "|" + str(self.data[key][1]) + "|" + str(self.data[key][2]) + "|" + str(self.data[key][3]) + "|" + str(self.data[key][5]) + "|" + str(self.data[key][6]) + "|" + str(self.data[key][7]) + "|" + str(self.data[key][8]) + "|" + str(self.data[key][9]) + "|" + str(self.data[key][12])
		print >> f, "%%%%"
		f.close()

	def echotables(self):
		for key in self.data:
			print "VARIABLES", key.ljust(15)
			self.data[key][4].echo()
			print "\n"

	def echotablestemp(self):
		for key in self.data:
			print "TEMPORALES", key.ljust(15)
			self.data[key][10].echo()
			print "\n"

	def echotablespoint(self):
		for key in self.data:
			print "APUNTADORES", key.ljust(15)
			self.data[key][11].echo()
			print "\n"

	def __str__(self):
		return repr(self.data)

#Se aniade un nuevo directorio de modulos
def dirmod(dir_modulos, nombre, params, conti, contf, contb, tab_valores, quad, tempi, tempf, tempb, tpoints, tab_temporales, tab_pointer, tipo, linea):
	if dir_modulos.lookup(nombre)!=True and tab_valores.lookup(nombre)!=True:
		dir_modulos.add(nombre, params, conti, contf, contb, tab_valores, quad, tempi, tempf, tempb, tpoints, tab_temporales, tab_pointer, tipo)
	else:
		senderror(11, linea, nombre)
	return dir_modulos

#Se almacena directorio de modulos de forma temporal, usado en la declaracion de modulos como variables globales
def tempdirmod(dir_modulos, nombre, params):
	if dir_modulos.lookup(nombre)!=True:
		dir_modulos.add(nombre, params, None, None, None, None, None, None, None, None, None, None, None, None)
	else:
		senderror(11, linea, nombre)
	return dir_modulos

#Remueve el modulo temporal
def removedirmod(dir_modulos, nombre):
	dir_modulos.remove(nombre)
	return dir_modulos