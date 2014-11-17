class TabDims:

	def __init__(self):
		self.data = {}

	def add(self, key, dim, limit1, limit2):
		self.data[key]=[dim, limit1, limit2]

	def isDuplicate(self, key):
		for llave in self.data:
			if (llave==key):
				return self.data[llave][0]
		return -1

	def getDim(self, key):
		for llave in self.data:
			if (llave==key):
				return self.data[key][0]
		return -1

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def getLimit1(self, key):
		return self.data[key][1]

	def getLimit2(self, key):
		return self.data[key][2]

	def __str__(self):
		return repr(self.data)