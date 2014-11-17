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
    'echo' : 'ECHO',
    'clear' : 'CLEAR',
    'sample' : 'SAMPLE',
    'on' : 'ON',
    'off' : 'OFF',
    'mod' : 'MOD',
    'oval' : 'OVAL',
    'trio' : 'TRIO',
    'quad' : 'QUAD',
    'arc' : 'ARC',
    'up' : 'UP',
    'down' : 'DOWN',
    'left' : 'LEFT',
    'right' : 'RIGHT',
    'where' : 'WHERE',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'replay' : 'REPLAY',
    'arr' : 'ARR',
    'mat' : 'MAT',
    'pipe' : 'PIPE',
    'in' : 'IN',
    'out' : 'OUT',
    'count' : 'COUNT',
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

def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserva.get(t.value,'ID') # Checa palabras reservadas
    return t

t_CTE_STRING = r'\".*?\"'

def t_CTE_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_CTE_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

#def t_newline(t):
#    r'\r\n+'

def t_COMMENT(t):
    r'\/\/.*'
    pass

def t_newline(t):
    r'\n+'
    global linenumber
    t.lexer.lineno += len(t.value)
    linenumber = t.lexer.lineno

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
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
    	#print "PROGRAM--1 ULTIMO PAR", par, len(pairs_idtype)
    	tab_valores=tabvar(tab_valores, par[0], par[1], par[2], linenumber)
    
    dir_modulos = dirmod(dir_modulos, "*work*", [], work_vars[0], work_vars[1], work_vars[2], tab_valores, None, work_tvars[0], work_tvars[1], work_tvars[2], work_point, tab_temporal, tab_pointer, None)

def p_programA(p):
    '''programA : programB END
                | END'''
    quads_gen.addGoTo('end', -1, -1, -1)

def p_programB(p):
    '''programB : workspace programC'''
    #print "programB", p[1]

def p_programC(p):
    '''programC : programB
            | empty'''
    #print "programC", p[1]

def p_workspace(p):
    '''workspace : statute
            | module'''
    global cont_vars, cont_tvars
    cont_vars = [0,0,0]
    cont_tvars = [0,0,0]

def p_statute(p):
    '''statute : assign
                | condition
                | write
                | cycle
                | repeat
                | command
                | calling
                | array
                | matrix
                | pipeline
                | screen'''
    global assign_vars
    assign_vars=[]

def p_module(p):
    '''module : MOD '#' moduleID insertQuadMod moduleA endMod'''
    global id_params, cont_vars, dir_modulos, list_params, work_vars, tab_lvalores, tab_ltemporal, pairs_idtype, flagTabTemp
    #print "modulo #", p[3]
    #print "MODULE-- suma", sum(cont_vars), sum(work_vars), len(pairs_idtype), sum(work_vars) - sum(cont_vars)
    x = sum(work_vars) - sum(cont_vars)
    suma = sum(work_vars)
    while (x < suma and pairs_idtype):
    	par = pairs_idtype.pop(x)
    	#print "MODULE-- ULTIMO PAR", par, len(pairs_idtype)
    	tab_lvalores=tabvar(tab_lvalores, par[0], par[1], par[2], linenumber)
    	suma = suma - 1

    dir_modulos = dirmod(dir_modulos, p[3], list_params, cont_vars[0], cont_vars[1], cont_vars[2], copy.deepcopy(tab_lvalores), quad_mod, cont_tvars[0], cont_tvars[1], cont_tvars[2], cont_point, copy.deepcopy(tab_ltemporal), copy.deepcopy(tab_lpointer), line_mod)
    list_params=[] #Reinicia lista de parametros
    id_params=[] #Reinicia lista de parametros
    work_vars[0] = work_vars[0] - cont_vars[0]
    work_vars[1] = work_vars[1] - cont_vars[1]
    work_vars[2] = work_vars[2] - cont_vars[2]
    work_tvars[0] = work_tvars[0] - cont_tvars[0]
    work_tvars[1] = work_tvars[1] - cont_tvars[1]
    work_tvars[2] = work_tvars[2] - cont_tvars[2]
    work_point = work_point - cont_point
    cont_vars = [0,0,0] #Reinicia contador
    cont_point = 0
    quads_gen.addcontinueG()
    quads_gen.setScope("*work*")
    flagTabTemp = False
    tab_lvalores = TabVars(12000, 14000, 16000)
    tab_ltemporal = TabVars(32000, 34000, 36000)
    tab_lpointer = TabPointer(42000)

