class DirMods:

	def __init__(self):
		self.data = {}

	def add(self, key, params, xints, yfloats):
		self.data[key]=[params, xints, yfloats]

	def getType(self, key):
		return self.data[key][0]

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def echo(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(15) + "|".ljust(5) + "# Var INTS".ljust(15) + "|".ljust(5) + "# Var FLOATS".ljust(15)
		print "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(15) + "|".ljust(5) + str(self.data[key][1]).ljust(15) + "|".ljust(5) + str(self.data[key][2]).ljust(15)
	
	def __str__(self):
		return repr(self.data)

def dirmod(dir_modulos, nombre, params, conti, contf, tab_valores):
	if dir_modulos.lookup(nombre)!=True and tab_valores.lookup(nombre)!=True:
		dir_modulos.add(nombre, params, conti, contf)
	else:
		print "EXISTS, module not added"
	return dir_modulos