# LEX

import sys
sys.path.insert(0,"../..")

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

def p_program(p):
    '''program : INIT programA'''

def p_programA(p):
    '''programA : programB END
                | END'''

def p_programB(p):
    '''programB : workspace programC'''

def p_programC(p):
    '''programC : programB
            | empty'''

def p_workspace(p):
    '''workspace : statute
            | module'''
    global cont_vars
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

def p_module(p):
    '''module : MOD '#' ID moduleA'''
    global id_params, cont_vars, dir_modulos, list_params
    print "modulo #", p[3]
    dir_modulos = dirmod(dir_modulos, p[3], list_params, cont_vars[0], cont_vars[1], cont_vars[2], tab_valores)
    list_params=[] #Reinicia lista de parametros
    id_params=[] #Reinicia lista de parametros
    cont_vars = [0,0,0] #Reinicia contador

def p_moduleA(p):
    '''moduleA : '(' vars ')' block
            | block'''
    print "modulo A"

def p_vars(p):
    '''vars : type ID varsA'''
    global id_type, tab_valores, id_params
    #print p[2]
    id_params.append(p[2])
    #print id_type
    #print id_params
    tab_valores = tabvar(tab_valores, p[2], vartipo_mod(id_type.pop())) #Aniade a la tabla de valores el par ID, TIPO

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

def p_callingA(p):
    '''callingA : callingB ')' ';'
            | ')' ';' '''

def p_callingB(p):
    '''callingB : expression callingC'''

def p_callingC(p):
    '''callingC : ',' callingB
            | empty '''

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
    '''assign : ID '=' expression ';' '''
    global tab_valores, pilaOpera, pilaTipos, quads_gen, cont_vars
    valor1 = pilaOpera.pop()
    tipo1 = pilaTipos.pop()
    if tipo1 == 0:
        cont_vars[0] = cont_vars[0] + 1
    elif tipo1 == 1:
        cont_vars[1] = cont_vars[1] + 1
    elif tipo1 == 2:
        cont_vars[2] = cont_vars[2] + 1
    ultimot = quads_gen.lasttemp()
    quads_gen.add3('=', ultimot, p[1])
    tab_valores = tabvar(tab_valores, p[1], vartipo_assign(assign_vars))

def p_condition(p):
    '''condition : IF '(' expression ')' block conditionA'''

def p_conditionA(p):
    '''conditionA : ELSE block
                | empty '''

def p_write(p):
    '''write : ECHO expression ';'
            | '"' CTE_STRING '"' ';' '''

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

def p_commandA(p):
    '''commandA : ON move exp CTE_INTEGER color ';'
            | OFF move exp ';' '''

def p_repeat(p):
    '''repeat : REPLAY CTE_INTEGER '[' repeatA ']' ';' '''

def p_repeatA(p):
    '''repeatA : command repeatB'''

def p_repeatB(p):
    '''repeatB : repeatA
            | empty'''

def p_expression(p):
    '''expression : exp expressionA'''

def p_expressionA(p):
    '''expressionA : '=' '=' exp
                | '<' '>' exp
                | '<' '=' exp
                | '>' '=' exp
                | '>' exp
                | '<' exp
                | AND exp
                | OR exp
                | empty'''

def p_exp(p):
    '''exp : term expA'''

def p_expA(p):
    '''expA : '+' exp
            | '-' exp
            | empty'''
    global pilaOpera, pilaTipos, quads_gen
    if p[1] == '+' or p[1] == '-':
        print p[1]
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        if p[1] == '+':
            tipoNuevo = semant_oper(tipo1, tipo2, 0)
        elif p[1] == '-':
            tipoNuevo = semant_oper(tipo1, tipo2, 1)
        if tipoNuevo != -1:
            quads_gen.add(p[1], valor1, valor2)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)

def p_term(p):
    '''term : factor termA'''

def p_termA(p):
    '''termA : '*' term
            | '/' term
            | empty'''
    global pilaOpera, pilaTipos, quads_gen
    if p[1] == '*' or p[1] == '/':
        print p[1]
        valor2=pilaOpera.pop()
        valor1=pilaOpera.pop()
        tipo2=pilaTipos.pop()
        tipo1=pilaTipos.pop()
        if p[1] == '*':
            tipoNuevo = semant_oper(tipo1, tipo2, 2)
        elif p[1] == '/':
            tipoNuevo = semant_oper(tipo1, tipo2, 3)
        if tipoNuevo != -1:
            quads_gen.add(p[1], valor1, valor2)
            pilaOpera.append(quads_gen.lasttemp())
            pilaTipos.append(tipoNuevo)

def p_factor(p):
    '''factor : '(' expression ')'
            | var_cte '''
    global listoper, pilaOpera
    print p[1]
    if p[1] != '(':
        pilaOpera.append(p[1])

def p_figure(p):
    '''figure : OVAL
            | TRIO
            | QUAD
            | ARC'''

def p_move(p):
    '''move : UP
            | DOWN
            | LEFT
            | RIGHT'''

def p_color(p):
    '''color : RED
            | YELLOW
            | BLUE
            | GREEN
            | BLACK
            | ORANGE
            | PURPLE
            | CYAN'''

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
        findtipo = tipoID(tab_valores, p[1])
        tab_constant = tabconstante(tab_constant, p[1])
        assign_vars.append(findtipo)
        pilaTipos.append(findtipo)
        p[0] = p[1]
        #print "--ID", p[1], pilaOpera



def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


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
tab_constant = TabConst() #Instancia clase TabConst, tabla de constantes del codigo seleccionado
tab_valores = TabVars() #Instancia clase TabVars, tabla de variables del codigo seleccionado
dir_modulos = DirMods() #Instancia clase DirMods, directorio de modulos del programa
quads_gen = CodeGen() #Instancia clase CodeGen, generador de cuadruplos para codigo intermedio
cont_vars = [0,0,0]
list_params = []

#'''

try:
    if sys.argv[1]:
        Name = str(sys.argv[1])
except:
    Name = "ej7.txt"

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
#'''
#print "TABLA FINAL", tab_valores
tab_valores.echo() #Despliega tabla de valores
#tab_valores.write() #Guarda en archivo la tabla de valores
print("\n")
dir_modulos.echo() #Despliega directorio de modulos
#dir_modulos.write()
#print tab_valores.getDir("b")
print("\n")
tab_constant.echo()
#quads_gen.echo()