def p_moduleA(p):
    '''moduleA : '(' vars ')' block
            | block'''

def p_moduleID(p):
    '''moduleID : ID'''
    global flagTabTemp, line_mod
    flagTabTemp = True
    line_mod = linenumber
    quads_gen.addGoTo('goTo', -1, -1, -1)
    quads_gen.setScope(p[1])
    p[0] = p[1]

def p_vars(p):
    '''vars : type ID varsA'''
    global id_type, tab_lvalores, id_params, pairs_idtype
    #print p[2]
    id_params.append(p[2])
    #print id_type
    #print id_params
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
    #print "NUEVO ID", p[1]
    pairs_idtype.append([p[2], tipo1, 0])
    #print "MODULEA--",pairs_idtype
    #tab_lvalores = tabvar(tab_lvalores, p[2], vartipo_mod(id_type.pop())) #Aniade a la tabla de valores el par ID, TIPO

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
	'''id : ID '[' sumdim exp ']' '[' sumdim exp ']'
		| ID '[' sumdim exp ']' 
		| ID '''
	global es_dim, pilaOpera, pilaTipos, quads_gen, tab_temporal, tab_ltemporal, tab_pointer, tab_lpointer, cont_point, work_point
	p[0] = [p[1], None]
	print "ID--", es_dim, tab_dims.getDim(p[1])
	if es_dim > 0 and tab_dims.getDim(p[1]) == -1:
		senderror(16, linenumber, p[1])
	if es_dim != tab_dims.getDim(p[1]) and tab_dims.getDim(p[1]) != -1:
		if tab_dims.getDim(p[1]) == 2:
			senderror(13, linenumber, p[1])
		elif tab_dims.getDim(p[1]) == 1:
			senderror(14, linenumber, p[1])
	if tab_dims.getDim(p[1]) == 1:
		oper = pilaOpera.pop()
		tipo = pilaTipos.pop()
		if flagTabTemp == True:
			templist = quads_gen.addVer1(oper, p[1], tab_dims.getLimit1(p[1]), tab_lpointer)
			tab_lpointer = templist[0]
			cont_point = cont_point + 1
			work_point = work_point + 1
		else:
			templist = quads_gen.addVer1(oper, p[1], tab_dims.getLimit1(p[1]), tab_pointer)
			tab_pointer = templist[0]
			cont_point = cont_point + 1
			work_point = work_point + 1
		p[0] = [p[1], templist[1]]
	elif tab_dims.getDim(p[1]) == 2:
		oper2 = pilaOpera.pop()
		oper1 = pilaOpera.pop()
		tipo2 = pilaTipos.pop()
		tipo1 = pilaTipos.pop()
		if flagTabTemp == True:
			templist = quads_gen.addVer2(oper1, oper2, p[1], tab_dims.getLimit1(p[1]), tab_dims.getLimit2(p[1]), tab_lpointer, tab_ltemporal, linenumber)
			tab_lpointer = templist[0]
			tab_ltemporal = templist[1]
			cont_tvars[0] = cont_tvars[0] + 2
			work_tvars[0] = work_tvars[0] + 2
			cont_point = cont_point + 1
			work_point = work_point + 1
		else:
			templist = quads_gen.addVer2(oper1, oper2, p[1], tab_dims.getLimit1(p[1]), tab_dims.getLimit2(p[1]), tab_pointer, tab_temporal, linenumber)
			tab_pointer = templist[0]
			tab_temporal = templist[1]
			cont_tvars[0] = cont_tvars[0] + 2
			work_tvars[0] = work_tvars[0] + 2
			cont_point = cont_point + 1
			work_point = work_point + 1
		p[0] = [p[1], templist[2]]
	es_dim = 0

def p_sumdim(p):
	'''sumdim : '''
	global es_dim
	es_dim += 1

def p_calling(p):
    '''calling : '#' callID '(' insertEra callingA'''
    quads_gen.addQ('gosub',id_mod,-1,-1)
    list_params = []
    #print dir_modulos.getParams(p[2])
    #print "CALLING", assign_vars

