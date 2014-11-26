class TabConst:

	#Inicializa clase TabConst
	def __init__(self):
		self.offset = 100
		self.data = {}

	#Aniade nuevo indice de constante
	def add(self, key):
		self.data[key]=[self.offset]
		self.offset = self.offset + 1 #Aumenta en 1 a la direccion a almacenar

	#Obtiene valor de constante
	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	#Obtiene direccion de constante
	def getDir(self, key):
		return self.data[key][0]

	#Verifica si la constante ya existe en la tabla
	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	#Impresion en pantalla de la tabla
	def echo(self):
		print "Constantes".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)
	
	#Impresion en archivo de la tabla
	def write(self):
		f = open('out-tabla_const', 'w')
		output = "Constantes".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print >> f, output
		print >> f, "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			print >> f, str(key).ljust(10) + "|".ljust(5) + str(self.data[key][0]).ljust(10) + "|".ljust(5)
		f.close()

	#Se almacena la tabla de constantes en el archivo objeto
	def writeQ(self):
		f = open('sample.smo', 'a')
		for key in self.data:
			print >> f, str(key) + "|" + str(self.data[key][0])
		print >> f, "%%%%"
		f.close()
	
	def __str__(self):
		return repr(self.data)

#Aniade nueva constante a tabla
def tabconstante(tab_const, nombre):
	if tab_const.lookup(nombre)!=True:
		tab_const.add(nombre)
	return tab_const