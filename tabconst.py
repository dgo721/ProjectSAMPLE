class TabConst:

	def __init__(self):
		self.offset = 100
		self.data = {}

	def add(self, key):
		self.data[key]=[self.offset]
		self.offset = self.offset + 1

	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	def getDir(self, key):
		return self.data[key][0]

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def echo(self):
		print "Constantes".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)
	
	def write(self):
		f = open('out-tabla_const', 'w')
		output = "Constantes".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print >> f, output
		print >> f, "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print >> f, str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)
		f.close()
	
	def __str__(self):
		return repr(self.data)

def tabconstante(tab_const, nombre):
	if tab_const.lookup(nombre)!=True:
		tab_const.add(nombre)
	return tab_const