def p_callID(p):
    '''callID : ID'''
    global id_mod
    if dir_modulos.lookup(p[1]) == False:
    	senderror(7, linenumber, p[1])
    id_mod = p[1]

def p_insertEra(p):
    '''insertEra : '''
    global list_params
    quads_gen.addQ('era',id_mod,-1,-1)
    list_params = dir_modulos.getParamsNum(id_mod)
    #print "INSERERA--",  list_params, len(list_params)
    if len(list_params) != 0:
    	xparam = 0
    else:
    	xparam = -1

def p_callingA(p):
    '''callingA : callingB ')' ';'
                | ')' ';' '''
    if (p[1] == ')' or p[2] == ')') and (xparam + 1) != len(list_params):
    	senderror(9, linenumber, id_mod, len(list_params))

def p_callingB(p):
    '''callingB : expression checkParam callingC'''

def p_checkParam(p):
    '''checkParam : '''
    argum = pilaOpera.pop()
    tipo = pilaTipos.pop()
    #print "CHECK PARAM--1-", xparam, list_params, argum, tipo
    if xparam >= len(dir_modulos.getParamsNum(id_mod)):
    	senderror(9, linenumber, id_mod, len(dir_modulos.getParamsNum(id_mod)))
    if list_params[xparam] == tipo:
    	prm = "param" + str(xparam + 1)
    	quads_gen.addQ('param',argum,-1,prm)
    else:
    	senderror(8, linenumber, invartipo_mod(list_params[xparam]))

def p_callingC(p):
    '''callingC : ',' sumXparam callingB
            | empty '''

def p_sumXparam(p):
	'''sumXparam : '''
	global xparam
	xparam = xparam + 1

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
    #print pilaOpera, pilaTipos, assign_vars
    valor1 = pilaOpera.pop()
    tipo1 = pilaTipos.pop()
    #print "ASSIGN--", assign_vars
    index = vartipo_assign(assign_vars)
    #print "ASSIGN--", assign_vars, index
    #print "ASSIGN--", valor1, tipo1, index
    if tipo1 != index:
    	senderror(3, linenumber, p[1][0])
    if tipo1 == 0 and p[1][1] == None:
        cont_vars[0] = cont_vars[0] + 1
        work_vars[0] = work_vars[0] + 1
    elif tipo1 == 1 and p[1][1] == None:
        cont_vars[1] = cont_vars[1] + 1
        work_vars[1] = work_vars[1] + 1
    elif tipo1 == 2 and p[1][1] == None:
        cont_vars[2] = cont_vars[2] + 1
        work_vars[2] = work_vars[2] + 1
    #print "NUEVO ID", p[1]
    pairs_idtype.append([p[1][0], tipo1, 0])
    #print "ASSIGN--1 PAIRS", pairs_idtype, vartipo_mod[sum(work_vars) - sum(cont_vars)], sum(work_vars) - sum(cont_vars)
    #print "ASSIGN--2 PAIRS", cont_vars, work_vars
    #tab_valores = tabvar(tab_valores, p[1], tipo1)
    #print "TABVAL en assign", tab_valores
    if p[1][1] == None:
    	quads_gen.add('=', valor1, -1, p[1][0])
    else:
    	quads_gen.add('=', valor1, -1, p[1][1])


def p_condition(p):
    '''condition : IF '(' expression ')' gotoFalse block conditionA continueGo'''

def p_conditionA(p):
    '''conditionA : ELSE gotoE block
                | empty '''

def p_write(p):
	'''write : ECHO writeA ';' '''
	global tab_constant
	if p[2] != None:
		#print "write", p[2]
		tab_constant = tabconstante(tab_constant, p[2])
		quads_gen.addQ(p[1], p[2], -1, -1)
	else:
		pilaTipos.pop()
		quads_gen.addQ(p[1], pilaOpera.pop(), -1, -1)

def p_writeA(p):
    '''writeA : expression
            | CTE_STRING '''
    p[0] = p[1]

