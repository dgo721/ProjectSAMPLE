# LEX

import sys, copy
sys.path.insert(0,"../..")

from error import senderror

if sys.version_info[0] >= 3:
    raw_input = input

reserva = {
    'init' : 'INIT',
    'end' : 'END',
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'and' : 'AND',
    'or' : 'OR',
    'input' : 'INPUT',
    'echo' : 'ECHO',
    'sample' : 'SAMPLE',
    'on' : 'ON',
    'off' : 'OFF',
    'mod' : 'MOD',
    'return' : 'RETURN',
    'oval' : 'OVAL',
    'trio' : 'TRIO',
    'quad' : 'QUAD',
    'arc' : 'ARC',
    'up' : 'UP',
    'down' : 'DOWN',
    'left' : 'LEFT',
    'right' : 'RIGHT',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'replay' : 'REPLAY',
    'arr' : 'ARR',
    'mat' : 'MAT',
    'rand' : 'RAND',
    'red' : 'RED',
    'yellow' : 'YELLOW',
    'green' : 'GREEN',
    'blue' : 'BLUE',
    'orange' : 'ORANGE',
    'black' : 'BLACK',
    'white' : 'WHITE',
    'purple' : 'PURPLE',
    'cyan' : 'CYAN',
}

tokens = ['CTE_INTEGER','CTE_FLOAT', 'CTE_STRING','ID'] + list(reserva.values())

literals = [',',';','*','/', '(',')','[',']','{','}','+','-','=','<','>','#']

linenumber = 0;

#TOKENS

def t_ID(t): #Recibe IDs
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserva.get(t.value,'ID') # Checa palabras reservadas
    return t

t_CTE_STRING = r'\".*?\"'

def t_CTE_FLOAT(t): #Recibe flotantes
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_CTE_INTEGER(t): #Recibe enteros
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_COMMENT(t): #Recibe/Ignora comentarios
    r'\/\/.*'
    pass

def t_newline(t): #Recibe el salto de linea
    r'\n+'
    global linenumber
    t.lexer.lineno += len(t.value)
    linenumber = t.lexer.lineno

def t_error(t): #Salida de error por caracter ilegal
    print("ERROR // Ilegar character '%s'" % t.value[0])
    print "-LINE //", linenumber
    sys.exit()
    t.lexer.skip(1)
    
# Construye LEX
from ply import lex
lex.lex()

# Parser

precedence = (
    ('left','+','-'),
    ('left','*','/'),
)

def p_program(p):
    '''program : INIT programA'''
    global id_params, dir_modulos, work_vars, tab_valores, pairs_idtype
    
    while (pairs_idtype):
    	par = pairs_idtype.pop(0)
    	tab_valores=tabvar(tab_valores, par[0], par[1], par[2], linenumber)#Almacena las variables correpondientes al ambito global
    
    #Adjunta el workspace al directorio de modulos
    dir_modulos = dirmod(dir_modulos, "*work*", [], work_vars[0]+work_offs[0], work_vars[1]+work_offs[1], work_vars[2]+work_offs[2], tab_valores, None, work_tvars[0], work_tvars[1], work_tvars[2], work_point, tab_temporal, tab_pointer, None, None)

def p_programA(p):
    '''programA : programB END
                | END'''
    quads_gen.addGoTo('end', -1, -1, -1) #Aniade cuadruplo de salida

def p_programB(p):
    '''programB : workspace programC'''

def p_programC(p):
    '''programC : programB
            | empty'''

def p_workspace(p):
    '''workspace : statute
            | module'''
    global cont_vars, cont_tvars, cont_offs
    #Reinicia variables de contadores locales
    cont_vars = [0,0,0]
    cont_tvars = [0,0,0]
    cont_offs = [0,0,0]

def p_statute(p):
    '''statute : assign
                | condition
                | read
                | write
                | cycle
                | repeat
                | command
                | calling
                | array
                | matrix
                | random
                | return'''
    global assign_vars
    #Reinicia pila de operandos
    assign_vars=[]

def p_typeMod(p):
	'''typeMod : INT
			| FLOAT
			| BOOL
			| empty'''
	global tipomod, has_return
	p[0] = p[1]
	tipomod = p[1]
	if p[1] != None:
		has_return = True #Prende la bandera de retorno del modulo

def p_addMod(p):
	'''addMod : '''
	global tipomod, nombremod, tab_valores, work_vars
    #Aniade el modulo como una variable global
	if tipomod == 'int':
		tab_valores = tabvar(tab_valores, nombremod, vartipo_mod(tipomod), 0, linenumber)
	elif tipomod == 'float':
		tab_valores = tabvar(tab_valores, nombremod, vartipo_mod(tipomod), 0, linenumber)
	elif tipomod == 'bool':
		tab_valores = tabvar(tab_valores, nombremod, vartipo_mod(tipomod), 0, linenumber)

