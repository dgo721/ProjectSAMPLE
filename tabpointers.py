class TabPointer:

	def __init__(self, dirp):
		self.offsdirp = dirp
		self.data = {}

	def add(self, key):
		self.data[key]=[self.offsdirp]
		self.offsdirp = self.offsdirp + 1

	def getDir(self, key):
		for llave in self.data:
			if (llave==key):
				return self.data[key][0]
		return -1

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def echo(self):
		print "Apuntador".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)

	def __str__(self):
		return repr(self.data)