def p_array(p):
	'''array : ARR typeDim ID '[' CTE_INTEGER ']' ';' '''
	global pairs_idtype, tab_constant, tab_dims
	if tab_dims.isDuplicate(p[3]) != -1:
		senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3]))
	if p[5] < 1:
		senderror(12, linenumber-1)
	r = p[5] #Equivalente a R = (Ls - Li) * R, R = 1
	tipo1 = vartipo_mod(p[2])
	if tipo1 == 0:
		cont_vars[0] = cont_vars[0] + r
		work_vars[0] = work_vars[0] + r
	elif tipo1 == 1:
		cont_vars[1] = cont_vars[1] + r
		work_vars[1] = work_vars[1] + r
	elif tipo1 == 2:
		cont_vars[2] = cont_vars[2] + r
		work_vars[2] = work_vars[2] + r
	print "NUEVO ARR", p[1], p[5]
	tab_constant = tabconstante(tab_constant, p[5])
	tab_constant = tabconstante(tab_constant, p[5]-1)
	pairs_idtype.append([p[3], tipo1, r])
	tab_dims.add(p[3], 1, p[5]-1, -1)
	quads_gen.addQ('arr', p[3], -1, r)

def p_matrix(p):
	'''matrix : MAT typeDim ID '[' CTE_INTEGER ']' '[' CTE_INTEGER ']' ';' '''
	global pairs_idtype, tab_constant, tab_dims
	if tab_dims.isDuplicate(p[3]) != -1:
		senderror(15, linenumber, p[3], tab_dims.isDuplicate(p[3]))
	if p[5] < 1 or p[8] < 1:
		senderror(12, linenumber-1)
	r = p[5] * p[8] #Equivalente a 2 veces R = (Ls - Li) * R, R = 1
	tipo1 = vartipo_mod(p[2])
	if tipo1 == 0:
		cont_vars[0] = cont_vars[0] + r
		work_vars[0] = work_vars[0] + r
	elif tipo1 == 1:
		cont_vars[1] = cont_vars[1] + r
		work_vars[1] = work_vars[1] + r
	elif tipo1 == 2:
		cont_vars[2] = cont_vars[2] + r
		work_vars[2] = work_vars[2] + r
	print "NUEVO MAT", p[1], p[5], p[8]
	tab_constant = tabconstante(tab_constant, p[5])
	tab_constant = tabconstante(tab_constant, p[5]-1)
	tab_constant = tabconstante(tab_constant, p[8])
	tab_constant = tabconstante(tab_constant, p[8]-1)
	pairs_idtype.append([p[3], tipo1, r])
	tab_dims.add(p[3], 2, p[5]-1, p[8]-1)
	quads_gen.addQ('mat', p[3], -1, r)

def p_pipeline(p):
    '''pipeline : PIPE ID pipelineA'''

def p_pipelineA(p):
    '''pipelineA : '[' pipelineB ']' ';'
            | IN '(' var_cte ')' ';'
            | OUT '(' ')' ';'
            | COUNT ';' '''

def p_pipelineB(p):
    '''pipelineB : exp pipelineC'''

def p_pipelineC(p):
    '''pipelineC : ',' pipelineB
            | empty'''

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
    		quads_gen.addQ('sample1', p[2][3], p[2][4], -1)
    		quads_gen.addQ('sample2', p[2][0], p[2][1], p[2][2])
    	elif p[2][0] == 'off':
			quads_gen.addQ('sample', p[2][0], p[2][1], p[2][2])
    else:
    	tipo2 = pilaTipos.pop()
    	tipo1 = pilaTipos.pop()
    	if tipo1 == 2 or tipo2 == 2:
    		senderror(10, linenumber-1)
    	valor2 = pilaOpera.pop()
    	valor1 = pilaOpera.pop()
    	quads_gen.addQ(p[1], valor1, valor2, p[4])
    
def p_commandA(p):
    '''commandA : ON move exp CTE_INTEGER color ';'
            | OFF move exp ';' '''
    global tab_constant
    if pilaTipos.pop() == 2:
    	senderror(10, linenumber-1)
    if p[1] == 'on':
    	tab_constant = tabconstante(tab_constant, p[4])
        p[0] = [p[1], p[2], pilaOpera.pop(), p[4], p[5]]
    else:
		p[0] = [p[1], p[2], pilaOpera.pop()]

def p_cycle(p):
    '''cycle : WHILE gotoW '(' expression ')' gotoFalse block continueGoW'''

