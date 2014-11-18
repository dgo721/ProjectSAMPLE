import re, turtle, math, sys
from memory import Memory
from error_exec import senderror

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

def addDirData(num, data):
	#print "addDirData--", num, data
	if num >= 42000:
		memoria.addLocalPointer(num, data)
	elif num >= 40000:
		memoria.addGlobalPointer(num, data)
	elif num >= 36000:
		memoria.addLocalBoolTemp(num, data)
	elif num >= 34000:
		memoria.addLocalFloatTemp(num, data)
	elif num >= 32000:
		memoria.addLocalIntTemp(num, data)
	elif num >= 26000:
		memoria.addGlobalBoolTemp(num, data)
	elif num >= 24000:
		memoria.addGlobalFloatTemp(num, data)
	elif num >= 22000:
		memoria.addGlobalIntTemp(num, data)
	elif num >= 16000:
		memoria.addLocalBool(num, data)
	elif num >= 14000:
		memoria.addLocalFloat(num, data)
	elif num >= 12000:
		memoria.addLocalInt(num, data)
	elif num >= 6000:
		memoria.addGlobalBool(num, data)
	elif num >= 4000:
		memoria.addGlobalFloat(num, data)
	elif num >= 2000:
		memoria.addGlobalInt(num, data)

def getDirData(num):
	if num >= 42000:
		return memoria.getLocalPointer(num)
	elif num >= 40000:
		return memoria.getGlobalPointer(num)
	elif num >= 36000:
		return memoria.getLocalBoolTemp(num)
	elif num >= 34000:
		return memoria.getLocalFloatTemp(num)
	elif num >= 32000:
		return memoria.getLocalIntTemp(num)
	elif num >= 26000:
		return memoria.getGlobalBoolTemp(num)
	elif num >= 24000:
		return memoria.getGlobalFloatTemp(num)
	elif num >= 22000:
		return memoria.getGlobalIntTemp(num)
	elif num >= 16000:
		return memoria.getLocalBool(num)
	elif num >= 14000:
		return memoria.getLocalFloat(num)
	elif num >= 12000:
		return memoria.getLocalInt(num)
	elif num >= 6000:
		return memoria.getGlobalBool(num)
	elif num >= 4000:
		return memoria.getGlobalFloat(num)
	elif num >= 2000:
		return memoria.getGlobalInt(num)
	elif num >= 100:
		return constants[num]

def addParamData(num, data):
	#print "addDirData--", num, data
	if num >= 16000:
		memoria.addParamBool(num, data)
	elif num >= 14000:
		memoria.addParamFloat(num, data)
	elif num >= 12000:
		memoria.addParamInt(num, data)

def getColor(color):
	if color == "red":
		return "#d03832"
	elif color == "yellow":
		return "#e1c81d"
	elif color == "green":
		return "#31ad29"
	elif color == "blue":
		return "#2734a4"
	elif color == "black":
		return "#000000";
	elif color == "white":
		return "#ffffff"
	elif color == "orange":
		return "#ee7c15"
	elif color == "purple":
		return "#740fd5"
	elif color == "cyan":
		return "#23c5ef"

def getDarkColor(color):
	if color == "red":
		return "#7c1d1c"
	elif color == "yellow":
		return "#b2a713"
	elif color == "green":
		return "#147517"
	elif color == "blue":
		return "#2e2c57"
	elif color == "black":
		return "#ffffff";
	elif color == "white":
		return "#000000"
	elif color == "orange":
		return "#a06911"
	elif color == "purple":
		return "#4a0b69"
	elif color == "cyan":
		return "#0f698e"

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
			cont_p = int(string[9])
			directory[string[0]] = [list_param, quad_init, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p]
			if string[0] == "*work*":
				memoria.setGlobalMemory(cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p)
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
#print constants

current_scope = "*work*"
parametros = list()
num_parametros = 0
paramint = 12000
paramfloat = 14000
parambool = 16000

turtle.bgcolor("#727678")
turtle.seth(90)
turtle.color("darkgreen", "black")
turtle.pendown()

