class Memory:

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

	def setGlobalMemory(self, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool):
		self.gintend = self.gintend + cont_int
		self.gfloatend = self.gfloatend + cont_float
		self.gboolend = self.gboolend + cont_bool
		self.gtintend = self.gtintend + cont_tint
		self.gtfloatend = self.gtfloatend + cont_tfloat
		self.gtboolend = self.gtboolend + cont_tbool
		print self.gintend, self.gfloatend, self.gboolend, self.gtintend, self.gtfloatend, self.gtboolend