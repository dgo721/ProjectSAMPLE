class Memory:

	def __init__(self):
		self.gint = {}
		self.gfloat = {}
		self.gbool = {}
		self.gtint = {}
		self.gtfloat = {}
		self.gtbool = {}
		self.lint = {}
		self.lfloat = {}
		self.lbool = {}
		self.ltint = {}
		self.ltfloat = {}
		self.ltbool = {}

	def addgINT(self, key):
		self.data[key]=[self.offset]
		self.offset = self.offset + 1