def p_repeat(p):
    '''repeat : REPLAY CTE_INTEGER gotoR '[' repeatA ']' ';' '''
    global tab_temporal, tab_ltemporal
    if flagTabTemp == True:
    	tab_ltemporal=quads_gen.addcontinueR(p[2], tab_ltemporal, linenumber)
    else:
    	tab_temporal=quads_gen.addcontinueR(p[2], tab_temporal, linenumber)
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
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        #print valor1, p[2], valor2, "//", tipo1, p[2], tipo2
        if p[2] == '=' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 8)
            p[2] = p[2] + p[3]
        elif p[2] == '<' and p[3] == '>':
            tipoNuevo = semant_oper(tipo1, tipo2, 9)
            p[2] = p[2] + p[3]
        elif p[2] == '<' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 6)
            p[2] = p[2] + p[3]
        elif p[2] == '>' and p[3] == '=':
            tipoNuevo = semant_oper(tipo1, tipo2, 7)
            p[2] = p[2] + p[3]
        elif p[2] == '<':
        	tipoNuevo = semant_oper(tipo1, tipo2, 4)
    	elif p[2] == '>':
        	tipoNuevo = semant_oper(tipo1, tipo2, 5)
        #print tipoNuevo
        if tipoNuevo != -1:
            if tipoNuevo == 2:
            	cont_tvars[2] = cont_tvars[2] + 1
            	work_tvars[2] = work_tvars[2] + 1
            if flagTabTemp == True:
            	tab_ltemporal=tabvar(tab_ltemporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber)
            else:
            	tab_temporal=tabvar(tab_temporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber)
            quads_gen.add(p[2], valor1, valor2, -1)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)
            #print pilaOpera, pilaTipos
        else:
            senderror(2, linenumber)

def p_exp(p):
    '''exp : exp '+' exp
            | exp '-' exp
            | exp '*' exp
            | exp '/' exp
            | factor empty'''
    global pilaOpera, pilaTipos, quads_gen, tab_ltemporal, tab_temporal
    if p[2] == '+' or p[2] == '-' or p[2] == '*' or p[2] == '/':
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        #print valor1, p[2], valor2, "//", tipo1, p[2], tipo2
        if p[2] == '+':
            tipoNuevo = semant_oper(tipo1, tipo2, 0)
        elif p[2] == '-':
            tipoNuevo = semant_oper(tipo1, tipo2, 1)
        elif p[2] == '*':
            tipoNuevo = semant_oper(tipo1, tipo2, 2)
        elif p[2] == '/':
            tipoNuevo = semant_oper(tipo1, tipo2, 3)
        #print tipoNuevo
        if tipoNuevo != -1:
            if tipoNuevo == 0:
            	cont_tvars[0] = cont_tvars[0] + 1
            	work_tvars[0] = work_tvars[0] + 1
            elif tipoNuevo == 1:
            	cont_tvars[1] = cont_tvars[1] + 1
            	work_tvars[1] = work_tvars[1] + 1
            if flagTabTemp == True:
            	tab_ltemporal=tabvar(tab_ltemporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber)
            else:
            	tab_temporal=tabvar(tab_temporal, quads_gen.gettemp(), tipoNuevo, 0, linenumber)
            quads_gen.add(p[2], valor1, valor2, -1)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)
        else:
            senderror(2, linenumber)

def p_factor(p):
    '''factor : '(' expression ')'
            | var_cte '''
    global listoper, pilaOpera
    if p[1] != '(':
        pilaOpera.append(p[1])
        print "FACTOR--", pilaOpera
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

def p_screen(p):
    '''screen : WHERE
            | CLEAR'''

def p_var_cte(p):
    '''var_cte : id
                | CTE_INTEGER
                | CTE_FLOAT
                | TRUE
                | FALSE'''
    global assign_vars, pilaTipos, tab_constant
    if (type(p[1]) is int):
        #print "VAR_CTE--",p[1]
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(0) #Encuentra un entero para asignar
        pilaTipos.append(0)
        p[0] = p[1]
        #print "--INT", p[1], pilaOpera
    elif (type(p[1]) is float):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(1) #Encuentra un float para asignar
        pilaTipos.append(1)
        p[0] = p[1]
        #print "--FLOAT", p[1], pilaOpera
    elif (p[1] == 'true'):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(2) #Encuentra un boleano para asignar
        pilaTipos.append(2)
        p[0] = p[1]
        #print "--TRUE", p[1], pilaOpera
    elif (p[1] == 'false'):
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(2) #Encuentra un boleano para asignar
        pilaTipos.append(2)
        p[0] = p[1]
        #print "--FALSE", p[1], pilaOpera
    else:
        print "VAR_CTE--", p[1][0], p[1][1]
        findtipo = buscaID(pairs_idtype, p[1][0])
        esdimensionada = tab_dims.isDuplicate(p[1][0])
        #print "VAR_CTE find tipo--", pairs_idtype, p[1], findtipo
        if findtipo == -1:
        	senderror(4, linenumber, p[1][0])
        assign_vars.append(findtipo)
        pilaTipos.append(findtipo)
        if esdimensionada == -1:
        	p[0] = p[1][0]
        else:
        	p[0] = p[1][1]
        #print "--ID", p[1], pilaOpera

