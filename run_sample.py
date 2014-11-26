import re, turtle, math, sys, random
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
memoria = Memory() #Crea mapa de memoria

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

#Aniade el nuevo valor al segmento correcto de memoria de acuerdo a su direccion / tipo
def addDirData(num, data):
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

#Accede al valor por el segmento correcto de memoria de acuerdo a su direccion / tipo
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

#Aniade valores que se pasan como parametros
def addParamData(num, data):
	if num >= 16000:
		memoria.addParamBool(num, data)
	elif num >= 14000:
		memoria.addParamFloat(num, data)
	elif num >= 12000:
		memoria.addParamInt(num, data)

#Regresa color primario
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

#Regresa color de contorno
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

f = open('sample.smo', 'r') #Abre el archivo objeto

for line in f:
	string = line.split("|")
	last = string[-1].split("\n")
	string[-1] = last[0]

	if string[0] == '%%%%':
		read = read + 1
	else:
		if read == 1:
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
			tipo_return = string[10]
			directory[string[0]] = [list_param, quad_init, cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p, tipo_return] #Regenera una entrada del directorio de modulos
			if string[0] == "*work*":
				memoria.setGlobalMemory(cont_int, cont_float, cont_bool, cont_tint, cont_tfloat, cont_tbool, cont_p) #Establece el mapa de memoria global
		if read == 2:
			esint = re.compile(pattn_int)
			esfloat = re.compile(pattn_float)
			esstring = re.compile(pattn_string)
			if re.match(esstring, string[0]): #Verifica si la constante es de tipo entero
				key = string[0]
			elif re.match(esfloat, string[0]): #Verifica si la constante es de tipo flotante
				key = float(string[0])
			elif re.match(esint, string[0]): #Verifica si la constante es de tipo string
				key = int(string[0])
			
			constants[int(string[1])]=key #Regenera una entrada de la tabla de constantes
		if read == 3:
			temp = [string[1], string[2], string[3], string[4]] #Regenera la secuencia de cuadruplos a ejecutar.
			quad.append([int(string[0]),temp])

f.close()

current_scope = "*work*" #Se inicializa el alcance global
parametros = list()
num_parametros = 0
paramint = 12000
paramfloat = 14000
parambool = 16000

turtle.title("Project SAMPLE by Python Turtle") #Titulo de la ventana
turtle.bgcolor("#727678")
turtle.seth(90)
turtle.color("darkgreen", "black")
turtle.pendown()

