class DirMods:

	def __init__(self):
		self.data = {}

	def add(self, key, params, xints, yfloats, zbools):
		self.data[key]=[params, xints, yfloats, zbools]

	def getParams(self, key):
		return self.data[key][0]

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def echo(self):
		print "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(20) + "|".ljust(5) + "# Var INTS".ljust(15) + "|".ljust(5) + "# Var FLOATS".ljust(15) + "|".ljust(5) + "# Var BOOLS".ljust(15) + "|".ljust(5)
		print "---------------".ljust(15) + "|".ljust(5) + "--------------------".ljust(20) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(20) + "|".ljust(5) + str(self.data[key][1]).ljust(15) + "|".ljust(5) + str(self.data[key][2]).ljust(15) + "|".ljust(5) + str(self.data[key][3]).ljust(15) + "|".ljust(5)
	
	def write(self):
		f = open('out-dir_mods', 'w')
		print >> f, "Modulos".ljust(15) + "|".ljust(5) + "Parametros".ljust(25) + "|".ljust(5) + "# Var INTS".ljust(15) + "|".ljust(5) + "# Var FLOATS".ljust(15) + "|".ljust(5) + "# Var BOOLS".ljust(15) + "|".ljust(5)
		print >> f, "---------------".ljust(15) + "|".ljust(5) + "-------------------------".ljust(25) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5) + "---------------".ljust(15) + "|".ljust(5)
		for key in sorted(self.data):
			print >> f, key.ljust(15) + "|".ljust(5) + str(self.data[key][0]).ljust(25) + "|".ljust(5) + str(self.data[key][1]).ljust(15) + "|".ljust(5) + str(self.data[key][2]).ljust(15) + "|".ljust(5) + str(self.data[key][3]).ljust(15) + "|".ljust(5)
		f.close()

	def __str__(self):
		return repr(self.data)

def dirmod(dir_modulos, nombre, params, conti, contf, contb, tab_valores):
	if dir_modulos.lookup(nombre)!=True and tab_valores.lookup(nombre)!=True:
		dir_modulos.add(nombre, params, conti, contf, contb)
	else:
		print "EXISTS, module not added"
	return dir_modulos