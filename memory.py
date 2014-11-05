class Memory:

	#Inicializa clase Memory
	def __init__(self):
		self.gintdir = 2000
		self.gintend = 2000
		self.gint = list()
		self.gfloatdir = 4000
		self.gfloatend = 4000
		self.gfloat = list()
		self.gbooldir = 6000
		self.gboolend = 6000
		self.gbool = list()
		self.gtintdir = 22000
		self.gtintend = 22000
		self.gtint = list()
		self.gtfloatdir = 24000
		self.gtfloatend = 24000
		self.gtfloat = list()
		self.gtbooldir = 26000
		self.gtboolend = 26000
		self.gtbool = list()
		self.lintdir = 12000
		self.lintend = 12000
		self.lint = list()
		self.lfloatdir = 14000
		self.lfloatend = 14000
		self.lfloat = list()
		self.lbooldir = 16000
		self.lboolend = 16000
		self.lbool = list()
		self.ltintdir = 32000
		self.ltintend = 32000
		self.ltint = list()
		self.ltfloatdir = 34000
		self.ltfloatend = 34000
		self.ltfloat = list()
		self.ltbooldir = 36000
		self.ltboolend = 36000
		self.ltbool = list()

	#Inicializa mapa de memoria global (workspace)
	def setGlobalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool):
		self.gintend = self.gintend + cont_int
		self.gfloatend = self.gfloatend + cont_float
		self.gboolend = self.gboolend + cont_bool
		self.gtintend = self.gtintend + cont_tint
		self.gtfloatend = self.gtfloatend + cont_tfloat
		self.gtboolend = self.gtboolend + cont_tbool
		#print self.gintend, self.gfloatend, self.gboolend, self.gtintend, self.gtfloatend, self.gtboolend

	#Aniade elemento a memoria global
	def addGlobalInt(self, data):
		self.gint.append(data)

	def addGlobalFloat(self, data):
		self.gfloat.append(data)

	def addGlobalBool(self, data):
		self.gbool.append(data)

	#Aniade elemento temporal a memoria global
	def addGlobalIntTemp(self, data):
		self.gtint.append(data)

	def addGlobalFloatTemp(self, data):
		self.gtfloat.append(data)

	def addGlobalBoolTemp(self, data):
		self.gtbool.append(data)

	#Aniade elemento a memoria local
	def addLocalInt(self, data):
		self.lint.append(data)

	def addLocalFloat(self, data):
		self.lfloat.append(data)

	def addLocalBool(self, data):
		self.lbool.append(data)

	#Aniade elemento temporal a memoria local
	def addLocalIntTemp(self, data):
		self.ltint.append(data)

	def addLocalFloatTemp(self, data):
		self.ltfloat.append(data)

	def addLocalBoolTemp(self, data):
		self.ltbool.append(data)
	
	#Busca elemento en memoria
	def getGlobalInt(self, num):
		pos = num - self.gintdir
		return self.gint[pos]

	def getGlobalFloat(self, num):
		pos = num - self.gfloatdir
		return self.gfloat[pos]

	def getGlobalBool(self, num):
		pos = num - self.gbooldir
		return self.gbool[pos]

	def getGlobalIntTemp(self, num):
		pos = num - self.gtintdir
		return self.gtint[pos]

	def getGlobalFloatTemp(self, num):
		pos = num - self.gtfloatdir
		return self.gtfloat[pos]

	def getGlobalBoolTemp(self, num):
		pos = num - self.gtbooldir
		return self.gtbool[pos]

	def getLocalInt(self, num):
		pos = num - self.lintdir
		return self.lint[pos]

	def getLocalFloat(self, num):
		pos = num - self.lfloatdir
		return self.lfloat[pos]

	def getLocalBool(self, num):
		pos = num - self.lbooldir
		return self.lbool[pos]

	def getLocalIntTemp(self, num):
		pos = num - self.ltintdir
		return self.ltint[pos]

	def getLocalFloatTemp(self, num):
		pos = num - self.ltfloatdir
		return self.ltfloat[pos]

	def getLocalBoolTemp(self, num):
		pos = num - self.ltbooldir
		return self.ltbool[pos]

	def echoGlobal(self):
		print "GLOBAL INT--", self.gint
		print "GLOBAL FLOAT--", self.gfloat
		print "GLOBAL BOOL--", self.gbool
		print "GLOBAL INT TEMP--", self.gtint
		print "GLOBAL FLOAT TEMP--", self.gtfloat
		print "GLOBAL BOOL TEMP--", self.gtbool