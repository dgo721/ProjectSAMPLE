class TabVars:

	def __init__(self):
		self.data = {}

	def add(self, key, value):
		self.data[key]=[value]

	def lookup(self, key):
		for llave in self.data:
			if (llave==key):
				return True
		return False

	def __str__(self):
		return repr(self.data)

def vartipo(tipo, previo):
	if (previo!=1):
		previo=tipo
	return previo

def tabvar(nombre,tipo):
	if tab_valores.lookup(nombre)!=True:
		tab_valores.add(nombre, tipo)
	else:
		print "EXISTS"