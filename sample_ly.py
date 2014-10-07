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
    t.type = reserva.get(t.value,'ID') # Checa palabras reservadas
    return t

t_CTE_STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_CTE_FLOAT(t):
    r'-?\d+\.\d*'
    t.value = float(t.value)
    return t

def t_CTE_INTEGER(t):
    r'\d+'
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

def p_statute(p):
    '''statute : assign
                | condition
                | write
                | repeat
                | command
                | calling
                | pipeline
                | screen'''

def p_module(p):
    '''module : MOD '#' ID moduleA'''

def p_moduleA(p):
    '''moduleA : '(' vars ')' block
            | block'''

def p_vars(p):
    '''vars : type ID varsA'''
    global id_type, tab_valores
    #print p[2]
    tab_valores = tabvar(tab_valores, p[2], vartipo_mod(id_type.pop())) #Aniade a la tabla de valores el par ID, TIPO

def p_varsA(p):
    '''varsA : ',' vars
            | empty'''

def p_type(p):
    '''type : INT
            | FLOAT'''
    global id_type
    id_type.append(p[1]) #Aniade a la lista de tipos de parametros, sea INT o FLOAT
    print id_type

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
    global assign_vars, tipo_asigna, tab_valores
    if p[2] == '=':
    	#print "EN LISTA", vartipo_assign(assign_vars)
    	#print tab_valores
    	tab_valores = tabvar(tab_valores, p[1], vartipo_assign(assign_vars))
    	tipo_asigna = 0 #Reinicia parametro tipo
    	assign_vars=[] = #Reinicia lista

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
    '''expression : exp '=' '=' exp
                | exp '<' '>' exp
                | exp '<' '=' exp
                | exp '>' '=' exp
                | exp '>' exp
                | exp '<' exp
                | exp'''

def p_exp(p):
    '''exp : term expA'''

def p_expA(p):
    '''expA : expB
            | empty'''

def p_expB(p):
    '''expB : '+' exp
            | '-' exp'''

def p_term(p):
    '''term : factor termA'''

def p_termA(p):
    '''termA : termB
            | empty'''

def p_termB(p):
    '''termB : '*' term
            | '/' term'''

def p_factor(p):
    '''factor : '(' expression ')'
    		| var_cte'''

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
                | CTE_FLOAT'''
    global assign_vars
    if (type(p[1]) is int):
    	assign_vars.append(0) #Encuentra un entero para asignar
    	#print "INT", p[1]
    elif (type(p[1]) is float):
    	assign_vars.append(1) #Encuentra un float para asignar
    	#print "FLOAT", p[1]
    else:
    	assign_vars.append(tipoID(tab_valores, p[1]))
    	#print "ID", p[1]

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


assign_vars = list()
tipo_asigna=0 #Determina si el tipo de variable en asignacion es INT(0) o FLOAT(1)
id_type = list() #Para VARS, guarda los tipos de variable encontrados en parametros
tab_valores=TabVars() #Instancia clase TabVars, tabla de variables del codigo seleccionado.

#'''

try:
    if sys.argv[1]:
        Name = str(sys.argv[1])
except:
    Name = "ej4.txt"

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
#tab_valores = sort_tabvar(tab_valores)
tab_valores.echo() #Despliega tabla de valores