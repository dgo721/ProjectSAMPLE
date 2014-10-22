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
    'replay' : 'REPLAY',
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
    'purple' : 'PURPLE',
    'cyan' : 'CYAN',
}

tokens = ['CTE_INTEGER','CTE_FLOAT', 'CTE_STRING','ID'] + list(reserva.values())

literals = [',',';','*','/', '(',')','[',']','{','}','+','-','=','<','>','#']

#TOKENS

def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    global pilaOpera
    t.type = reserva.get(t.value,'ID') # Checa palabras reservadas
    return t

t_CTE_STRING = r'\".*?\"'

def t_CTE_FLOAT(t):
    r'-?\d+\.\d*'
    global pilaOpera
    t.value = float(t.value)
    return t

def t_CTE_INTEGER(t):
    r'\d+'
    global pilaOpera
    t.value = int(t.value)
    return t

t_ignore = " \t"

#def t_newline(t):
#    r'\r\n+'

def t_newline(t):
    r'\n+'

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
    
    templist = list()
    #print "SUMA", sum(cont_vars), pairs_idtype
    suma = sum(work_vars)
    while (suma > 0):
    	tempair = pairs_idtype.pop()
    	#print "ULTIMO PAR", tempair
    	dup = isduplicate(templist, tempair, len(templist))
    	#print "DUP", dup
    	if dup != 1:
    		#tab_valores.removelastKeyDir(tempair)
    		templist.append(tempair)
    	suma = suma - 1
    
    #print "TEMPLIST", templist, tab_valores
    suma = len(templist)
    while suma > 0:
    	par = templist.pop()
    	tab_valores=tabvar(tab_valores, par[0], par[1])
    	suma = suma - 1

    dir_modulos = dirmod(dir_modulos, "workspace", [], work_vars[0], work_vars[1], work_vars[2], tab_valores)

def p_programA(p):
    '''programA : programB END
                | END'''
    p[0] = p[1]

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
    global cont_vars, pairs_idtype
    cont_vars = [0,0,0]

def p_statute(p):
    '''statute : assign
                | condition
                | write
                | repeat
                | command
                | calling
                | pipeline
                | screen'''
    global assign_vars
    assign_vars=[]
    print "STATUTE", quads_gen.getX()

def p_module(p):
    '''module : MOD '#' ID moduleA'''
    global id_params, cont_vars, dir_modulos, list_params, work_vars, tab_valores, tab_lvalores, pairs_idtype
    print "modulo #", p[3]

    templist = list()
    #print "SUMA", sum(cont_vars), pairs_idtype
    suma = sum(cont_vars)
    while (suma > 0):
    	tempair = pairs_idtype.pop()
    	#print "ULTIMO PAR", tempair
    	dup = isduplicate(templist, tempair, len(templist))
    	#print "DUP", dup
    	if dup != 1:
    		#tab_valores.removelastKeyDir(tempair)
    		templist.append(tempair)
    	suma = suma - 1
    
    #print "TEMPLIST", templist, tab_valores
    suma = len(templist)
    while suma > 0:
    	par = templist.pop()
    	tab_lvalores=tabvar(tab_lvalores, par[0], par[1])
    	suma = suma - 1

    dir_modulos = dirmod(dir_modulos, p[3], list_params, cont_vars[0], cont_vars[1], cont_vars[2], copy.deepcopy(tab_lvalores))
    list_params=[] #Reinicia lista de parametros
    id_params=[] #Reinicia lista de parametros
    work_vars[0] = work_vars[0] - cont_vars[0]
    work_vars[1] = work_vars[1] - cont_vars[1]
    work_vars[2] = work_vars[2] - cont_vars[2]
    cont_vars = [0,0,0] #Reinicia contador
    tab_lvalores.empty()

def p_moduleA(p):
    '''moduleA : '(' vars ')' block
            | block'''

def p_vars(p):
    '''vars : type ID varsA'''
    global id_type, tab_lvalores, id_params
    #print p[2]
    id_params.append(p[2])
    #print id_type
    #print id_params
    tab_lvalores = tabvar(tab_lvalores, p[2], vartipo_mod(id_type.pop())) #Aniade a la tabla de valores el par ID, TIPO

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

def p_calling(p):
    '''calling : '#' ID '(' callingA'''
    #print dir_modulos.getParams(p[2])
    #print "CALLING", assign_vars

def p_callingA(p):
    '''callingA : callingB ')' ';'
            | ')' ';' '''

def p_callingB(p):
    '''callingB : expression callingC'''
    #print "CALLING B", assign_vars

def p_callingC(p):
    '''callingC : ',' callingB
            | empty '''

def p_block(p):
    '''block : '{' blockA '''
    print "block", p[1]

def p_blockA(p):
    '''blockA : blockB '}'
                | '}' '''
    print "blockA", p[1]

def p_blockB(p):
    '''blockB : statute blockC'''

def p_blockC(p):
    '''blockC : blockB
                | empty'''

def p_assign(p):
    '''assign : ID '=' expression ';' '''
    global tab_valores, pilaOpera, pilaTipos, quads_gen, cont_vars, work_vars, pairs_idtype
    #print pilaOpera, pilaTipos, assign_vars
    valor1 = pilaOpera.pop()
    tipo1 = pilaTipos.pop()
    if tipo1 != vartipo_assign(assign_vars):
    	senderror(3, p[1])
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
    pairs_idtype.append([p[1], tipo1])
    #print "PAIRS en assign", pairs_idtype
    #tab_valores = tabvar(tab_valores, p[1], tipo1)
    #print "TABVAL en assign", tab_valores
    quads_gen.add('=', valor1, -1, p[1])

