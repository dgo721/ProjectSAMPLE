class TabDims:

	#Inicializa clase TabDims
	def __init__(self):
		self.data = {}

	#Aniade nuevo indice de variable dimensionada, incluyendo no. de dimensiones, limite 1, limite 2
	def add(self, key, dim, limit1, limit2):
		self.data[key]=[dim, limit1, limit2]

	#Revisa si el variable ya se encuentra dentro de las variables dimensionadas.
	def isDuplicate(self, key):
		for llave in self.data:
			if (llave==key):
				return self.data[llave][0]
		return -1

	#Obtiene el valor sobre cuantas dimensiones representa la variable
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

	#Obtiene el valor del primer limite
	def getLimit1(self, key):
		return self.data[key][1]

	#Obtiene el valor del segundo limite
	def getLimit2(self, key):
		return self.data[key][2]

	def __str__(self):
		return repr(self.data)