while quad[ip][1][0] != 'end': #Se lleva a cabo el proceso de ejecucion hasta encontrar el estatuto end
	qactual = quad[ip][1]
	turtle.seth(90)
	turtle.color("darkgreen", "black")
	turtle.pendown()

	if qactual[0] == '+': #Operacion suma
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1]))) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			operador1 = getDirData(int(qactual[1])) #Obtiene el valor de la direccion obtenida en el cuadruplo
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 + operador2
		addDirData(int(qactual[3]), tmp) #Almacena el nuevo valor en la direccion correspondiente.

	elif qactual[0] == '-': #Operacion resta
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

	elif qactual[0] == '*': #Operacion multiplicacion
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

	elif qactual[0] == '/': #Operacion division
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
			senderror(1) #Lanza mensaje de error cuando se encuentra una division entre 0
		else:
			addDirData(int(qactual[3]), tmp)

	elif qactual[0] == '=': #Operacion asignacion
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1]))) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			tmp = getDirData(int(qactual[1])) #Obtiene el valor de la direccion obtenida en el cuadruplo
		if int(qactual[3]) >= 40000:
			data = getDirData(int(qactual[3])) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			data = int(qactual[3]) #Obtiene el valor de la direccion obtenida en el cuadruplo
		addDirData(data, tmp) #Almacena el nuevo valor en la direccion correspondiente.

	elif qactual[0] == '==': #Operacion igual igual
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

	elif qactual[0] == '<>': #Operacion diferente
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

	elif qactual[0] == '>=': #Operacion mayor igual
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

	elif qactual[0] == '<=': #Operacion menor igual
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

	elif qactual[0] == '>': #Operacion mayor
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

	elif qactual[0] == '<': #Operacion menor
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

	elif qactual[0] == 'and': #Operacion and
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 and operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == 'or': #Operacion or
		if int(qactual[1]) >= 40000:
			operador1 = getDirData(getDirData(int(qactual[1])))
		else:
			operador1 = getDirData(int(qactual[1]))
		if int(qactual[2]) >= 40000:
			operador2 = getDirData(getDirData(int(qactual[2])))
		else:
			operador2 = getDirData(int(qactual[2]))
		tmp = operador1 or operador2
		addDirData(int(qactual[3]), tmp)

	elif qactual[0] == 'sample1': #Operacion dibujo linea
		prevSample = True
		if int(qactual[1]) >= 40000:
			linew = getDirData(getDirData(int(qactual[1]))) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			linew = getDirData(int(qactual[1])) #Obtiene el valor de la direccion recibida por el cuadruplo.
		color = getColor(qactual[2]) #Obtiene color
		ip = ip + 1; qactual = quad[ip][1] #Avanza al siguiente cuadruplo, parte 2
		if int(qactual[3]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[3])))*5
		else:
			tmp = getDirData(int(qactual[3]))*5
		turtle.pendown()
		turtle.pensize(linew); turtle.pencolor(color) #Modo dibujo
		if qactual[2] == 'up':
			turtle.seth(90) #Establece direccion hacia arriba
			turtle.forward(tmp)
		elif qactual[2] == 'down':
			turtle.seth(270) #Establece direccion hacia abajo
			turtle.forward(tmp)
		elif qactual[2] == 'left':
			turtle.seth(180) #Establece direccion hacia la izquierda
			turtle.forward(tmp)
		elif qactual[2] == 'right':
			turtle.seth(0) #Establece direccion hacia la derecha
			turtle.forward(tmp)

	elif qactual[0] == 'sample': #Operacion cursor
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

	elif qactual[0] == 'arc': #Operacion arco
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
		turtle.circle(size,angle) #Dibuja tamanio de arco de acuerdo a radio y angulo
		prevSample = False

	elif qactual[0] == 'oval': #Operacion ovalo
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
		turtle.stamp() #Dibuja / Estampa borde del circulo
		turtle.shapesize(dmenor,dmayor,1)
		turtle.fillcolor(getColor(qactual[3]))
		turtle.stamp() #Dibuja / Estampa el circulo
		turtle.shapesize(1,1,1)
		turtle.fillcolor("black")
		turtle.shape('classic')
		turtle.penup()
		turtle.seth(0)
		turtle.forward((dmayor+0.5)*10)
		turtle.seth(90)
		turtle.backward((dmenor+0.5)*10)
		prevSample = False

	elif qactual[0] == 'trio': #Operacion triangulo
		if int(qactual[1]) >= 40000:
			b = getDirData(getDirData(int(qactual[1])))*5 #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			b = getDirData(int(qactual[1]))*5 #Obtiene el valor de la direccion colocada en el cuadruplo.
		if int(qactual[2]) >= 40000:
			h = getDirData(getDirData(int(qactual[2])))*5
		else:
			h = getDirData(int(qactual[2]))*5
		ang = math.degrees(math.atan(h/(b/2))) #Usando ley de la contangente, se calcula el angulo que dirige la base
		l = math.sqrt(h**2 + (b/2)**2) #Se obtiene la longitud de los lados laterales.
		turtle.pensize(5);
		turtle.pencolor(getDarkColor(qactual[3]))
		turtle.fillcolor(getColor(qactual[3]))
		turtle.fill(True)
		turtle.seth(90)
		turtle.left(90-ang)
		turtle.forward(l) #Primer trazo
		turtle.left(ang*2)
		turtle.forward(l) #Segundo trazo
		turtle.left(180-ang)
		turtle.forward(b) #Tercer trazo
		turtle.fill(False)
		prevSample = False

	elif qactual[0] == 'quad': #Operacion cuadrado
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
			turtle.left(90) #Primer y tercer trazo
			turtle.forward(base)
			turtle.left(90) #Segundo y cuarto trazo
		turtle.fill(False)
		prevSample = False

	elif qactual[0] == 'arr' or qactual[0] == 'mat': #Operacion arreglo o matriz
		ini = int(qactual[1])
		#Ciclo que inicializa valores por defecto en la asignacion de arreglos y matrices
		if ini >= 6000:
			data = False
		elif ini >= 4000:
			data = 0.0
		elif ini >= 2000:
			data = 0
		i = 0
		while i < int(qactual[3]):
			addDirData(int(qactual[1])+i, data) #Se almacenan los datos en memoria de acuerdo al tamanio de la variable dimensionada
			i = i + 1

	elif qactual[0] == 'ver': #Operacion verifica
		tmp = getDirData(int(qactual[1]))
		if tmp < 0 or tmp > int(qactual[3]):
			senderror(2) #Lanza mensaje de error en caso que la indexacion excede del espacio dimensionado.

	elif qactual[0] == 'input': #Operacion input
		i = raw_input('input> ')
		if qactual[1] == 'int':
			try:
				i = int(i)
			except ValueError:
				senderror(4, qactual[1]) #Lanza mensaje de error si se recibe un tipo incorrecto.
		elif qactual[1] == 'float':
			try:
				i = float(i)
			except ValueError:
				senderror(4, qactual[1]) #Lanza mensaje de error si se recibe un tipo incorrecto.
		elif qactual[1] == 'bool':
			try:
				i = bool(i)
			except ValueError:
				senderror(4, qactual[1]) #Lanza mensaje de error si se recibe un tipo incorrecto.

		if int(qactual[3]) >= 40000:
			data = getDirData(int(qactual[3])) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			data = int(qactual[3]) #Obtiene el valor de la direccion colocada en el cuadruplo.
		addDirData(data, i)

	elif qactual[0] == 'random': #Operacion random
		if int(qactual[2]) >= 40000:
			limite = getDirData(getDirData(int(qactual[2])))
		else:
			limite = getDirData(int(qactual[2]))
		if qactual[1] == 'int':
			val = random.randrange(0, limite) #Genera un valor aleatorio a partir de 0 hasta el valor previo al limite establecido
		elif qactual[1] == 'float':
			val = round(random.uniform(0, limite),2) #Genera un valor aleatorio flotante a partir de 0 hasta el valor previo al limite establecido

		if int(qactual[3]) >= 40000:
			data = getDirData(int(qactual[3]))
		else:
			data = int(qactual[3])
		addDirData(data, val)

	elif qactual[0] == 'echo': #Operacion echo
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1])))
		else:
			tmp = getDirData(int(qactual[1]))
		tmp1 = str(tmp)
		esstring = re.compile(pattn_string)
		if re.match(esstring, tmp1):
			tmp1 = tmp.split("\"")
			print "----->", tmp1[1] #Despliega una constante de texto
		else:
			print "----->", tmp #Despliega una variable de tipo entero, flotante o booleano

	elif qactual[0] == '+dir': #Operacion suma direccion base
		tmp = getDirData(int(qactual[1])) + int(qactual[2]) #Suma el valor de la direccion base y la casilla correspondiente.
		addDirData(int(qactual[3]), tmp) #Se guarda el apuntador a dimension en la memoria

	elif qactual[0] == 'goTo': #Operacion salto
		ip = int(qactual[3]) - 2

	elif qactual[0] == 'goToF': #Operacion de salto en falso
		if getDirData(int(qactual[1])) == False:
			ip = int(qactual[3]) - 2

	elif qactual[0] == 'era': #Operacion era / reservacion de memoria
		actual = directory[qactual[1]] #Obtiene el directorio actual del procedimiento
		memoria.newLocalMemory(actual[2], actual[3], actual[4], actual[5], actual[6], actual[7], actual[8]) #Crear un nuevo espacio de memoria nueva
		if directory[qactual[1]][0] != None:
			parametros = directory[qactual[1]][0] #Recibe la lista de parametros del modulo
		else:
			parametros = [] #Si no hay parametros que enviar la lista es nula
		num_parametros = 0 #Inicializa el contador de parametros
		paramint = 12000
		paramfloat = 14000
		parambool = 16000

	elif qactual[0] == 'param': #Operacion paso de parametros
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1])))
		else:
			tmp = getDirData(int(qactual[1]))
		if parametros[num_parametros] == 'int':
			addParamData(paramint, tmp) #Aniade a la memoria nueva una variable de tipo entero
			paramint = paramint + 1
		elif parametros[num_parametros] == 'float':
			addParamData(paramfloat, tmp) #Aniade a la memoria nueva una variable de tipo flotante
			paramfloat = paramfloat + 1
		elif parametros[num_parametros] == 'bool':
			addParamData(parambool, tmp) #Aniade a la memoria nueva una variable de tipo booleano
			parambool = parambool + 1
		num_parametros += 1

	elif qactual[0] == 'gosub': #Operacion salto a modulo
		if current_scope != "*work*":
			memoria.sleepLocalMemory() #Si el ambito actual no es la memoria global, se duerme la memoria local en procedimiento.
		memoria.addIP([ip, current_scope]) #Se guarda el IP correspondiente a la invocacion para su proxima continuacion.
		memoria.setLocalMemory() #La memoria nueva se inicializa como nueva memoria local
		current_scope = qactual[1] #Se establece el nuevo scope a trabajar los cuadruplos
		direcmod = directory[qactual[1]][1] #Se obtiene el cuadruplo de inicio de modulo
		ip = direcmod - 2

	elif qactual[0] == 'ret': #Operacion ret
		memoria.freeLocalMemory() #Libera la memoria local
		ipscope = memoria.getIP() #Obtiene el IP que realizo la ultima llamada
		if ipscope[1] != "*work*":
			memoria.awakeLocalMemory() #Si el scope es diferente al workspace, se manda llamar a un segmento previo de memoria local.
		ip = ipscope[0]
		current_scope = ipscope[1] #Se establece el nuevo scope actual.

	elif qactual[0] == 'return': #Operacion return
		if int(qactual[1]) >= 40000:
			tmp = getDirData(getDirData(int(qactual[1]))) #Obtiene el valor de la direccion del apuntador en referencia.
		else:
			tmp = getDirData(int(qactual[1])) #Obtiene el valor de la direccion dado por el cuadruplo.
		if int(qactual[3]) >= 40000:
			data = getDirData(int(qactual[3]))
		else:
			data = int(qactual[3])
		addDirData(data, tmp) #Aniade el valor de retorno al espacio de memoria global
		memoria.freeLocalMemory() #Libera la memoria local
		ipscope = memoria.getIP() #Obtiene el IP que realizo la ultima llamada
		if ipscope[1] != "*work*":
			memoria.awakeLocalMemory() #Si el scope es diferente al workspace, se manda llamar a un segmento previo de memoria local.
		ip = ipscope[0]
		current_scope = ipscope[1] #Se establece el nuevo scope actual.

	
	#Condicionante del cursor de tipo espejo, si el cursor sale del canvas por un lado particular, entra nuevamente por el lado inverso.
	if (turtle.pos()[0] < -turtle.screensize()[0]):
		turtle.hideturtle()
		turtle.penup()
		turtle.goto(turtle.screensize()[0], turtle.pos()[1])
		turtle.showturtle()
	elif (turtle.pos()[0] > turtle.screensize()[0]):
		turtle.hideturtle()
		turtle.penup()
		turtle.goto(-turtle.screensize()[0], turtle.pos()[1])
		turtle.showturtle()
	elif (turtle.pos()[1] > turtle.screensize()[1]):
		turtle.hideturtle()
		turtle.penup()
		turtle.goto(turtle.pos()[0], -turtle.screensize()[1])
		turtle.showturtle()
	elif (turtle.pos()[1] < -turtle.screensize()[1]):
		turtle.hideturtle()
		turtle.penup()
		turtle.goto(turtle.pos()[0], turtle.screensize()[1])
		turtle.showturtle()
	
	ip = ip + 1
turtle.hideturtle()
turtle.done()