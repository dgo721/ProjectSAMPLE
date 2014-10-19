class TabVars:

	def __init__(self, dirint, dirfloat, dirbool):
		self.offsint = dirint
		self.offsflo = dirfloat
		self.offsbol = dirbool
		self.data = {}

	def add(self, key, value):
		if value == 0:
			self.data.update({key:[value, self.offsint]})
			self.offsint = self.offsint + 1
		elif value == 1:
			self.data.update({key:[value, self.offsflo]})
			self.offsflo = self.offsflo + 1
		elif value == 2:
			self.data.update({key:[value, self.offsbol]})
			self.offsbol = self.offsbol + 1

	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	def getType(self, key):
		return self.data[key][0]

	def getDir(self, key):
		return self.data[key][1]

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def empty(self):
		self.data = {}

	def removelastKeyDir(self, pair):
		if pair[1] == 0:
			limit = self.offsint - 1
			self.offsint = self.offsint - 1
		elif pair[1] == 1:
			limit = self.offsflo - 1
			self.offsflo = self.offsflo - 1
		elif pair[1] == 2:
			limit = self.offsbol - 1
			self.offsbol = self.offsbol - 1
		print "LIMIT--------", limit
		for key in self.data:
			if (self.data[key][1] == limit):
				llave = key
				print "LA LLAVE", llave
				break
		print "IM OUT"

	
	def echo(self):
		print "Variables".ljust(10) + "|".ljust(5) + "Tipo".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in self.data:
			if (self.data[key][0]==0):
				print key.ljust(10) + "|".ljust(5) + "INT".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
			elif (self.data[key][0]==1):
				print key.ljust(10) + "|".ljust(5) + "FLOAT".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
			elif (self.data[key][0]==2):
				print key.ljust(10) + "|".ljust(5) + "BOOL".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
	
	def write(self):
		f = open('out-tabla_vars', 'w')
		output = "Variables".ljust(10) + "|".ljust(5) + "Tipo".ljust(10) + "|".ljust(5) + "Direccion".ljust(10) + "|".ljust(5)
		print >> f, output
		print >> f, "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5) + "----------".ljust(10) + "|".ljust(5)
		for key in sorted(self.data):
			if (self.data[key][0]==0):
				print >> f, key.ljust(10) + "|".ljust(5) + "INT".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
			elif (self.data[key][0]==1):
				print >> f, key.ljust(10) + "|".ljust(5) + "FLOAT".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
			elif (self.data[key][0]==2):
				print >> f, key.ljust(10) + "|".ljust(5) + "BOOL".ljust(10) + "|".ljust(5) + str(self.data[key][1]).ljust(10) + "|".ljust(5)
		f.close()
	
	def __str__(self):
		return repr(self.data)

#Usado en ASSIGN, determina si en una asignacion de multiples valores, se llega a un
#float o int. Encontrando un float, hace toda la operacion como float.
def vartipo_assign(varlista):
	index = 0
	while (varlista!=[]):
		compara=varlista.pop(0)
		
		if compara==2:
			index = 2
		elif compara==1 and index<2:
			index = 1
		elif compara==0 and index<1:
			index = 0
	return index

#Usado en VAR_CTE para ASSIGN, determina el tipo de un ID ya registrado en la tabla.
def tipoID(tab_valores, nombre):
	if tab_valores.lookup(nombre)==True:
		tipo = tab_valores.getType(nombre)
		return tipo
	return -1

#Usado en VARS, verifica el tipo de dato recibido, retorna su valor entero.
def vartipo_mod(tipo):
	if (tipo=="int"):
		return 0
	elif (tipo=="float"):
		return 1
	elif (tipo=="bool"):
		return 2

#Recibe la tabla y el nuevo par (nombre-tipo) para aniadir a la tabla, solo seran agregados
#si el par no existe previamente
def tabvar(tab_valores, nombre, tipo):
	if tab_valores.lookup(nombre)!=True:
		tab_valores.add(nombre, tipo)
	else:
		print "EXISTS, var not added"
	return tab_valores