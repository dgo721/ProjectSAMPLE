from dirmods import DirMods
from tabvars import TabVars, tabvar
from tabdims import TabDims
from tabpointers import TabPointer

class CodeGen:

	#Valores de inicializacion de clase
	def __init__(self):
		self.x = 1
		self.t = 1
		self.a = 1
		self.data = {}
		self.pilaSaltos = []
		self.scope = "*work*"

	#Aniade un nuevo cuadruplo con un respectivo temporal
	def add(self, op, oper1, oper2, asigna):
		if oper2 != -1:
			stmp=str(self.t)
			tmp='_t' + stmp
			self.data[self.x]=[op, oper1, oper2, tmp, self.scope]
			self.x=self.x+1 #Incrementa al indice de cuadruplo siguiente a guardar.
			self.t=self.t+1 #Incrementa al indice de temporal siguiente a guardar.
		else:
			self.data[self.x]=[op, oper1, oper2, asigna, self.scope]
			self.x=self.x+1

	#Aniade un nuevo cuadruplo
	def addQ(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
		self.x=self.x+1

	#Aniade un nuevo cuadruplo de salto
	def addGoTo(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
		self.pilaSaltos.append(self.x)
		self.x=self.x+1

	#Aniade un nuevo cuadruplo de salto al bloque ELSE
	def addGoToE(self, op, oper1, oper2, oper3):
		self.data[self.x]=[op, oper1, oper2, oper3, self.scope]
		quadro = self.pilaSaltos.pop()
		self.pilaSaltos.append(self.x)
		self.x=self.x+1
		self.data[quadro][3] = self.x

	#Aniade el numero de cuadruplo a una instruccion previa de salto
	def addcontinueG(self):
		quadro = self.pilaSaltos.pop()
		self.data[quadro][3] = self.x

	#Genera el cuadruplo de retorno a WHILE y aniade el numero de cuadruplo a la instruccion previa de salto en Falso
	def addcontinueW(self):
		salida = self.pilaSaltos.pop() #Obtiene numero de cuadruplo almacenado de salto previo al ciclo
		retorno = self.pilaSaltos.pop() #Obtiene numero de cuadruplo donde comienza el ciclo
		self.data[self.x]=['goTo', -1, -1, retorno, self.scope]
		self.x=self.x+1
		self.data[salida][3] = self.x

	#Genera cuadruplos de repeticiones en REPEAT
	def addcontinueR(self, cte, tabtemp, linenumber):
		temporal = self.pilaSaltos.pop() #Obtiene el temporal almacenado, equivalente al numero de repeticiones al momento.
		regreso = self.pilaSaltos.pop() #Obtiene numero de cuadruplo donde comienza el ciclo
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['+', temporal, 1, tmp, self.scope] #Se suma una unidad al temporal de inicio.
		tabtemp=tabvar(tabtemp, tmp, 0, 0, linenumber) #Aniade el temporal a la tabla de valores temporales
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['=', tmp, -1, temporal, self.scope] #Se actualiza el valor de temporal.
		self.x=self.x+1
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['==', temporal, cte, tmp, self.scope] #Se compara con la constante entera que indica el numero de repeticiones.
		tabtemp=tabvar(tabtemp, tmp, 2, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['goToF', tmp, -1, regreso, self.scope] #Se genera el cuadruplo de salto en falso
		self.x=self.x+1
		return tabtemp

	#Almacena el cuadruplo donde comienza el ciclo de estatutos del WHILE
	def addGoToW(self):
		self.pilaSaltos.append(self.x)

	#Almacena el cuadruplo donde comienza el ciclo de estatutos del REPEAT, generando un respectivo temporal de control
	def addGoToR(self, tabtemp, linenumber):
		stmp=str(self.t)
		tmp='_t' + stmp
		self.data[self.x]=['=', 0, -1, tmp, self.scope] #Se inicializa el temporal de control en 0
		tabtemp=tabvar(tabtemp, tmp, 0, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.pilaSaltos.append(self.x) #Se almaena el cuadruplo de inicio de repeticion
		self.pilaSaltos.append(tmp) #Se almacena el temporal de control
		return tabtemp

	#Establece los cuadruplos para indexacion de arreglos
	def addVer1(self, oper, iden, limite1, tabpointer):
		self.data[self.x]=['ver', oper, -1, limite1, self.scope] #Genera el cuadruplo de verificacion de dimension 1
		self.x=self.x+1
		stmp=str(self.a)
		tmp='_a' + stmp
		self.data[self.x]=['+dir', oper, iden, tmp, self.scope] #Genera el cuadruplo de acceso a la direccion base.
		tabpointer.add(tmp) #Aniade el apuntador a la tabla de apuntadores
		self.x=self.x+1
		self.a=self.a+1 #Incrementa el indice del siguiente apuntador a direccion base.
		return [tabpointer, tmp]

	#Establece los cuadruplos para indexacion de matrices
	def addVer2(self, oper1, oper2, iden, limite1, limite2, tabpointer, tabtemp, linenumber):
		self.data[self.x]=['ver', oper1, -1, limite1, self.scope] #Genera el cuadruplo de verificacion de dimension 1
		self.x=self.x+1
		stmp=str(self.t)
		tmp1='_t' + stmp
		self.data[self.x]=['*', oper1, limite1, tmp1, self.scope] #Genera el cuadruplo de multiplicacion por limite1, ubica el renglon de matriz
		tabtemp=tabvar(tabtemp, tmp1, 0, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		self.data[self.x]=['ver', oper2, -1, limite2, self.scope] #Genera el cuadruplo de verificacion de dimension 2
		self.x=self.x+1
		stmp=str(self.t)
		tmp2='_t' + stmp
		self.data[self.x]=['+', tmp1, oper2, tmp2, self.scope] #Genera el cuadruplo de suma con limite2, ubica la columna de matriz
		tabtemp=tabvar(tabtemp, tmp2, 0, 0, linenumber)
		self.x=self.x+1
		self.t=self.t+1
		stmp=str(self.a)
		tmp3='_a' + stmp
		self.data[self.x]=['+dir', tmp2, iden, tmp3, self.scope] #Genera el cuadruplo de acceso a la direccion base.
		tabpointer.add(tmp3) #Aniade el apuntador a la tabla de apuntadores
		self.x=self.x+1
		self.a=self.a+1 #Incrementa el indice del siguiente apuntador a direccion base.
		return [tabpointer, tabtemp, tmp3]

	#Regresa el indice de un cuadruplo
	def getKey(self, key):
		for llave in self.data:
			if (llave==key):
				return key
		return None

	#Regresa un cuadruplo dado un indice
	def getQuad(self, key):
		return self.data[key]

	#Regresa el valor del ultimo cuadruplo asignado.
	def getX(self):
		return self.x - 1

	#Regresa el valor del cuadruplo proximo a asignar.
	def getnextX(self):
		return self.x

	#Regresa el temporal proximo a asignar.
	def gettemp(self):
		ltemp=self.t
		stmp=str(ltemp)
		tmp='_t' + stmp
		return tmp

	#Regresa el ultimo temporal asignado.
	def lasttemp(self):
		ltemp=self.t-1
		stmp=str(ltemp)
		tmp='_t' + stmp
		return tmp

	#Regresa el scope en el que se trabajan los cuadruplos
	def getScope(self):
		return self.scope

	#Establece el scope en el que se trabajaran los cuadruplos
	def setScope(self, name):
		self.scope = name

	def empty(self):
		self.x = 1
		self.t = 1
		self.data = {}

	#Salida en pantalla de los cuadruplos
	def echo(self):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4) + "SCOPE".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4) + str(self.data[key][4]).ljust(4) + "|".ljust(4)

	#Salida en texto de los cuadruplos
	def write(self):
		f = open('out-quads', 'w')
		print >> f, "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print >> f, "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		for key in sorted(self.data):
			print >> f, str(key).rjust(4) + "|".ljust(4) + str(self.data[key][0]).ljust(4) + "|".ljust(4) + str(self.data[key][1]).ljust(4) + "|".ljust(4) + str(self.data[key][2]).ljust(4) + "|".ljust(4) + str(self.data[key][3]).ljust(4) + "|".ljust(4)
		f.close()

	def echoQ(self, dirmod, tabconst):
		print "QUAD".ljust(4) + "|".ljust(4) + "OP".ljust(4) + "|".ljust(4) + "OPR1".ljust(4) + "|".ljust(4) + "OPR2".ljust(4) + "|".ljust(4) + "TEMP".ljust(4) + "|".ljust(4)
		print "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4) + "----".ljust(4) + "|".ljust(4)
		tablaP = dirmod.getTable("*work*")
		tablatempP = dirmod.getTableTemp("*work*")
		for a in self.data:
			quad = self.getQuad(a)
			scope = quad[4]
			tabla = dirmod.getTable(scope)
			tablatemp = dirmod.getTableTemp(scope)
			q = list()
			i = 0
			if quad[0] == "goTo" or quad[0] == "ret" or quad[0] == "era" or quad[0] == "gosub":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "goToF" or quad[0] == "param" or quad[0] == "sample1":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True):
					q.append(tabla.getDir(quad[1]))
				elif (tablatemp.lookup(quad[1])==True):
					q.append(tablatemp.getDir(quad[1]))
				elif (tablaP.lookup(quad[1])==True):
					q.append(tablaP.getDir(quad[1]))
				elif (tablatempP.lookup(quad[1])==True):
					q.append(tablatempP.getDir(quad[1]))
				elif (tabconst.lookup(quad[1])==True):
					q.append(tabconst.getDir(quad[1]))
				else:
					q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "sample2":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				if (tabla.lookup(quad[3])==True):
					q.append(tabla.getDir(quad[3]))
				elif (tablatemp.lookup(quad[3])==True):
					q.append(tablatemp.getDir(quad[3]))
				elif (tablaP.lookup(quad[3])==True):
					q.append(tablaP.getDir(quad[3]))
				elif (tablatempP.lookup(quad[3])==True):
					q.append(tablatempP.getDir(quad[3]))
				elif (tabconst.lookup(quad[3])==True):
					q.append(tabconst.getDir(quad[3]))
				else:
					q.append(quad[3])
			else:
				for x in quad:
					#print x, a
					if (tabla.lookup(x)==True):
						q.append(tabla.getDir(x))
					elif (tablatemp.lookup(x)==True):
						q.append(tablatemp.getDir(x))
					elif (tablaP.lookup(x)==True):
						q.append(tablaP.getDir(x))
					elif (tablatempP.lookup(x)==True):
						q.append(tablatempP.getDir(x))
					elif (tabconst.lookup(x)==True):
						q.append(tabconst.getDir(x))
					else:
						q.append(quad[i])
					i = i + 1
			print str(a).rjust(4) + "|".ljust(4) + str(q[0]).ljust(4) + "|".ljust(4) + str(q[1]).ljust(4) + "|".ljust(4) + str(q[2]).ljust(4) + "|".ljust(4) + str(q[3]).ljust(4) + "|".ljust(4)

	#Metodo de traduccion de cuadruplos al archivo objeto, asignando las variables encontradas en direcciones
	def writeQ(self, dirmod, tabconst):
		f = open('sample.smo', 'a') #Abre el archivo objeto, ubicandose en la ultima linea
		tablaP = dirmod.getTable("*work*") #Pide la tabla de variables globales
		tablatempP = dirmod.getTableTemp("*work*") #Pide la tabla de temporales globales
		tablapointP = dirmod.getTablePoint("*work*") #Pide la tabla de apuntadores globales
		for a in self.data:
			quad = self.getQuad(a) #Obtiene cuadruplo
			scope = quad[4] #Obtiene alcance / scope de cuadruplo
			tabla = dirmod.getTable(scope) #Obtiene la tabla de variables locales del metodo establecido en el scope
			tablatemp = dirmod.getTableTemp(scope) #Obtiene la tabla de temporales locales del metodo establecido en el scope
			tablapoint = dirmod.getTablePoint(scope) #Obtiene la tabla de variables locales del metodo establecido en el scope
			q = list() #Inicializa lista
			i = 0
			if quad[0] == "goTo" or quad[0] == "ret" or quad[0] == "era" or quad[0] == "gosub":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "goToF" or quad[0] == "param" or quad[0] == "sample1" or quad[0] == "ver":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True): #Busca direccion en tabla de variables locales
					q.append(tabla.getDir(quad[1]))
				elif (tablatemp.lookup(quad[1])==True): #Busca direccion en tabla de temporales locales
					q.append(tablatemp.getDir(quad[1]))
				elif (tablapoint.lookup(quad[1])==True): #Busca direccion en tabla de apuntadores locales
					q.append(tablapoint.getDir(quad[1]))
				elif (tablaP.lookup(quad[1])==True): #Busca direccion en tabla de variables globales
					q.append(tablaP.getDir(quad[1]))
				elif (tablatempP.lookup(quad[1])==True): #Busca direccion en tabla de temporales globales
					q.append(tablatempP.getDir(quad[1]))
				elif (tablapointP.lookup(quad[1])==True): #Busca direccion en tabla de apuntadores globales
					q.append(tablapointP.getDir(quad[1]))
				elif (tabconst.lookup(quad[1])==True): #Busca direccion en tabla de contantes
					q.append(tabconst.getDir(quad[1]))
				else:
					q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			elif quad[0] == "+dir":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True):
					q.append(tabla.getDir(quad[1])) #Asigna direccion de tabla de variables locales
				elif (tablatemp.lookup(quad[1])==True):
					q.append(tablatemp.getDir(quad[1])) #Asigna direccion de tabla de temporales locales
				elif (tablapoint.lookup(quad[1])==True):
					q.append(tablapoint.getDir(quad[1])) #Asigna direccion de tabla de apuntadores locales
				elif (tablaP.lookup(quad[1])==True):
					q.append(tablaP.getDir(quad[1])) #Asigna direccion de tabla de variables globales
				elif (tablatempP.lookup(quad[1])==True):
					q.append(tablatempP.getDir(quad[1])) #Asigna direccion de tabla de temporales globales
				elif (tablapointP.lookup(quad[1])==True):
					q.append(tablapointP.getDir(quad[1])) #Asigna direccion de tabla de apuntadores globales
				elif (tabconst.lookup(quad[1])==True):
					q.append(tabconst.getDir(quad[1])) #Asigna direccion de tabla de constantes
				else:
					q.append(quad[1])
				if (tabla.lookup(quad[2])==True):
					q.append(tabla.getDir(quad[2]))
				elif (tablaP.lookup(quad[2])==True):
					q.append(tablaP.getDir(quad[2]))
				if (tablapoint.lookup(quad[3])==True):
					q.append(tablapoint.getDir(quad[3]))
				elif (tablapointP.lookup(quad[3])==True):
					q.append(tablapointP.getDir(quad[3]))
			elif quad[0] == "sample2" or quad[0] == "input":
				q.append(quad[0])
				q.append(quad[1])
				q.append(quad[2])
				if (tabla.lookup(quad[3])==True):
					q.append(tabla.getDir(quad[3]))
				elif (tablatemp.lookup(quad[3])==True):
					q.append(tablatemp.getDir(quad[3]))
				elif (tablapoint.lookup(quad[3])==True):
					q.append(tablapoint.getDir(quad[3]))
				elif (tablaP.lookup(quad[3])==True):
					q.append(tablaP.getDir(quad[3]))
				elif (tablatempP.lookup(quad[3])==True):
					q.append(tablatempP.getDir(quad[3]))
				elif (tablapointP.lookup(quad[3])==True):
					q.append(tablapointP.getDir(quad[3]))
				elif (tabconst.lookup(quad[3])==True):
					q.append(tabconst.getDir(quad[3]))
				else:
					q.append(quad[3])
			elif quad[0] == "random":
				q.append(quad[0])
				q.append(quad[1])
				if (tabla.lookup(quad[2])==True):
					q.append(tabla.getDir(quad[2]))
				elif (tablatemp.lookup(quad[2])==True):
					q.append(tablatemp.getDir(quad[2]))
				elif (tablapoint.lookup(quad[2])==True):
					q.append(tablapoint.getDir(quad[2]))
				elif (tablaP.lookup(quad[2])==True):
					q.append(tablaP.getDir(quad[2]))
				elif (tablatempP.lookup(quad[2])==True):
					q.append(tablatempP.getDir(quad[2]))
				elif (tablapointP.lookup(quad[2])==True):
					q.append(tablapointP.getDir(quad[2]))
				elif (tabconst.lookup(quad[2])==True):
					q.append(tabconst.getDir(quad[2]))
				else:
					q.append(quad[2])
				if (tabla.lookup(quad[3])==True):
					q.append(tabla.getDir(quad[3]))
				elif (tablatemp.lookup(quad[3])==True):
					q.append(tablatemp.getDir(quad[3]))
				elif (tablapoint.lookup(quad[3])==True):
					q.append(tablapoint.getDir(quad[3]))
				elif (tablaP.lookup(quad[3])==True):
					q.append(tablaP.getDir(quad[3]))
				elif (tablatempP.lookup(quad[3])==True):
					q.append(tablatempP.getDir(quad[3]))
				elif (tablapointP.lookup(quad[3])==True):
					q.append(tablapointP.getDir(quad[3]))
				elif (tabconst.lookup(quad[3])==True):
					q.append(tabconst.getDir(quad[3]))
				else:
					q.append(quad[3])
			elif quad[0] == "arr" or quad[0] == "mat":
				q.append(quad[0])
				if (tabla.lookup(quad[1])==True):
					q.append(tabla.getDir(quad[1]))
				elif (tablatemp.lookup(quad[1])==True):
					q.append(tablatemp.getDir(quad[1]))
				elif (tablapoint.lookup(quad[1])==True):
					q.append(tablapoint.getDir(quad[1]))
				elif (tablaP.lookup(quad[1])==True):
					q.append(tablaP.getDir(quad[1]))
				elif (tablatempP.lookup(quad[1])==True):
					q.append(tablatempP.getDir(quad[1]))
				elif (tablapointP.lookup(quad[1])==True):
					q.append(tablapointP.getDir(quad[1]))
				elif (tabconst.lookup(quad[1])==True):
					q.append(tabconst.getDir(quad[1]))
				else:
					q.append(quad[1])
				q.append(quad[2])
				q.append(quad[3])
			else:
				for x in quad:
					#print x, a
					if (tabla.lookup(x)==True):
						q.append(tabla.getDir(x))
					elif (tablatemp.lookup(x)==True):
						q.append(tablatemp.getDir(x))
					elif (tablapoint.lookup(x)==True):
						q.append(tablapoint.getDir(x))
					elif (tablaP.lookup(x)==True):
						q.append(tablaP.getDir(x))
					elif (tablatempP.lookup(x)==True):
						q.append(tablatempP.getDir(x))
					elif (tablapointP.lookup(x)==True):
						q.append(tablapointP.getDir(x))
					elif (tabconst.lookup(x)==True):
						q.append(tabconst.getDir(x))
					else:
						q.append(quad[i])
					i = i + 1
			print >> f, str(a) + "|" + str(q[0]) + "|" + str(q[1]) + "|" + str(q[2]) + "|" + str(q[3]) #Imprime cuadruplo en archivo objeto
		f.close()

	def __str__(self):
		return repr(self.data)