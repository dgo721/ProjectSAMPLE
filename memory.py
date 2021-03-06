import copy
from error_exec import senderror

class Memory:

	#Inicializa clase Memory / Crea mapa de memoria
	def __init__(self):
		self.gintdir = 2000
		self.gintend = 2000
		self.gint = dict()
		self.gfloatdir = 4000
		self.gfloatend = 4000
		self.gfloat = dict()
		self.gbooldir = 6000
		self.gboolend = 6000
		self.gbool = dict()
		self.gtintdir = 22000
		self.gtintend = 22000
		self.gtint = dict()
		self.gtfloatdir = 24000
		self.gtfloatend = 24000
		self.gtfloat = dict()
		self.gtbooldir = 26000
		self.gtboolend = 26000
		self.gtbool = dict()
		self.lintdir = 12000
		self.lintend = 12000
		self.lint = dict()
		self.lfloatdir = 14000
		self.lfloatend = 14000
		self.lfloat = dict()
		self.lbooldir = 16000
		self.lboolend = 16000
		self.lbool = dict()
		self.ltintdir = 32000
		self.ltintend = 32000
		self.ltint = dict()
		self.ltfloatdir = 34000
		self.ltfloatend = 34000
		self.ltfloat = dict()
		self.ltbooldir = 36000
		self.ltboolend = 36000
		self.ltbool = dict()
		self.gpdir = 40000
		self.gpend = 40000
		self.gp = dict()
		self.lpdir = 42000
		self.lpend = 42000
		self.lp = dict()
		#Valores de creacion para nueva memoria
		self.nwintdir = 12000
		self.nwintend = 12000
		self.nwint = dict()
		self.nwfloatdir = 14000
		self.nwfloatend = 14000
		self.nwfloat = dict()
		self.nwbooldir = 16000
		self.nwboolend = 16000
		self.nwbool = dict()
		self.nwtintdir = 32000
		self.nwtintend = 32000
		self.nwtint = dict()
		self.nwtfloatdir = 34000
		self.nwtfloatend = 34000
		self.nwtfloat = dict()
		self.nwtbooldir = 36000
		self.nwtboolend = 36000
		self.nwtbool = dict()
		self.nwpdir = 42000
		self.nwpend = 42000
		self.nwp = dict()
		self.callip = list() #Pila IPs de llamada
		self.pilaLocal = list() #Pila Memoria en Sleep
		self.localspace = 14000 #Espacio disponible en memoria local

	#Crea mapa de memoria local nueva / Cuadruplo ERA
	def newLocalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p):
		self.nwintdir = 12000
		self.nwintend = self.nwintdir + cont_int
		if self.nwintend >= 14000:
			senderror(3)
		self.nwint = dict()
		self.nwfloatdir = 14000
		self.nwfloatend = self.nwfloatdir + cont_float
		if self.nwfloatend >= 16000:
			senderror(3)
		self.nwfloat = dict()
		self.nwbooldir = 16000
		self.nwboolend = self.nwbooldir + cont_bool
		if self.nwboolend >= 18000:
			senderror(3)
		self.nwbool = dict()
		self.nwtintdir = 32000
		self.nwtintend = self.nwintdir + cont_tint
		if self.nwtintend >= 34000:
			senderror(3)
		self.nwtint = dict()
		self.nwtfloatdir = 34000
		self.nwtfloatend = self.nwfloatdir + cont_tfloat
		if self.nwtfloatend >= 36000:
			senderror(3)
		self.nwtfloat = dict()
		self.nwtbooldir = 36000
		self.nwtboolend = self.nwtbooldir + cont_tbool
		if self.nwtboolend >= 38000:
			senderror(3)
		self.nwtbool = dict()
		self.nwpdir = 42000
		self.nwpend = self.nwpdir + cont_p
		if self.nwpend >= 44000:
			senderror(3)
		self.nwp = dict()

	#Inicializa mapa de memoria global (workspace)
	def setGlobalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p):
		self.gintend = self.gintend + cont_int
		if self.gintend >= 4000:
			senderror(3)
		self.gfloatend = self.gfloatend + cont_float
		if self.gfloatend >= 6000:
			senderror(3)
		self.gboolend = self.gboolend + cont_bool
		if self.gboolend >= 8000:
			senderror(3)
		self.gtintend = self.gtintend + cont_tint
		if self.gtintend >= 24000:
			senderror(3)
		self.gtfloatend = self.gtfloatend + cont_tfloat
		if self.gtfloatend >= 26000:
			senderror(3)
		self.gtboolend = self.gtboolend + cont_tbool
		if self.gtboolend >= 28000:
			senderror(3)
		self.gpend = self.gpend + cont_p
		if self.gpend >= 42000:
			senderror(3)

	#Inicializa mapa de memoria local (modulo); el espacio local recibe la informacion de la memoria, la cual fue inicializada al momento de realizar una operacion del cuadruplo era.
	def setLocalMemory(self):
		#Se ocupa un nuevo espacio de memoria local
		self.localspace = self.localspace - (self.nwintend - self.nwintdir) - (self.nwfloatend - self.nwfloatdir) - (self.nwboolend - self.nwbooldir) - (self.nwtintend - self.nwtintdir) - (self.nwtfloatend - self.nwtfloatdir) - (self.nwtboolend - self.nwtbooldir) - (self.nwpend - self.nwpdir)
		if self.localspace <= 0:
			senderror(3) #Salida de error en caso de agotarse el espacio de memoria local.
		self.lintdir = self.nwintdir #Memoria local toma direccion nueva
		self.lintend = self.nwintend #Memoria local establece el limite de espacio para variables
		self.lint = self.nwint
		self.lint = copy.deepcopy(self.nwint) #La memoria local recibe la informacion de la memoria nueva.
		self.lfloatdir = self.nwfloatdir 
		self.lfloatend = self.nwfloatend
		self.lfloat = self.nwfloat
		self.lfloat = copy.deepcopy(self.nwfloat)
		self.lbooldir = self.nwbooldir
		self.lboolend = self.nwboolend
		self.lbool = self.nwbool
		self.lbool = copy.deepcopy(self.nwbool)
		self.ltintdir = self.nwtintdir
		self.ltintend = self.nwtintend
		self.ltint = self.nwtint
		self.ltint = copy.deepcopy(self.nwtint)
		self.ltfloatdir = self.nwtfloatdir
		self.ltfloatend = self.nwtfloatend
		self.ltfloat = self.nwtfloat
		self.ltfloat = copy.deepcopy(self.nwtfloat)
		self.ltbooldir = self.nwtbooldir
		self.ltboolend = self.nwtboolend
		self.ltbool = self.nwtbool
		self.ltbool = copy.deepcopy(self.nwtbool)
		self.lpdir = self.nwpdir
		self.lpend = self.nwpend
		self.lp = self.nwp
		self.lp = copy.deepcopy(self.nwp)

	#El espacio de memoria local (modulo) es liberado
	def freeLocalMemory(self):
		self.localspace = self.localspace + (self.lintend - self.lintdir) + (self.lfloatend - self.lfloatdir) + (self.lboolend - self.lbooldir) + (self.ltintend - self.ltintdir) + (self.ltfloatend - self.ltfloatdir) + (self.ltboolend - self.ltbooldir) + (self.lpend - self.lpdir)
		self.lintdir = 12000
		self.lintend = 12000
		self.lint = dict()
		self.lfloatdir = 14000
		self.lfloatend = 14000
		self.lfloat = dict()
		self.lbooldir = 16000
		self.lboolend = 16000
		self.lbool = dict()
		self.ltintdir = 32000
		self.ltintend = 32000
		self.ltint = dict()
		self.ltfloatdir = 34000
		self.ltfloatend = 34000
		self.ltfloat = dict()
		self.ltbooldir = 36000
		self.ltboolend = 36000
		self.ltbool = dict()
		self.lpdir = 42000
		self.lpend = 42000
		self.lp = dict()

	#Guarda segmento de memoria local ante una nueva llamada recursiva
	def sleepLocalMemory(self):
		self.pilaLocal.append([self.lintend, self.lint, self.lfloatend, self.lfloat, self.lboolend, self.lbool, self.ltintend, self.ltint, self.ltfloatend, self.ltfloat, self.ltboolend, self.ltbool, self.lpend, self.lp])

	#Retoma un espacio local de memoria que fue previamente almacenado a guardar, a partir de la pila Local de memoria
	def awakeLocalMemory(self):
		mem_awake = self.pilaLocal.pop()
		self.lintdir = 12000
		self.lintend = mem_awake[0]
		self.lint = mem_awake[1]
		self.lint = copy.deepcopy(mem_awake[1])
		self.lfloatdir = 14000
		self.lfloatend = mem_awake[2]
		self.lfloat = mem_awake[3]
		self.lfloat = copy.deepcopy(mem_awake[3])
		self.lbooldir = 16000
		self.lboolend = mem_awake[4]
		self.lbool = mem_awake[5]
		self.lbool = copy.deepcopy(mem_awake[5])
		self.ltintdir = 32000
		self.ltintend = mem_awake[6]
		self.ltint = mem_awake[7]
		self.ltint = copy.deepcopy(mem_awake[7])
		self.ltfloatdir = 34000
		self.ltfloatend = mem_awake[8]
		self.ltfloat = mem_awake[9]
		self.ltfloat = copy.deepcopy(mem_awake[9])
		self.ltbooldir = 36000
		self.ltboolend = mem_awake[10]
		self.ltbool = mem_awake[11]
		self.ltbool = copy.deepcopy(mem_awake[11])
		self.lpdir = 42000
		self.lpend = mem_awake[12]
		self.lp = mem_awake[13]
		self.lp = copy.deepcopy(mem_awake[13])

	#Aniade elemento a memoria global
	def addGlobalInt(self, num, data):
		self.gint[num]=data

	def addGlobalFloat(self, num, data):
		self.gfloat[num]=data

	def addGlobalBool(self, num, data):
		self.gbool[num]=data

	#Aniade elemento temporal a memoria global
	def addGlobalIntTemp(self, num, data):
		self.gtint[num]=data

	def addGlobalFloatTemp(self, num, data):
		self.gtfloat[num]=data

	def addGlobalBoolTemp(self, num, data):
		self.gtbool[num]=data

	#Aniade elemento a memoria local
	def addLocalInt(self, num, data):
		self.lint[num]=data

	def addLocalFloat(self, num, data):
		self.lfloat[num]=data

	def addLocalBool(self, num, data):
		self.lbool[num]=data

	#Aniade elemento temporal a memoria local
	def addLocalIntTemp(self, num, data):
		self.ltint[num]=data

	def addLocalFloatTemp(self, num, data):
		self.ltfloat[num]=data

	def addLocalBoolTemp(self, num, data):
		self.ltbool[num]=data

	def addGlobalPointer(self, num, data):
		self.gp[num]=data

	def addLocalPointer(self, num, data):
		self.lp[num]=data

	#Enlaza parametros a memoria local
	def addParamInt(self, num, data):
		self.nwint[num]=data

	def addParamFloat(self, num, data):
		self.nwfloat[num]=data

	def addParamBool(self, num, data):
		self.nwbool[num]=data
	
	#Busca elemento en memoria
	def getGlobalInt(self, num):
		return self.gint[num]

	def getGlobalFloat(self, num):
		return self.gfloat[num]

	def getGlobalBool(self, num):
		return self.gbool[num]

	def getGlobalIntTemp(self, num):
		return self.gtint[num]

	def getGlobalFloatTemp(self, num):
		return self.gtfloat[num]

	def getGlobalBoolTemp(self, num):
		return self.gtbool[num]

	def getLocalInt(self, num):
		return self.lint[num]

	def getLocalFloat(self, num):
		return self.lfloat[num]

	def getLocalBool(self, num):
		return self.lbool[num]

	def getLocalIntTemp(self, num):
		return self.ltint[num]

	def getLocalFloatTemp(self, num):
		return self.ltfloat[num]

	def getLocalBoolTemp(self, num):
		return self.ltbool[num]

	def getGlobalPointer(self, num):
		return self.gp[num]

	def getLocalPointer(self, num):
		return self.lp[num]

	def getParamInt(self, num):
		return self.nwint[num]

	def getParamFloat(self, num, data):
		return self.nwfloat[num]

	def getParamBool(self, num, data):
		return self.nwbool[num]

	#Aniade cuadruplo para su proxima continuacion
	def addIP(self, ip):
		self.callip.append(ip)

	#Obtiene cuadruplo para la continuacion de la ejecucion
	def getIP(self):
		return self.callip.pop()

	def checkNone(data):
		if data == None:
			senderror(5, data)

	def echoGlobal(self):
		print "GLOBAL INT--", self.gint
		print "GLOBAL FLOAT--", self.gfloat
		print "GLOBAL BOOL--", self.gbool
		print "GLOBAL INT TEMP--", self.gtint
		print "GLOBAL FLOAT TEMP--", self.gtfloat
		print "GLOBAL BOOL TEMP--", self.gtbool
		print "GLOBAL POINT--", self.gp

	def echoLocal(self):
		print "LOCAL INT--", self.lint
		print "LOCAL FLOAT--", self.lfloat
		print "LOCAL BOOL--", self.lbool
		print "LOCAL INT TEMP--", self.ltint
		print "LOCAL FLOAT TEMP--", self.ltfloat
		print "LOCAL BOOL TEMP--", self.ltbool
		print "LOCAL POINT--", self.lp

	def echoNew(self):
		print "NEW INT--", self.nwint
		print "NEW FLOAT--", self.nwfloat
		print "NEW BOOL--", self.nwbool
		print "NEW INT TEMP--", self.nwtint
		print "NEW FLOAT TEMP--", self.nwtfloat
		print "NEW BOOL TEMP--", self.nwtbool
		print "NEW POINT--", self.nwp

	def echoEndMemory(self):
		print self.gintend
		print self.gfloatend
		print self.gboolend
		print self.gtintend
		print self.gtfloatend
		print self.gtboolend
		print self.gpend
		print self.lintend
		print self.lfloatend
		print self.lboolend
		print self.ltintend
		print self.ltfloatend
		print self.ltboolend
		print self.lpend