while quad[ip][1][0] != 'end':
	qactual = quad[ip][1]
	turtle.seth(90)
	turtle.color("darkgreen", "black")
	turtle.pendown()
	#print qactual

	if ip == 10:
		#print getDirData(int(qactual[1])), getDirData(int(qactual[2]))
		#memoria.echoGlobal()
		#memoria.echoEndMemory()
		#print constants
		pass

	if qactual[0] == '+':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 + operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '-':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 - operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '*':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 * operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '/':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		try:
			tmp = operador1 / operador2
		except ZeroDivisionError:
			senderror(1)
		else:
			addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '=':
		#print "=", getDirData(int(qactual[1])), qactual[1], int(qactual[3])
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1])))
		else:
			tmp = getDirData(int(qactual[1]))
		if int(qactual[3]) >= 40000:
			data = getDirData(int(qactual[3]))
		else:
			data = int(qactual[3])
		addDirData(data, tmp)

	elif qactual[0] == '==':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 == operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '<>':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 <> operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '>=':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 >= operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '<=':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 <= operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '>':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 > operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '<':
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 < operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == 'sample1':
		prevSample = True
		if int(qactual[1]) >= 40000:
			linew = getDirData(getDirData(int(qactual[1])))
		else:
			linew = getDirData(int(qactual[1]))
		color = getColor(qactual[2])
		ip = ip + 1; qactual = quad[ip][1]
		if int(qactual[3]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[3])))*5
		else:
			tmp = getDirData(int(qactual[3]))*5
		print qactual[0], qactual[1], qactual[2], getDirData(int(qactual[3])), linew, color
		turtle.pendown()
		turtle.pensize(linew); turtle.pencolor(color)
		if qactual[2] == 'up':
			turtle.seth(90)
			turtle.forward(tmp)
		elif qactual[2] == 'down':
			turtle.seth(270)
			turtle.forward(tmp)
		elif qactual[2] == 'left':
			turtle.seth(180)
			turtle.forward(tmp)
		elif qactual[2] == 'right':
			turtle.seth(0)
			turtle.forward(tmp)

	elif qactual[0] == 'sample':
		print qactual[0], qactual[1], qactual[2], getDirData(int(qactual[3]))
		prevSample = True
		if int(qactual[3]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[3])))*5
		else:
			tmp = getDirData(int(qactual[3]))*5
		turtle.penup()
		if qactual[2] == 'up':
			turtle.seth(90)
			turtle.forward(tmp)
		elif qactual[2] == 'down':
			turtle.seth(270)
			turtle.forward(tmp)
		elif qactual[2] == 'left':
			turtle.seth(180)
			turtle.forward(tmp)
		elif qactual[2] == 'right':
			turtle.seth(0)
			turtle.forward(tmp)

	elif qactual[0] == 'arc':
		print qactual[0], getDirData(int(qactual[1])), getDirData(int(qactual[2])), qactual[3]
		if int(qactual[1]) >= 40000:
			size = getDirData(getDirData(int(qactual[1])))*5
		else:
			size = getDirData(int(qactual[1]))*5
		if int(qactual[2]) >= 40000:
			angle = getDirData(getDirData(int(qactual[2])))
		else:
			angle = getDirData(int(qactual[2]))
		turtle.pencolor(getColor(qactual[3]));
		turtle.pensize(2)
		turtle.circle(size,angle)
		prevSample = False

	elif qactual[0] == 'oval':
		print qactual[0], getDirData(int(qactual[1])), getDirData(int(qactual[2])), qactual[3]
		if int(qactual[1]) >= 40000:
			dmenor = getDirData(getDirData(int(qactual[1])))/5
		else:
			dmenor = getDirData(int(qactual[1]))/5
		if int(qactual[2]) >= 40000:
			dmayor = getDirData(getDirData(int(qactual[2])))/5
		else:
			dmayor = getDirData(int(qactual[2]))/5
		turtle.pencolor(getDarkColor(qactual[3]))

		turtle.penup()
		turtle.forward((dmenor+0.5)*10)
		turtle.seth(180)
		turtle.forward((dmayor+0.5)*10)
		turtle.seth(90)
		turtle.shape("circle")
		turtle.shapesize(dmenor+0.5,dmayor+0.5,1)
		turtle.fillcolor(getDarkColor(qactual[3]))
		turtle.stamp()
		turtle.shapesize(dmenor,dmayor,1)
		turtle.fillcolor(getColor(qactual[3]))
		turtle.stamp()
		turtle.shapesize(1,1,1)
		turtle.fillcolor("black")
		turtle.shape('classic')
		turtle.penup()
		turtle.seth(0)
		turtle.forward((dmayor+0.5)*10)
		turtle.seth(90)
		turtle.backward((dmenor+0.5)*10)
		prevSample = False

	elif qactual[0] == 'trio':
		print qactual[0], getDirData(int(qactual[1])), getDirData(int(qactual[2])), qactual[3]
		if int(qactual[1]) >= 40000:
			b = getDirData(getDirData(int(qactual[1])))*5
		else:
			b = getDirData(int(qactual[1]))*5
		if int(qactual[2]) >= 40000:
			h = getDirData(getDirData(int(qactual[2])))*5
		else:
			h = getDirData(int(qactual[2]))*5
		ang = math.degrees(math.atan(h/(b/2)))
		l = math.sqrt(h**2 + (b/2)**2)
		turtle.pensize(5);
		turtle.pencolor(getDarkColor(qactual[3]))
		turtle.fillcolor(getColor(qactual[3]))
		turtle.fill(True)
		turtle.seth(90)
		turtle.left(90-ang)
		turtle.forward(l)
		turtle.left(ang*2)
		turtle.forward(l)
		turtle.left(180-ang)
		turtle.forward(b)
		turtle.fill(False)
		prevSample = False

	elif qactual[0] == 'quad':
		print qactual[0], getDirData(int(qactual[1])), getDirData(int(qactual[2])), qactual[3]
		if int(qactual[1]) >= 40000:
			base = getDirData(getDirData(int(qactual[1])))*5
		else:
			base = getDirData(int(qactual[1]))*5
		if int(qactual[2]) >= 40000:
			height = getDirData(getDirData(int(qactual[2])))*5
		else:
			height = getDirData(int(qactual[2]))*5
		turtle.pensize(5);
		turtle.pencolor(getDarkColor(qactual[3]))
		turtle.fillcolor(getColor(qactual[3]))
		turtle.fill(True)
		for _ in range(2):
			turtle.forward(height)
			turtle.left(90)
			turtle.forward(base)
			turtle.left(90)
		turtle.fill(False)
		prevSample = False

	elif qactual[0] == 'arr' or qactual[0] == 'mat':
		print qactual[0], int(qactual[1]), 0, qactual[3]
		ini = int(qactual[1])
		if ini >= 6000:
			data = False
		elif ini >= 4000:
			data = 0.0
		elif ini >= 2000:
			data = 0
		i = 0
		while i < int(qactual[3]):
			addDirData(int(qactual[1])+i, data)
			i = i + 1

	elif qactual[0] == 'ver':
		print qactual[0], getDirData(int(qactual[1])), qactual[2], qactual[3]
		tmp = getDirData(int(qactual[1]))
		if tmp < 0 or tmp > int(qactual[3]):
			senderror(2)

	elif qactual[0] == 'echo':
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1])))
		else:
			tmp = getDirData(int(qactual[1]))
		tmp1 = str(tmp)
		esstring = re.compile(pattn_string)
		if re.match(esstring, tmp1):
			tmp1 = tmp.split("\"")
			print tmp1[1]
		else:
			print tmp

	elif qactual[0] == '+dir':
		tmp = getDirData(int(qactual[1])) + int(qactual[2])
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == 'goTo':
		print qactual[0], qactual[3]
		ip = int(qactual[3]) - 2

	elif qactual[0] == 'goToF':
		print qactual[0], getDirData(int(qactual[1])), qactual[3]
		if getDirData(int(qactual[1])) == False:
			ip = int(qactual[3]) - 2

	elif qactual[0] == 'era':
		print qactual[0], qactual[1]
		memoria.newLocalMemory(cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p)
		if directory[qactual[1]][0] != None:
			parametros = directory[qactual[1]][0]
		else:
			parametros = []
		num_parametros = 0

	elif qactual[0] == 'param':
		print qactual[0], qactual[1]
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1])))
		else:
			tmp = getDirData(int(qactual[1]))
		if parametros[num_parametros] == 'int':
			addParamData(paramint, tmp)
			paramint = paramint + 1
		elif parametros[num_parametros] == 'float':
			addParamData(paramfloat, tmp)
			paramfloat = paramfloat + 1
		elif parametros[num_parametros] == 'bool':
			addParamData(parambool, tmp)
			parambool = parambool + 1
		num_parametros += 1

	elif qactual[0] == 'gosub':
		print qactual[0], qactual[1]
		memoria.sleepLocalMemory()
		memoria.setLocalMemory()
		if current_scope == "*work*":
			memoria.addIP([ip, current_scope])
		current_scope = qactual[1]
		direcmod = directory[qactual[1]][1]
		ip = direcmod - 2

	elif qactual[0] == 'ret':
		memoria.freeLocalMemory()
		ipscope = memoria.getIP()
		if ipscope[1] != "*work*":
			memoria.awakeLocalMemory()
		ip = ipscope[0]
		current_scope = ipscope[1]

	#print "IP-", ip+1
	ip = ip + 1
turtle.hideturtle()
turtle.done()
#memoria.echoGlobal()