def p_condition(p):
    '''condition : IF '(' expression ')' gotoFalse block conditionA'''
    print "condition", p[1], p[3]

def p_conditionA(p):
    '''conditionA : ELSE block
                | empty '''
    print "conditionA", p[1]

def p_write(p):
	'''write : ECHO writeA ';' '''
	global tab_constant
	if p[2] != None:
		print "write", p[2]
		tab_constant = tabconstante(tab_constant, p[2])
		quads_gen.addQ(p[1], p[2], -1, -1)
	else:
		quads_gen.addQ(p[1], pilaOpera.pop(), -1, -1)

def p_writeA(p):
    '''writeA : expression
            | CTE_STRING '''
    p[0] = p[1]

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
    		print "ERROR TIPO OPERACION"
    	valor2 = pilaOpera.pop()
    	valor1 = pilaOpera.pop()
    	quads_gen.addQ(p[1], valor1, valor2, p[4])
    
def p_commandA(p):
    '''commandA : ON move exp CTE_INTEGER color ';'
            | OFF move exp ';' '''
    if pilaTipos.pop() == 2:
    	print "ERROR TIPO OPERACION"
    if p[1] == 'on':
    	p[0] = [p[1], p[2], pilaOpera.pop(), p[4], p[5]]
    else:
		p[0] = [p[1], p[2], pilaOpera.pop()]

def p_repeat(p):
    '''repeat : REPLAY CTE_INTEGER '[' repeatA ']' ';' '''

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
    global pilaOpera, pilaTipos, quads_gen
    if p[2] == '=' or p[2] == '<' or p[2] == '>' or p[2] == 'and' or p[2] == 'or':
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        print valor1, p[2], valor2, "//", tipo1, p[2], tipo2
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
            quads_gen.add(p[2], valor1, valor2, -1)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)
            #print pilaOpera, pilaTipos
        else:
            senderror(2)

def p_exp(p):
    '''exp : exp '+' exp
            | exp '-' exp
            | exp '*' exp
            | exp '/' exp
            | factor empty'''
    global pilaOpera, pilaTipos, quads_gen
    if p[2] == '+' or p[2] == '-' or p[2] == '*' or p[2] == '/':
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        print valor1, p[2], valor2, "//", tipo1, p[2], tipo2
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
            quads_gen.add(p[2], valor1, valor2, -1)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)
        else:
            senderror(2)

def p_factor(p):
    '''factor : '(' expression ')'
            | var_cte '''
    global listoper, pilaOpera
    if p[1] != '(':
        pilaOpera.append(p[1])
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
            | ORANGE
            | PURPLE
            | CYAN'''
    p[0] = p[1]

def p_screen(p):
    '''screen : WHERE
            | CLEAR'''

def p_var_cte(p):
    '''var_cte : ID
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
        findtipo = buscaID(pairs_idtype, p[1])
        print pairs_idtype, p[1], findtipo
        assign_vars.append(findtipo)
        pilaTipos.append(findtipo)
        p[0] = p[1]
        #print "--ID", p[1], pilaOpera

def p_gotoFalse(p):
	'''gotoFalse : '''
	global quads_gen, pilaOpera, pilaTipos
	if pilaTipos.pop() != 2:
		senderror(5)
	quads_gen.addQ('gotoF', pilaOpera.pop(), -1, -1)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        senderror(1, p.value)
    else:
        senderror(1, "EOF")


from ply import yacc
yacc.yacc()
from tabvars import *
from tabconst import *
from dirmods import *
from cube_sem import semant_oper
from codegen import CodeGen

pilaTipos = list() #Almacena los tipos encontrados.
pilaOpera = list() #Guarda las variables y contanstes utilizadas para una asignacion
id_type = list() #Para VARS, guarda los tipos de variable encontrados en parametros
id_params = list() #Para MODULE-VARS, guarda los id recibidos como parametros en los modulos
assign_vars = list() #Para ASSIGN, almacena los tipos de variables encontrados en una asignacion
pairs_idtype = list()
tab_constant = TabConst() #Instancia clase TabConst, tabla de constantes del codigo seleccionado
tab_valores = TabVars(2000, 4000, 6000) #Instancia clase TabVars, tabla de variables del codigo seleccionado
tab_lvalores = TabVars(1100, 1200, 1300)
dir_modulos = DirMods() #Instancia clase DirMods, directorio de modulos del programa
quads_gen = CodeGen() #Instancia clase CodeGen, generador de cuadruplos para codigo intermedio
cont_vars = [0,0,0]
work_vars = [0,0,0]
list_params = []

#'''

try:
    if sys.argv[1]:
        Name = str(sys.argv[1])
except:
    Name = "ej/ej8.txt"

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

#dir_modulos.echotables()
#tab_valores.echo() #Despliega tabla de valores
#tab_valores.write() #Guarda en archivo la tabla de valores
print("\n")
#dir_modulos.echo() #Despliega directorio de modulos
#dir_modulos.write()
#print tab_valores.getDir("b")
print("\n")
tab_constant.echo()
#tab_constant.write()
print("\n")
quads_gen.echo()
#quads_gen.write()
print("\n")
#quads_gen.echoQ(tab_valores, tab_constant)
#quads_gen.writeQ(tab_valores, tab_constant)