def p_module(p):
    '''module : MOD typeMod '#' moduleID addMod insertQuadMod moduleA endMod'''
    global id_params, cont_vars, cont_point, dir_modulos, list_params, work_vars, work_point, tab_valores, tab_lvalores, tab_ltemporal, tab_lpointer, pairs_idtype, flagTabTemp, has_return, find_return, cont_offs, work_offs
    if has_return == True and find_return == False:
    	senderror(19, linenumber, p[4]) #Salida de error al no encontrar el return cuando se esperaba.
    if has_return == False and find_return == True:
    	senderror(20, linenumber, p[4]) #Salida de error al encontrar el return cuando no se esperaba.
    dir_modulos = removedirmod(dir_modulos, p[4]) #Remueve el directorio temporal
    x = sum(work_vars) - sum(cont_vars) #Calcula la diferencia de variables encontradas de ambito local sobre ambito global.
    suma = sum(work_vars)
    while (x < suma and pairs_idtype): #Mientras se tengan variables en ambito local
    	par = pairs_idtype.pop(x) #Se saca la variable de la lista auxiliar.
    	tab_lvalores=tabvar(tab_lvalores, par[0], par[1], par[2], linenumber) #Se aniade el la variable a la tabla con su tipo y dimension
    	suma = suma - 1
    #El modulo es entregado al directorio de modulos
    dir_modulos = dirmod(dir_modulos, p[4], list_params, cont_vars[0]+cont_offs[0], cont_vars[1]+cont_offs[1], cont_vars[2]+cont_offs[2], copy.deepcopy(tab_lvalores), quad_mod, cont_tvars[0], cont_tvars[1], cont_tvars[2], cont_point, copy.deepcopy(tab_ltemporal), copy.deepcopy(tab_lpointer), p[2], line_mod)
    list_params=[] #Reinicia lista de parametros
    id_params=[] #Reinicia lista de parametros
    #Se actualizan los contadores globales.
    work_vars[0] = work_vars[0] - cont_vars[0]
    work_vars[1] = work_vars[1] - cont_vars[1]
    work_vars[2] = work_vars[2] - cont_vars[2]
    work_tvars[0] = work_tvars[0] - cont_tvars[0]
    work_tvars[1] = work_tvars[1] - cont_tvars[1]
    work_tvars[2] = work_tvars[2] - cont_tvars[2]
    work_offs[0] = work_offs[0] - cont_offs[0]
    work_offs[1] = work_offs[1] - cont_offs[1]
    work_offs[2] = work_offs[2] - cont_offs[2]
    work_point = work_point - cont_point
    cont_vars = [0,0,0] #Reinicia contador
    cont_point = 0 #Reinicia contador
    quads_gen.addcontinueG() #Se aniade el salto al cuatro goto previo al modulo
    quads_gen.setScope("*work*") #Se establece el workspace a scope
    flagTabTemp = False #Se apaga la bandera de tabla temporal / local
    has_return = False #Se apaga la bandera de retorno
    find_return = False #Se apaga la bandera de encuentra retorno
    tab_lvalores = TabVars(12000, 14000, 16000) #Reinicializan tablas de valores
    tab_ltemporal = TabVars(32000, 34000, 36000) #Reinicializan tablas de temporales
    tab_lpointer = TabPointer(42000) #Reinicializan tablas de apuntadores
    tab_ldims = TabDims()

def p_moduleA(p):
    '''moduleA : '(' vars ')' block
            | block'''

def p_moduleID(p):
    '''moduleID : ID'''
    global flagTabTemp, line_mod, dir_modulos, nombremod
    flagTabTemp = True
    line_mod = linenumber
    dir_modulos = tempdirmod(dir_modulos, p[1], list_params) #Se aniade el modulo temporalmente al directorio
    quads_gen.addGoTo('goTo', -1, -1, -1) #Se establece un salto goTo
    quads_gen.setScope(p[1]) #Se establece el scope al modulo senialado
    nombremod = p[1]
    p[0] = p[1]

def p_vars(p):
    '''vars : type ID varsA'''
    global id_type, tab_lvalores, id_params, pairs_idtype
    id_params.append(p[2]) #Guarda el ID del parametro
    tipo1 = vartipo_mod(id_type.pop())
    if tipo1 == 0:
        cont_vars[0] = cont_vars[0] + 1
        work_vars[0] = work_vars[0] + 1
    elif tipo1 == 1:
        cont_vars[1] = cont_vars[1] + 1
        work_vars[1] = work_vars[1] + 1
    elif tipo1 == 2:
        cont_vars[2] = cont_vars[2] + 1
        work_vars[2] = work_vars[2] + 1
    pairs_idtype.append([p[2], tipo1, 0]) #Aniade el par id-tipo a la lista de variables

def p_varsA(p):
    '''varsA : ',' vars
             | empty'''

