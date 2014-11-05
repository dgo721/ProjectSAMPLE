import re
from memory import Memory

read = 1
ip = 0
pattn_string = r'\".*?\"'
pattn_float = r'\d+\.\d*'
pattn_int = r'\d+'
directory = dict()
constants = dict()
quad = list()
memoria = Memory()

#Transforma el string de parametros en objeto lista
def listParams(lista):
	if lista == '[]':
		return None
	nvlista = lista[1:-1]
	temp = nvlista.split(",")
	i = 0
	for t in temp:
		temp[i] = temp[i][1:-1]
		i = i + 1
	return temp

def getDirValue(num):
	if num >= 36000:
		pass
	elif num >= 34000:
		pass
	elif num >= 32000:
		pass
	elif num >= 26000:
		pass
	elif num >= 24000:
		pass
	elif num >= 22000:
		pass
	elif num >= 16000:
		pass
	elif num >= 14000:
		pass
	elif num >= 12000:
		pass
	elif num >= 6000:
		pass
	elif num >= 4000:
		pass
	elif num >= 2000:
		pass
	elif num >= 100:
		return constants[num]

f = open('sample.smo', 'r')

for line in f:
	string = line.split("|")
	last = string[-1].split("\n")
	string[-1] = last[0]
	#print string;

	if string[0] == '%%%%':
		read = read + 1
	else:
		if read == 1:
			#list_param = string[1]
			list_param = listParams(string[1])
			if string[5] == 'None':
				quad_init = None
			else:
				quad_init = int(string[5])
			cont_int = int(string[2])
			cont_float = int(string[3])
			cont_bool = int(string[4])
			cont_tint = int(string[6])
			cont_tfloat = int(string[7])
			cont_tbool = int(string[8])
			directory[string[0]] = [list_param, quad_init, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool]
			if string[0] == "*work*":
				memoria.setGlobalMemory(cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool)
		if read == 2:
			esint = re.compile(pattn_int)
			esfloat = re.compile(pattn_float)
			esstring = re.compile(pattn_string)
			if re.match(esstring, string[0]):
				key = string[0]
			elif re.match(esfloat, string[0]):
				key = float(string[0])
			elif re.match(esint, string[0]):
				key = int(string[0])
			
			constants[int(string[1])]=key
		if read == 3:
			temp = [string[1], string[2], string[3], string[4]]
			quad.append([int(string[0]),temp])

f.close()
#print quad[0][0]

while quad[ip][1][0] != 'end':
	qactual = quad[ip][1]

	if qactual[0] == '+':
		pass

	ip = ip + 1