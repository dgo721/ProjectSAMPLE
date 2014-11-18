import copy

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
		self.localspace = 14000
		self.pilaLocal = list()
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
		#Pila IPs de llamada
		self.callip = list()

	#Crea mapa de memoria local nueva / Cuadruplo ERA
	def newLocalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p):
		self.nwintdir = 12000
		self.nwintend = self.nwintdir + cont_int
		self.nwint = dict()
		self.nwfloatdir = 14000
		self.nwfloatend = self.nwfloatdir + cont_float
		self.nwfloat = dict()
		self.nwbooldir = 16000
		self.nwboolend = self.nwbooldir + cont_bool
		self.nwbool = dict()
		self.nwtintdir = 32000
		self.nwtintend = self.nwintdir + cont_tint
		self.nwtint = dict()
		self.nwtfloatdir = 34000
		self.nwtfloatend = self.nwfloatdir + cont_tfloat
		self.nwtfloat = dict()
		self.nwtbooldir = 36000
		self.nwtboolend = self.nwtbooldir + cont_tbool
		self.nwtbool = dict()
		self.nwpdir = 42000
		self.nwpend = self.nwpdir + cont_p
		self.nwp = dict()

	#Inicializa mapa de memoria global (workspace)
	def setGlobalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p):
		self.gintend = self.gintend + cont_int
		self.gfloatend = self.gfloatend + cont_float
		self.gboolend = self.gboolend + cont_bool
		self.gtintend = self.gtintend + cont_tint
		self.gtfloatend = self.gtfloatend + cont_tfloat
		self.gtboolend = self.gtboolend + cont_tbool
		self.gpend = self.gpend + cont_p
		#print self.gintend, self.gfloatend, self.gboolend, self.gtintend, self.gtfloatend, self.gtboolend

	#Inicializa mapa de memoria local (modulo)
	def setLocalMemory(self):
		self.lintdir = self.nwintdir
		self.lintend = self.nwintend
		self.lint = self.nwint
		self.lint = copy.deepcopy(self.nwint)
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
		#print self.lintend, self.lfloatend, self.lboolend, self.ltintend, self.ltfloatend, self.ltboolend

	def freeLocalMemory(self):
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

	def addIP(self, ip):
		self.callip.append(ip)

	def getIP(self):
		return self.callip.pop()

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