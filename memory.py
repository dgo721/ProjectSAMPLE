class Memory:

	#Inicializa clase Memory
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

	def echoGlobal(self):
		print "GLOBAL INT--", self.gint
		print "GLOBAL FLOAT--", self.gfloat
		print "GLOBAL BOOL--", self.gbool
		print "GLOBAL INT TEMP--", self.gtint
		print "GLOBAL FLOAT TEMP--", self.gtfloat
		print "GLOBAL BOOL TEMP--", self.gtbool
		print "GLOBAL POINT--", self.gp

	def echoEndMemory(self):
		print self.gintend
		print self.gfloatend
		print self.gboolend
		print self.gtintend
		print self.gtfloatend
		print self.gtboolend
		print self.gpend