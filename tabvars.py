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

x=TabVars()
print x

x.add('y', 'INT')
x.add("x", "INT")

if x.lookup("x")!=True:
	x.add("x", "FLOAT")
else:
	print "EXISTS"
print x