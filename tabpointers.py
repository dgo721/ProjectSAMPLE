class TabPointer:

	#Inicializa clase TabPointer
	def __init__(self, dirp):
		self.offsdirp = dirp
		self.data = {}

	#Aniade un nuevo indice de apuntador con su respectiva direccion
	def add(self, key):
		self.data[key]=[self.offsdirp]
		self.offsdirp = self.offsdirp + 1 #Aumenta la direccion en uno para el proximo indice a asignar

	#Obtiene la direccion del apuntador
	def getDir(self, key):
		for llave in self.data:
			if (llave==key):
				return self.data[key][0]
		return -1

	#Verifica si se encuentra una variable apuntador
	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	#Salida en pantalla de tabla de apuntadores
	def echo(self):
		print "Apuntador".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)

	def __str__(self):
		return repr(self.data)