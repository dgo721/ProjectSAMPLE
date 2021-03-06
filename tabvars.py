from error import senderror

class TabVars:

	#Inicializa clase TabVars
	def __init__(self, dirint, dirfloat, dirbool):
		self.offsint = dirint
		self.offsflo = dirfloat
		self.offsbol = dirbool
		self.data = {}

	#Aniade nuevo indice de variable, incluyendo su tipo de dato.
	def add(self, key, value, numdim):
		if value == 0:
			self.data.update({key:[value, self.offsint]})
			if numdim == 0:
				self.offsint = self.offsint + 1 #El indice del tipo entero se incrementa en 1.
			else:
				self.offsint = self.offsint + numdim #El indice del tipo entero se incrementa en el numero que cuenta el valor dimensionado.
		elif value == 1:
			self.data.update({key:[value, self.offsflo]})
			if numdim == 0:
				self.offsflo = self.offsflo + 1 #El indice del tipo flotante se incrementa en 1.
			else:
				self.offsflo = self.offsflo + numdim #El indice del tipo flotante se incrementa en el numero que cuenta el valor dimensionado.
		elif value == 2:
			self.data.update({key:[value, self.offsbol]})
			if numdim == 0:
				self.offsbol = self.offsbol + 1 #El indice del tipo booleano se incrementa en 1.
			else:
				self.offsbol = self.offsbol + numdim #El indice del tipo booleano se incrementa en el numero que cuenta el valor dimensionado.

	#Obtiene valor de variable
	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	#Obtiene tipo de variable
	def getType(self, key):
		return self.data[key][0]

	#Obtiene direccion de variable
	def getDir(self, key):
		return self.data[key][1]

	#Verifica si la veriable existe en la tabla
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
		for key in self.data:
			if (self.data[key][1] == limit):
				llave = key
				break
		self.data.pop(llave)

	#Impresion en pantalla de tabla de variables
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
	
	#Impresion en archivo de tabla de variables
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

#Inverso al metodo vartipo_mod, devuelve el formato string de un tipo de dato.
def invartipo_mod(tipo):
	if (tipo==0):
		return "INT"
	elif (tipo==1):
		return "FLOAT"
	elif (tipo==2):
		return "BOOL"

#Recibe la tabla y el nuevo par (nombre-tipo) para aniadir a la tabla, solo seran agregados
#si el par no existe previamente
def tabvar(tab_valores, nombre, tipo, numdim, linea):
	if tab_valores.lookup(nombre)!=True:
		tab_valores.add(nombre, tipo, numdim)
	else:
		if tab_valores.getType(nombre) != tipo:
			#print "TABVAR--", tab_valores.getType(nombre), tipo
			senderror(6, linea, nombre, invartipo_mod(tab_valores.getType(nombre)))
	return tab_valores

#Busca un ID dentro de la lista de variables acumuladas.
def buscaID(lista, idv):
	x = 1
	for l in lista:
		if lista[-x][0] == idv:
			return lista[-x][1]
		x = x + 1
	return -1

#Busca un ID dublicado dentro de la lista de variables acumuladas.
def isduplicate(lista, par, contvars):
	x = 1
	while x < contvars:
		if lista[-x][0] == par[0]:
			return 1
		x = x + 1
	return 0

def offsetVars(lista):
	offset = 0
	i = 0
	for x in lista:
		if lista[i][2] != 0:
			offset = offset + (lista[i][2]-1)
		i += 1
	return offset