def p_gotoFalse(p):
	'''gotoFalse : '''
	global pilaOpera, pilaTipos, assign_vars
	#print "GOTOFALSE--", pilaOpera
	#print "GOTOFALSE--", pilaTipos
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
tab_constant = TabConst() #Instancia clase TabConst, tabla de constantes del codigo seleccionado
tab_valores = TabVars(2000, 4000, 6000) #Instancia clase TabVars, tabla de variables del codigo seleccionado
tab_lvalores = TabVars(12000, 14000, 16000) #Instancia clase TabVars, tabla de variables locales, distinta por cada modulo
tab_temporal = TabVars(22000, 24000, 26000) #Instancia clase TabVars, tabla de variables temporales del codigo seleccionado
tab_ltemporal = TabVars(32000, 34000, 36000) #Instancia clase TabVars, tabla de variables temporales locales del codigo seleccionado
tab_pointer = TabPointer(40000) #Instancia clase TabPointer, guarda los apuntadores a direccion dentro de variables dimensionadas
tab_lpointer = TabPointer(42000) #Instancia clase TabPointer, guarda los apuntadores locales a direccion dentro de variables dimensionadas
dir_modulos = DirMods() #Instancia clase DirMods, directorio de modulos del programa
tab_dims = TabDims() #Instancia clase TabDims, almaneca limites de variables dimensionadas
quads_gen = CodeGen() #Instancia clase CodeGen, generador de cuadruplos para codigo intermedio
cont_vars = [0,0,0] #Contador de variables en modulos, en el orden entero/flotante/boleano
work_vars = [0,0,0] #Contador de variables en el workspace, en el orden entero/flotante/boleano
cont_tvars = [0,0,0] #Contador de variables en modulos, en el orden entero/flotante/boleano
work_tvars = [0,0,0] #Contador de variables en el workspace, en el orden entero/flotante/boleano
cont_point = 0 #Contador de apuntadores en modulos
work_point = 0 #Contador de apuntadores en el workspace
list_params = [] #Lista que almacena el tipo de variables encontrado en los parametros de modulos.
quad_mod = 0 #Almacena el cuadruplo donde comienza un modulo
line_mod = 0 #Almacena el numero de linea donde comienza un modulo
id_mod = "work" #Guarda el id que sera registrado en el cuadruplo ERA
xparam = 0 #Variable entera en funcion de apuntador de parametros
flagTabTemp = False #Indica si almacena valores temporales globales o locales
es_dim = 0 #Variable indica si la variable es atomica, de dimension 1 o dimension 2

#'''

nodisplay = 0

try:
    if sys.argv[1]:
        Name = str(sys.argv[1])
except:
    Name = "ej/ej10.txt"

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
#print st
f.close()

if nodisplay != 1:
	print("\n")
	print tab_dims
	print tab_pointer
	print("\n")
	dir_modulos.echotables()
	dir_modulos.echotablestemp()
	#tab_valores.echo() #Despliega tabla de valores
	#tab_valores.write() #Guarda en archivo la tabla de valores
	print("\n")
	dir_modulos.echo() #Despliega directorio de modulos
	dir_modulos.echoV()
	dir_modulos.echoT()
	#dir_modulos.write()
	dir_modulos.writeQ()
	#print tab_valores.getDir("b")
	print("\n")
	tab_constant.echo()
	#tab_constant.write()
	tab_constant.writeQ()
	print("\n")
	quads_gen.echo()
	quads_gen.write()
	print("\n")
	#quads_gen.echoQ(dir_modulos, tab_constant)
	quads_gen.writeQ(dir_modulos, tab_constant)