def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL'''
    global id_type, list_params
    list_params.append(p[1]) #Aniade el tipo a la secuencia
    id_type.append(p[1]) #Aniade a la lista de tipos de parametros, sea INT, FLOAT, BOOL

def p_id(p):
	'''id : ID initdim '[' sumdim exp ']' '[' sumdim exp ']'
		| ID initdim '[' sumdim exp ']' 
		| callID initdim '#' calling2
		| ID initdim empty'''
	global es_dim, pilaOpera, pilaTipos, quads_gen, tab_temporal, tab_ltemporal, tab_pointer, tab_lpointer, cont_point, work_point, list_dims, flag_dim
	p[0] = [p[1], None]
	flag = flag_dim.pop() #Toma la bandera del ultimo id evaluado.
	es_dim = 0
	if flag == True:
		es_dim = list_dims.pop() #Toma la dimension del utlimo id no atomico
	if p[3] == '#' and tab_valores.lookup(p[1]) == True:
		p[0] = [p[1], 'mod', tab_valores.getType(p[1])] #Devuelve el id y el tipo de dato una llamada
	elif p[3] == '#' and dir_modulos.lookup(p[1]) == False:
		senderror(7, linenumber, p[1]) #Salida de error cuando se hace una llamada a un modulo que no existe
	if es_dim > 0 and tab_dims.getDim(p[1]) == -1:
		senderror(16, linenumber, p[1]) #Salida de error cuando se accesa una variable como dimensionada siendo atomica
	if es_dim != tab_dims.getDim(p[1]) and tab_dims.getDim(p[1]) != -1:
		if tab_dims.getDim(p[1]) == 2:
			senderror(13, linenumber, p[1]) #Salida de error cuando una variable se accesa como arreglo siendo matriz
		elif tab_dims.getDim(p[1]) == 1:
			senderror(14, linenumber, p[1]) #Salida de error cuando una variable se accesa como matriz siendo arreglo
	if tab_dims.getDim(p[1]) == 1:
		oper = pilaOpera.pop()
		tipo = pilaTipos.pop()
		if flagTabTemp == True:
			templist = quads_gen.addVer1(oper, p[1], tab_dims.getLimit1(p[1]), tab_lpointer) #Se realizan los cuadruplos de acceso a variable dimensionada
			tab_lpointer = templist[0] #Se actualiza la tabla de apuntadores locales
			cont_point = cont_point + 1
			work_point = work_point + 1
		else:
			templist = quads_gen.addVer1(oper, p[1], tab_dims.getLimit1(p[1]), tab_pointer) #Se realizan los cuadruplos de acceso a variable dimensionada
			tab_pointer = templist[0] #Se actualiza la tabla de apuntadores globales
			cont_point = cont_point + 1
			work_point = work_point + 1
		p[0] = [p[1], templist[1]]
	elif tab_dims.getDim(p[1]) == 2:
		oper2 = pilaOpera.pop()
		oper1 = pilaOpera.pop()
		tipo2 = pilaTipos.pop()
		tipo1 = pilaTipos.pop()
		if flagTabTemp == True:
			templist = quads_gen.addVer2(oper1, oper2, p[1], tab_dims.getLimit1(p[1]), tab_dims.getLimit2(p[1]), tab_lpointer, tab_ltemporal, linenumber) #Se realizan los cuadruplos de acceso a variable dimensionada
			tab_lpointer = templist[0] #Se actualiza la tabla de apuntadores locales
			tab_ltemporal = templist[1] #Se actualiza la tabla de temporales globales
			cont_tvars[0] = cont_tvars[0] + 2
			work_tvars[0] = work_tvars[0] + 2
			cont_point = cont_point + 1
			work_point = work_point + 1
		else:
			templist = quads_gen.addVer2(oper1, oper2, p[1], tab_dims.getLimit1(p[1]), tab_dims.getLimit2(p[1]), tab_pointer, tab_temporal, linenumber) #Se realizan los cuadruplos de acceso a variable dimensionada
			tab_pointer = templist[0] #Se actualiza la tabla de apuntadores globales
			tab_temporal = templist[1] #Se actualiza la tabla de temporales globales
			cont_tvars[0] = cont_tvars[0] + 2
			work_tvars[0] = work_tvars[0] + 2
			cont_point = cont_point + 1
			work_point = work_point + 1
		p[0] = [p[1], templist[2]]
	es_dim = 0

def p_initdim(p):
	'''initdim : '''
	global flag_dim, es_dim
	esdim = 0
	flag_dim.append(False) #Se aniade una bandera en falso

def p_sumdim(p):
	'''sumdim : '''
	global es_dim, list_dims, flag_dim
	flag = flag_dim.pop()
	if flag == False:
		flag = True
		es_dim = es_dim + 1
		flag_dim.append(flag) #Se aniade la bandera con valor de verdadero
		list_dims.append(es_dim) #Se aniade el valor actual de dimension
	else:
		es_dim = list_dims.pop()
		es_dim = es_dim + 1
		flag_dim.append(flag)
		list_dims.append(es_dim) #Se aniade el nuevo valor de dimension

def p_calling(p):
	'''calling : '#' callID calling2 ';' '''

def p_calling2(p):
	'''calling2 : '(' maincalling ')' '''
	global lista_params
	if (xparam + 1) != len(lista_params):
		senderror(9, linenumber, id_mod, len(lista_params)) #Salida de error cuando se excede o faltan parametros en un modulo
	quads_gen.addQ('gosub',id_mod,-1,-1) #Se coloca el cuadruplo de rutina gosub
	lista_params = []

def p_maincalling(p):
    '''maincalling : insertEra callingA'''

def p_callID(p):
    '''callID : ID'''
    global id_mod
    if dir_modulos.lookup(p[1]) == False:
    	senderror(7, linenumber, p[1]) #Salida de error se quiere hacer una llamada a un modulo no declarado
    id_mod = p[1]
    p[0] = p[1]

def p_insertEra(p):
    '''insertEra : '''
    global lista_params
    quads_gen.addQ('era',id_mod,-1,-1) #Se coloca el cuadruplo ERA
    lista_params = dir_modulos.getParamsNum(id_mod) #Se pide la lista de parametros a revisar
    if len(lista_params) != 0:
    	xparam = 0
    else:
    	xparam = -1

def p_callingA(p):
    '''callingA : callingB
                | empty '''

def p_callingB(p):
    '''callingB : exp checkParam callingC'''

def p_checkParam(p):
    '''checkParam : '''
    global lista_params
    argum = pilaOpera.pop()
    tipo = pilaTipos.pop()
    if xparam >= len(dir_modulos.getParamsNum(id_mod)):
    	senderror(9, linenumber, id_mod, len(dir_modulos.getParamsNum(id_mod)))
    if lista_params[xparam] == tipo:
    	prm = "param" + str(xparam + 1)
    	quads_gen.addQ('param',argum,-1,prm) #Coloca un cuadruplo para registro de parametro
    else:
    	senderror(8, linenumber, invartipo_mod(lista_params[xparam])) #Salida de error cuando se introduce un dato de tipo incorrecto

def p_callingC(p):
    '''callingC : ',' sumXparam callingB
            | empty '''

def p_sumXparam(p):
	'''sumXparam : '''
	global xparam
	xparam = xparam + 1 #Se posiciona en el siguiente parametro

def p_block(p):
    '''block : '{' blockA '''

def p_blockA(p):
    '''blockA : blockB '}'
                | '}' '''

def p_blockB(p):
    '''blockB : statute blockC'''

def p_blockC(p):
    '''blockC : blockB
                | empty'''

def p_assign(p):
    '''assign : id '=' expression ';' '''
    global tab_valores, pilaOpera, pilaTipos, quads_gen, cont_vars, work_vars, pairs_idtype
    valor1 = pilaOpera.pop() #Obtiene el valor del operando
    tipo1 = pilaTipos.pop() #Obtiene el tipo del operando
    index = vartipo_assign(assign_vars) #Verifica que tipo de dato se espera guardar
    if tipo1 != index:
    	senderror(3, linenumber, p[1][0]) #Salida de error por asignacion incorrecta.
    if tipo1 == 0:
        cont_vars[0] = cont_vars[0] + 1
        work_vars[0] = work_vars[0] + 1
    elif tipo1 == 1:
        cont_vars[1] = cont_vars[1] + 1
        work_vars[1] = work_vars[1] + 1
    elif tipo1 == 2:
        cont_vars[2] = cont_vars[2] + 1
        work_vars[2] = work_vars[2] + 1
    pairs_idtype.append([p[1][0], tipo1, 0]) #Aniade el par id-tipo a la lista de variables
    if p[1][1] == None:
    	quads_gen.add('=', valor1, -1, p[1][0]) #Aniade el cuadruplo de asignacion
    else:
    	quads_gen.add('=', valor1, -1, p[1][1]) #Aniade el cuadruplo de asignacion en variable dimensionada


def p_condition(p):
    '''condition : IF '(' expression ')' gotoFalse block conditionA continueGo'''

def p_conditionA(p):
    '''conditionA : ELSE gotoE block
                | empty '''

def p_random(p):
    '''random : RAND typeRand ID CTE_INTEGER ';' '''
    global quads_gen, cont_vars, work_vars, pairs_idtype, tab_constant
    tipo = vartipo_mod(p[2])
    if tipo == 0:
        cont_vars[0] = cont_vars[0] + 1
        work_vars[0] = work_vars[0] + 1
    elif tipo == 1:
        cont_vars[1] = cont_vars[1] + 1
        work_vars[1] = work_vars[1] + 1
    tab_constant = tabconstante(tab_constant, p[4])
    pairs_idtype.append([p[3], tipo, 0])
    quads_gen.addQ('random', p[2], p[4], p[3])

def p_typeRand(p):
    '''typeRand : INT
                | FLOAT'''
    p[0] = p[1]

def p_read(p):
    '''read : INPUT typeDim ID '#' ';' '''
    global quads_gen, cont_vars, work_vars, pairs_idtype
    tipo = vartipo_mod(p[2])
    if tipo == 0:
        cont_vars[0] = cont_vars[0] + 1
        work_vars[0] = work_vars[0] + 1
    elif tipo == 1:
        cont_vars[1] = cont_vars[1] + 1
        work_vars[1] = work_vars[1] + 1
    elif tipo == 2:
        cont_vars[2] = cont_vars[2] + 1
        work_vars[2] = work_vars[2] + 1
    pairs_idtype.append([p[3], tipo, 0]) #Aniade el par id-tipo a la lista de variables
    quads_gen.addQ('input', p[2], -1, p[3]) #Aniade el cuadruplo de input

def p_write(p):
    '''write : ECHO '(' writeA writeB ')' ';' '''

def p_writeA(p):
    '''writeA : expression
            | CTE_STRING'''
    global tab_constant
    if p[1] != None:
    	tab_constant = tabconstante(tab_constant, p[1]) #Aniade la constante string a la tabla de constantes
    	quads_gen.addQ('echo', p[1], -1, -1) #Aniade el cuadruplo de escritura
    else:
    	pilaTipos.pop()
    	quads_gen.addQ('echo', pilaOpera.pop(), -1, -1) #Aniade el cuadruplo de escritura

def p_writeB(p):
    '''writeB : ',' writeA
                | empty'''

def p_array(p):
	'''array : ARR typeDim ID '[' CTE_INTEGER ']' ';' '''
	global pairs_idtype, tab_constant, tab_dims, cont_vars, work_vars, cont_offs, work_offs
	if flagTabTemp == True:
		if tab_ldims.isDuplicate(p[3]) != -1:
			senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3])) #Salida de error dado que el arreglo ya fue asignado previamente
	else:
		if tab_dims.isDuplicate(p[3]) != -1:
			senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3])) #Salida de error dado que el arreglo ya fue asignado previamente
	if p[5] < 1:
		senderror(12, linenumber-1) #Salida de error cuando se inicializa un arreglo de tamanio 0
	r = p[5] #Equivalente a R = (Ls - Li) * R, R = 1
	tipo1 = vartipo_mod(p[2])
	if tipo1 == 0:
		cont_vars[0] = cont_vars[0] + 1
		work_vars[0] = work_vars[0] + 1
		cont_offs[0] = cont_offs[0] + r - 1
		work_offs[0] = work_offs[0] + r - 1
	elif tipo1 == 1:
		cont_vars[1] = cont_vars[1] + 1
		work_vars[1] = work_vars[1] + 1
		cont_offs[1] = cont_offs[1] + r - 1
		work_offs[1] = work_offs[1] + r - 1
	elif tipo1 == 2:
		cont_vars[2] = cont_vars[2] + 1
		work_vars[2] = work_vars[2] + 1
		cont_offs[2] = cont_offs[2] + r - 1
		work_offs[2] = work_offs[2] + r - 1
	tab_constant = tabconstante(tab_constant, p[5])
	tab_constant = tabconstante(tab_constant, p[5]-1)
	pairs_idtype.append([p[3], tipo1, r]) #Aniade el par id-tipo a la lista de variables
	if flagTabTemp == True:
		tab_ldims.add(p[3], 1, p[5]-1, -1) #Se coloca el id con sus respectivas dimensiones en la tabla local
	else:
		tab_dims.add(p[3], 1, p[5]-1, -1) #Se coloca el id con sus respectivas dimensiones en la tabla
	quads_gen.addQ('arr', p[3], -1, r) #Se coloca el cuadruplo de asignacion de arreglo

def p_matrix(p):
	'''matrix : MAT typeDim ID '[' CTE_INTEGER ']' '[' CTE_INTEGER ']' ';' '''
	global pairs_idtype, tab_constant, tab_dims, cont_vars, work_vars
	if flagTabTemp == True:
		if tab_ldims.isDuplicate(p[3]) != -1:
			senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3])) #Salida de error dado que la matriz ya fue asignado previamente
	else:
		if tab_dims.isDuplicate(p[3]) != -1:
			senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3])) #Salida de error dado que la matriz ya fue asignado previamente
	if p[5] < 1 or p[8] < 1:
		senderror(12, linenumber-1) #Salida de error cuando se inicializa una matriz de tamanio 0
	r = p[5] * p[8] #Equivalente a 2 veces R = (Ls - Li) * R, R = 1
	tipo1 = vartipo_mod(p[2])
	if tipo1 == 0:
		cont_vars[0] = cont_vars[0] + 1
		work_vars[0] = work_vars[0] + 1
		cont_offs[0] = cont_offs[0] + r - 1
		work_offs[0] = work_offs[0] + r - 1
	elif tipo1 == 1:
		cont_vars[1] = cont_vars[1] + 1
		work_vars[1] = work_vars[1] + 1
		cont_offs[1] = cont_offs[1] + r - 1
		work_offs[1] = work_offs[1] + r - 1
	elif tipo1 == 2:
		cont_vars[2] = cont_vars[2] + 1
		work_vars[2] = work_vars[2] + 1
		cont_offs[2] = cont_offs[2] + r - 1
		work_offs[2] = work_offs[2] + r - 1
	tab_constant = tabconstante(tab_constant, p[5])
	tab_constant = tabconstante(tab_constant, p[5]-1)
	tab_constant = tabconstante(tab_constant, p[8])
	tab_constant = tabconstante(tab_constant, p[8]-1)
	pairs_idtype.append([p[3], tipo1, r]) #Aniade el par id-tipo a la lista de variables
	if flagTabTemp == True:
		tab_ldims.add(p[3], 2, p[5]-1, p[8]-1) #Se coloca el id con sus respectivas dimensiones en la tabla local
	else:
		tab_dims.add(p[3], 2, p[5]-1, p[8]-1) #Se coloca el id con sus respectivas dimensiones en la tabla
	quads_gen.addQ('mat', p[3], -1, r) #Se coloca el cuadruplo de asignacion de matriz

def p_typeDim(p):
    '''typeDim : INT
                | FLOAT
                | BOOL'''
    p[0] = p[1]

def p_command(p):
    '''command : figure exp exp color ';'
            | SAMPLE commandA '''
    global quads_gen, pilaOpera, pilaTipos
    if p[1] == 'sample':
    	if p[2][0] == 'on':
    		quads_gen.addQ('sample1', p[2][3], p[2][4], -1) #Se coloca el cuadruplo1 de dibujo
    		quads_gen.addQ('sample2', p[2][0], p[2][1], p[2][2]) #Se coloca el cuadruplo2 de dibujo
    	elif p[2][0] == 'off':
			quads_gen.addQ('sample', p[2][0], p[2][1], p[2][2]) #Se coloca el cuadruplo de cursor
    else:
    	tipo2 = pilaTipos.pop()
    	tipo1 = pilaTipos.pop()
    	if tipo1 == 2 or tipo2 == 2:
    		senderror(10, linenumber-1) #Salida de error si se recibe un tipo de dato booleano
    	valor2 = pilaOpera.pop()
    	valor1 = pilaOpera.pop()
    	quads_gen.addQ(p[1], valor1, valor2, p[4]) #Se coloca el cuadruplo de figura
    
def p_commandA(p):
    '''commandA : ON move exp CTE_INTEGER color ';'
            | OFF move exp ';' '''
    global tab_constant
    if pilaTipos.pop() == 2:
    	senderror(10, linenumber-1) #Salida de error si se recibe un tipo de dato booleano
    if p[1] == 'on':
    	tab_constant = tabconstante(tab_constant, p[4]) #Aniade constantes de dibujo a tabla de constantes
        p[0] = [p[1], p[2], pilaOpera.pop(), p[4], p[5]]
    else:
		p[0] = [p[1], p[2], pilaOpera.pop()]

def p_cycle(p):
    '''cycle : WHILE gotoW '(' expression ')' gotoFalse block continueGoW'''

def p_repeat(p):
    '''repeat : REPLAY CTE_INTEGER gotoR '[' repeatA ']' ';' '''
    global tab_temporal, tab_ltemporal, tab_constant
    tab_constant = tabconstante(tab_constant, 1)
    tab_constant = tabconstante(tab_constant, p[2])
    if flagTabTemp == True:
    	tab_ltemporal=quads_gen.addcontinueR(p[2], tab_ltemporal, linenumber) #Actualiza tabla local de temporales
    else:
    	tab_temporal=quads_gen.addcontinueR(p[2], tab_temporal, linenumber) #Actualiza tabla global de temporales
    cont_tvars[0] = cont_tvars[0] + 1
    work_tvars[0] = work_tvars[0] + 1
    cont_tvars[2] = cont_tvars[2] + 1
    work_tvars[2] = work_tvars[2] + 1

def p_repeatA(p):
    '''repeatA : command repeatB'''

def p_repeatB(p):
    '''repeatB : repeatA
            | empty'''

def p_expression(p):
    '''expression : exp '=' '=' exp
                | exp '<' '>' exp
                | exp '<' '=' exp
                | exp '>' '=' exp
                | exp '>' exp
                | exp '<' exp
                | exp AND exp
                | exp OR exp
                | exp empty'''
    global pilaOpera, pilaTipos, quads_gen, tab_ltemporal, tab_temporal
    if p[2] == '=' or p[2] == '<' or p[2] == '>' or p[2] == 'and' or p[2] == 'or':
        valor2=pilaOpera.pop() #Operando2
        valor1=pilaOpera.pop() #Operando1
        tipo2=pilaTipos.pop() #Tipo2
        tipo1=pilaTipos.pop() #Tipo1
        if p[2] == '=' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 8) #Analisis semantico por cubo
            p[2] = p[2] + p[3]
        elif p[2] == '<' and p[3] == '>':
            tipoNuevo = semant_oper(tipo1, tipo2, 9) #Analisis semantico por cubo
            p[2] = p[2] + p[3]
        elif p[2] == '<' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 6) #Analisis semantico por cubo
            p[2] = p[2] + p[3]
        elif p[2] == '>' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 7) #Analisis semantico por cubo
            p[2] = p[2] + p[3]
        elif p[2] == '<':
        	tipoNuevo = semant_oper(tipo1, tipo2, 4) #Analisis semantico por cubo
    	elif p[2] == '>':
        	tipoNuevo = semant_oper(tipo1, tipo2, 5) #Analisis semantico por cubo
        elif p[2] == 'and':
        	tipoNuevo = semant_oper(tipo1, tipo2, 10) #Analisis semantico por cubo
        elif p[2] == 'or':
        	tipoNuevo = semant_oper(tipo1, tipo2, 11) #Analisis semantico por cubo
        if tipoNuevo != -1:
            if tipoNuevo == 2:
            	cont_tvars[2] = cont_tvars[2] + 1
            	work_tvars[2] = work_tvars[2] + 1
            if flagTabTemp == True:
            	tab_ltemporal=tabvar(tab_ltemporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber) #Actualiza tabla local de temporales
            else:
            	tab_temporal=tabvar(tab_temporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber) #Actualiza tabla global de temporales
            quads_gen.add(p[2], valor1, valor2, -1) #Se aniade cuadruplo de operacion
            pilaOpera.append(quads_gen.lasttemp()) #Inserta nuevo operando
            pilaTipos.append(tipoNuevo) #Inserta nuevo tipo
        else:
            senderror(2, linenumber) #Salida de error por operacion incompatible

def p_exp(p):
    '''exp : exp '+' exp
            | exp '-' exp
            | exp '*' exp
            | exp '/' exp
            | factor empty'''
    global pilaOpera, pilaTipos, quads_gen, tab_ltemporal, tab_temporal
    if p[2] == '+' or p[2] == '-' or p[2] == '*' or p[2] == '/':
        valor2=pilaOpera.pop() #Operando2
        valor1=pilaOpera.pop() #Operando1
        tipo2=pilaTipos.pop() #Tipo2
        tipo1=pilaTipos.pop() #Tipo1
        if p[2] == '+':
            tipoNuevo = semant_oper(tipo1, tipo2, 0) #Analisis semantico por cubo
        elif p[2] == '-':
            tipoNuevo = semant_oper(tipo1, tipo2, 1) #Analisis semantico por cubo
        elif p[2] == '*':
            tipoNuevo = semant_oper(tipo1, tipo2, 2) #Analisis semantico por cubo
        elif p[2] == '/':
            tipoNuevo = semant_oper(tipo1, tipo2, 3) #Analisis semantico por cubo
        if tipoNuevo != -1:
            if tipoNuevo == 0:
            	cont_tvars[0] = cont_tvars[0] + 1
            	work_tvars[0] = work_tvars[0] + 1
            elif tipoNuevo == 1:
            	cont_tvars[1] = cont_tvars[1] + 1
            	work_tvars[1] = work_tvars[1] + 1
            if flagTabTemp == True:
            	tab_ltemporal=tabvar(tab_ltemporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber) #Actualiza tabla local de temporales
            else:
            	tab_temporal=tabvar(tab_temporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber) #Actualiza tabla global de temporales
            quads_gen.add(p[2], valor1, valor2, -1) #Se aniade cuadruplo de operacion
            pilaOpera.append(quads_gen.lasttemp()) #Inserta nuevo operando
            pilaTipos.append(tipoNuevo) #Inserta nuevo tipo
        else:
            senderror(2, linenumber) #Salida de error por operacion incompatible

def p_return(p):
	'''return : RETURN exp ';' '''
	global pilaOpera, pilaTipos, quads_gen, cont_vars, work_vars, find_return
	valor=pilaOpera.pop()
	tipo=pilaTipos.pop()
	if quads_gen.getScope() == "*work*":
		senderror(18, linenumber) #Salida de error por encontrar return en ambito global
	if tipo != vartipo_mod(tipomod):
		senderror(17, linenumber, nombremod, tipomod) #Salida de error por un return de tipo incorrecto
	quads_gen.add('return', valor, -1, nombremod) #Se ingresa cuadruplo de return
	find_return = True

def p_factor(p):
    '''factor : '(' expression ')'
            | var_cte '''
    global listoper, pilaOpera
    if p[1] != '(':
        pilaOpera.append(p[1]) #Se aniade operando a la lista/pila de operandos
    p[0] = p[1]

def p_figure(p):
    '''figure : OVAL
            | TRIO
            | QUAD
            | ARC'''
    p[0] = p[1]

def p_move(p):
    '''move : UP
            | DOWN
            | LEFT
            | RIGHT'''
    p[0] = p[1]

def p_color(p):
    '''color : RED
            | YELLOW
            | BLUE
            | GREEN
            | BLACK
            | WHITE
            | ORANGE
            | PURPLE
            | CYAN'''
    p[0] = p[1]

def p_var_cte(p):
    '''var_cte : id
                | CTE_INTEGER
                | CTE_FLOAT
                | TRUE
                | FALSE'''
    global assign_vars, pilaTipos, tab_constant
    if (type(p[1]) is int):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(0) #Encuentra un entero para asignar
        pilaTipos.append(0)
        p[0] = p[1]
    elif (type(p[1]) is float):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(1) #Encuentra un float para asignar
        pilaTipos.append(1)
        p[0] = p[1]
    elif (p[1] == 'true'):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(2) #Encuentra un boleano para asignar
        pilaTipos.append(2)
        p[0] = p[1]
    elif (p[1] == 'false'):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(2) #Encuentra un boleano para asignar
        pilaTipos.append(2)
        p[0] = p[1]
    else:
        findtipo = buscaID(pairs_idtype, p[1][0]) #Encuentra un id para asignar
        esdimensionada = tab_dims.isDuplicate(p[1][0])
        if p[1][1] == 'mod':
        	findtipo = p[1][2]
        if findtipo == -1:
        	senderror(4, linenumber, p[1][0])
        assign_vars.append(findtipo)
        pilaTipos.append(findtipo)
        if esdimensionada == -1:
        	p[0] = p[1][0]
        else:
        	p[0] = p[1][1]

def p_gotoFalse(p):
	'''gotoFalse : '''
	global pilaOpera, pilaTipos, assign_vars
	if pilaTipos.pop() != 2:
		senderror(5, linenumber)
	assign_vars = []
	quads_gen.addGoTo('goToF', pilaOpera.pop(), -1, -1)

def p_gotoE(p):
	'''gotoE : '''
	quads_gen.addGoToE('goTo', -1, -1, -1)

def p_gotoW(p):
	'''gotoW : '''
	quads_gen.addGoToW()

def p_gotoR(p):
	'''gotoR : '''
	global tab_temporal, tab_ltemporal, tab_constant
	if flagTabTemp == True:
		tab_ltemporal=quads_gen.addGoToR(tab_ltemporal, linenumber)
	else:
		tab_temporal=quads_gen.addGoToR(tab_temporal, linenumber)
	tab_constant = tabconstante(tab_constant, 0)
	cont_tvars[0] = cont_tvars[0] + 1
	work_tvars[0] = work_tvars[0] + 1

def p_continueGo(p):
	'''continueGo : '''
	quads_gen.addcontinueG()

def p_continueGoW(p):
	'''continueGoW : '''
	quads_gen.addcontinueW()

def p_insertQuadMod(p):
	'''insertQuadMod : '''
	global quad_mod
	quad_mod = quads_gen.getnextX()

def p_endMod(p):
	'''endMod : '''
	if has_return == False:
		quads_gen.addQ('ret',-1,-1,-1)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        senderror(1, linenumber, p.value)
    else:
        senderror(1, linenumber, "EOF")


from ply import yacc
yacc.yacc()

from tabvars import *
from tabconst import *
from dirmods import *
from cube_sem import semant_oper
from codegen import CodeGen
from tabdims import TabDims
from tabpointers import TabPointer

pilaTipos = list() #Almacena los tipos encontrados.
pilaOpera = list() #Guarda las variables y contanstes utilizadas para una asignacion
id_type = list() #Para VARS, guarda los tipos de variable encontrados en parametros
id_params = list() #Para MODULE-VARS, guarda los id recibidos como parametros en los modulos
assign_vars = list() #Para ASSIGN, almacena los tipos de variables encontrados en una asignacion
pairs_idtype = list() #Almacena las variables en par id-tipo, utlizados para distincion entre variables locales/globales
list_dims = list() #Almacena si las variables encontradas en las expresiones son de 0, 1 o 2 dimensiones
flag_dim = list() #Indica si se encuentra una variable de dimension en la evaluacion de expresiones/asignaciones
tab_constant = TabConst() #Instancia clase TabConst, tabla de constantes del codigo seleccionado
tab_valores = TabVars(2000, 4000, 6000) #Instancia clase TabVars, tabla de variables del codigo seleccionado
tab_lvalores = TabVars(12000, 14000, 16000) #Instancia clase TabVars, tabla de variables locales, distinta por cada modulo
tab_temporal = TabVars(22000, 24000, 26000) #Instancia clase TabVars, tabla de variables temporales del codigo seleccionado
tab_ltemporal = TabVars(32000, 34000, 36000) #Instancia clase TabVars, tabla de variables temporales locales del codigo seleccionado
tab_pointer = TabPointer(40000) #Instancia clase TabPointer, guarda los apuntadores a direccion dentro de variables dimensionadas
tab_lpointer = TabPointer(42000) #Instancia clase TabPointer, guarda los apuntadores locales a direccion dentro de variables dimensionadas
dir_modulos = DirMods() #Instancia clase DirMods, directorio de modulos del programa
tab_dims = TabDims() #Instancia clase TabDims, almaneca limites de variables dimensionadas
tab_ldims = TabDims() #Instancia clase TabDims, almaneca limites de variables dimensionadas en modulos
quads_gen = CodeGen() #Instancia clase CodeGen, generador de cuadruplos para codigo intermedio
cont_vars = [0,0,0] #Contador de variables en modulos, en el orden entero/flotante/boleano
work_vars = [0,0,0] #Contador de variables en el workspace, en el orden entero/flotante/boleano
cont_tvars = [0,0,0] #Contador de variables en modulos, en el orden entero/flotante/boleano
work_tvars = [0,0,0] #Contador de variables en el workspace, en el orden entero/flotante/boleano
cont_offs = [0,0,0] #Contador de offsets en el modulo, en el orden entero/flotante/boleano
work_offs = [0,0,0] #Contador de offsets en el workspace, en el orden entero/flotante/boleano
cont_point = 0 #Contador de apuntadores en modulos
work_point = 0 #Contador de apuntadores en el workspace
list_params = [] #Lista que almacena el tipo de variables encontrado en los parametros de modulos
lista_params = [] #Lista que almacena el tipo de variables encontrado en los parametros de invocacion
quad_mod = 0 #Almacena el cuadruplo donde comienza un modulo
line_mod = 0 #Almacena el numero de linea donde comienza un modulo
id_mod = "work" #Guarda el id que sera registrado en el cuadruplo ERA
xparam = 0 #Variable entera en funcion de apuntador de parametros
flagTabTemp = False #Indica si almacena valores temporales globales o locales
es_dim = 0 #Variable indica si la variable es atomica, de dimension 1 o dimension 2
nombremod = str() #Guarda el nombre del modulo a colocar en la tabla de variables globales
tipomod = str() #Guarda el tipo del modulo a colocar en la tabla de variables globales
has_return = False #Bandera boleana, indica si un modulo cuenta con valor de retorno
find_return = False #Bandera boleana, indica si se coloca el valor de retorno en el modulo


nodisplay = 0

try:
    if sys.argv[1]:
        Name = str(sys.argv[1])
except:
    Name = "ej/ej17.txt"

try:
    if int(sys.argv[2])==1:
        nodisplay = 1
except:
    nodisplay = 0

s = Name

f = open(s, "r")
lines = f.readlines()
x=0
st=""
for l in lines:
    st=st+lines[x]
    x=x+1
yacc.parse(st)
f.close()

if nodisplay != 1:
	dir_modulos.writeQ()
	tab_constant.writeQ()
	quads_gen.write()
	quads_gen.writeQ(dir_modulos, tab_constant)

