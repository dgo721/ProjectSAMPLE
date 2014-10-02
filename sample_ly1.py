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

literals = [',',';','*','/', '(',')','[',']','{','}','+','-','=','<','>','_']

#TOKENS

def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserva.get(t.value,'ID')    # Check for reserved words
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
import ply.lex as lex
lex.lex()

# Parser

def p_program(p):
    '''program : INIT programA END
    			| INIT END'''

def p_programA(p):
    '''programA : workspace programA
            | workspace'''

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
    '''module : MOD '_' ID '(' vars ')' block
            | MOD '_' ID block'''

def p_vars(p):
    '''vars : type ID ',' vars
    		| type ID'''

def p_type(p):
    '''type : INT
            | FLOAT'''

def p_calling(p):
	'''calling : '_' ID '(' callingA ')' ';'
            | '_' ID '(' ')' ';' '''

def p_callingA(p):
	'''callingA : expression ',' callingA
            | expression '''

def p_block(p):
    '''block : '{' blockA '}'
                | '{' '}' '''

def p_blockA(p):
    '''blockA : statute blockA
                | statute'''

def p_assign(p):
    '''assign : ID '=' expression ';' '''

def p_condition(p):
    '''condition : IF '(' expression ')' block ELSE block
                | IF '(' expression ')' block empty '''

def p_write(p):
    '''write : ECHO expression ';'
            | '"' CTE_STRING '"' ';' '''

def p_pipeline(p):
    '''pipeline : PIPE ID '[' pipelineA ']' ';'
            | PIPE ID IN '(' var_cte ')' ';'
            | PIPE ID OUT '(' ')' ';'
            | PIPE ID COUNT ';' '''

def p_pipelineA(p):
    '''pipelineA : exp ',' pipelineA
            | exp'''

def p_command(p):
    '''command : figure exp exp color ';'
            | SAMPLE ON move exp CTE_INTEGER color ';'
            | SAMPLE OFF move exp ';' '''

def p_repeat(p):
	'''repeat : REPLAY CTE_INTEGER '[' repeatA ']' ';' '''

def p_repeatA(p):
    '''repeatA : command repeatA
            | command'''

def p_expression(p):
    '''expression : exp '=' '=' exp
                | exp '<' '>' exp
                | exp '<' '=' exp
                | exp '>' '=' exp
                | exp '>' exp
                | exp '<' exp
                | exp'''

def p_exp(p):
    '''exp : term expA
            | term'''

def p_expA(p):
    '''expA : '+' exp
            | '-' exp'''

def p_term(p):
    '''term : factor termA
    		| factor'''

def p_termA(p):
    '''termA : '*' term
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

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

s = sys.argv[1];

f = open(s, "r")
lines = f.readlines()
x=0
st=""
for l in lines:
    st=st+lines[x]
    x=x+1
yacc.parse(unicode(st))
print st
f.close()