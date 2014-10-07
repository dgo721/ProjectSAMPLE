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
		print "Variable".ljust(10) + "|".ljust(5) + "Tipo".ljust(10)
		for key in sorted(self.data):
			if (self.data[key][0]==0):
				print key.ljust(10) + "|".ljust(5) + "INT".ljust(10)
			elif (self.data[key][0]==1):
				print key.ljust(10) + "|".ljust(5) + "FLOAT".ljust(10)
	
	def __str__(self):
		return repr(self.data)