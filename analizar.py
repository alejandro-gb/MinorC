#----------------------------------------ANALIZADOR LEXICO

#DICCIONARIO CON LAS PALABRAS RESERVADAS
reservadas = {
    'break':'BREAK',
    'case':'CASE',
    'char':'CHAR',
    'signed':'SIGNED',
    'const':'CONST',
    'continue':'CONTINUE',
    'default':'DEFAULT',
    'do':'DO',
    'double':'DOUBLE',
    'else':'ELSE',
    'static':'STATIC',
    'float':'FLOAT',
    'for':'FOR',
    'typedef':'TYPEDEF',
    'auto':'AUTO',
    'goto':'GOTO',
    'if':'IF',
    'int':'INT',
    'enum':'ENUM',
    'return':'RETURN',
    'struct':'STRUCT',
    'sizeof':'SIZEOF',
    'extern':'EXTERN',
    'switch':'SWITCH',
    'void':'VOID',
    'while':'WHILE',
}

#LISTA DE TOKENS
tokens = [
    'CADENA',
    'ASSIGN_SHIFTR',
    'ASSIGN_SHIFTL',
    'ASSING_MAS',
    'ASSING_MENOS',
    'ASSING_POR',
    'ASSING_DIV',
    'ASSING_MOD',
    'ASSING_AND',
    'ASSING_OR',
    'ASSING_XOR',
    'SHIFTR',
    'SHIFTL',
    'INCREMENTO',
    'DECREMENTO',
    'PUNTERO',
    'AND',
    'OR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'EQUIVALENTE',
    'DIFERENTE',
    'PUNTOYCOMA',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'DOSPUNTOS',
    'IGUAL',
    'PARA',
    'PARC',
    'CORCHETEA',
    'CORCHETEC',
    'PUNTO',
    'ANPERSAND',
    'ADMIRACION',
    'NOTBIT',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'MOD',
    'MAYOR',
    'MENOR',
    'PICO',
    'BARRAOR',
    'INTERROGACION',
    'ENTERO',
    'DECIMAL',
    'IDENTIFICADOR',
    'COMENTARIO',
    'COMENTARIOMULTI',

] + list(reservadas.values())

#DEFINICION DE TOKENS
t_ASSIGN_SHIFTR     = r'>>='
t_ASSIGN_SHIFTL     = r'<<='
t_ASSING_MAS        = r'\+='
t_ASSING_MENOS      = r'-='
t_ASSING_POR        = r'\*='
t_ASSING_DIV        = r'/='
t_ASSING_MOD        = r'%='
t_ASSING_AND        = r'&='
t_ASSING_OR         = r'\|='
t_ASSING_XOR        = r'^='
t_SHIFTR            = r'>>'
t_SHIFTL            = r'<<'
t_INCREMENTO        = r'\+\+'
t_DECREMENTO        = r'--'
t_PUNTERO           = r'->'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_MENORIGUAL        = r'<='
t_MAYORIGUAL        = r'>='
t_EQUIVALENTE       = r'=='
t_DIFERENTE         = r'!='
t_PUNTOYCOMA        = r';'
t_LLAVEA            = r'\{'
t_LLAVEC            = r'\}'
t_COMA              = r','
t_DOSPUNTOS         = r':'
t_IGUAL             = r'='
t_PARA              = r'\('
t_PARC              = r'\)'
t_CORCHETEA         = r'\['
t_CORCHETEC         = r'\]'
t_PUNTO             = r'.'
t_ANPERSAND         = r'&'
t_ADMIRACION        = r'!'
t_NOTBIT            = r'~'
t_MAS               = r'\+'
t_MENOS             = r'-'
t_POR               = r'\*'
t_DIV               = r'/'
t_MOD               = r'%'
t_MAYOR             = r'>'
t_MENOR             = r'<'
t_PICO              = r'\^'
t_BARRAOR           = r'\|'   
t_INTERROGACION     = r'\?'

#METODO PARA ACEPTAR UN DECIMAL Y DEVOLVER EL VALOR
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = 0
    return t

#METODO PARA ACEPTAR UN ENTERO Y DEVOLVER SU VALOR
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = 0
    return t

#METODO PARA ACEPTAR UN IDENTIFICADOR
def t_IDENTIFICADOR(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'IDENTIFICADOR')
     return t

#METODO PARA ACEPTAR UNA CADENA QUITANDO LAS COMILLAS DOBLES
def t_CADENA(t):
    r"\".*?\""
    t.value = t.value[1:-1]
    return t 

#CARACTERES IGNORADOS
t_ignore = " \t\v\f"

#METODO PARA ACEPTAR UN COMENTARIO
def t_COMENTARIO(t):
    r'//.*\n'
    t.lexer.lineno += 1

#METODO PARA ACEPTAR UN COMENTARIO MULTILINEA
def t_COMENTARIOMULTI(t):
    r'/\*(.|\n*)?\*/'
    t.lexer.lineno += t.value.count('\n')

#METODO PARA ACEPTAR UNA NUEVA LINEA Y SUMAR LA CUENTA
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#METODO PARA RECONOCER UN ERROR
def t_error(t):
    print('Error lexico '+ t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

#PRECEDENCIA
precedence = (
    ('left','ADMIRACION','AND','OR'),
    ('left','EQUIVALENTE','DIFERENTE'),
    ('left','MAYOR','MAYORIGUAL','MENOR','MENORIGUAL'),
    ('left','BARRAOR'), 
    ('left','PICO'),
    ('left','ANPERSAND'),
    ('left','SHIFTL','SHIFTR'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV','MOD')
)

#---------------------------------ANALIZADOR SINTACTICO
def p_start(t):
    '''start : inicio'''

def p_inicio(t):
    '''inicio : IDENTIFICADOR
              | CADENA
              | PARA expresion PARC 
              '''

def p_expresion(t):
    '''expresion : asignacion
                 | expresion COMA asignacion'''

def p_asignacion(t):
    '''asignacion : condicional
                  | unario assoperador asignacion'''

def p_assoperador(t):
    '''assoperador : IGUAL
                   | ASSIGN_MUL
                   | ASSIGN_DIV
                   | ASSIGN_MOD
                   | ASSIGN_MAS
                   | ASSIGN_MENOS
                   | ASSIGN_SHIFTL
                   | ASSIGN_SHIFTR
                   | ASSIGN_AND
                   | ASSIGN_OR
                   | ASSIGN_XOR'''

def p_condicional(t):
    '''condicional : logicaoexpresion
                   | logicaoexpresion INTERROGACION expresion DOSPUNTOS condicional'''

def p_logicaoexpresion(t):
    '''logicaoexpresion : logicayexpresion
                        | logicaoexpresion OR logicayexpresion'''

def p_logicayexpresion(t):
    '''logicayexpresion : inclusivaoexpresion
                        | logicayexpresion AND inclusivaoexpresion'''

def p_inclusivaoexpresion(t):
    '''inclusivaoexpresion : exclusivaoexpresion
                           | inclusivaoexpresion BARRAOR exclusivaoexpresion'''

def p_exclusivaoexpresion(t):
    '''exclusivaoexpresion : yexpresion
                           | exclusivaoexpresion PICO yexpresion'''

def p_yexpresion(t):
    '''yexpresion : equiexpresion
                  | yexpresion ANPERSAND equiexpresion'''

def p_equiexpresion(t):
    '''equiexpresion : relacional
                     | equiexpresion EQUIVALENTE relacional
                     | equiexpresion DIFERENTE relacional'''

def p_relacional(t):
    '''relacional : shiftexpresion
                  | relacional MAYOR shiftexpresion
                  | relacional MENOR shiftexpresion
                  | relacional MENORIGUAL shiftexpresion
                  | relacional MAYORIGUAL shiftexpresion'''
        
def p_shiftexpresion(t):
    '''shiftexpresion : adicion
                      | shiftexpresion SHIFTL adicion
                      | shiftexpresion SHIFTR adicion'''
        
def p_adicion(t):
    '''adicion : multiplicacion
               | adicion MAS multiplicacion
               | adicion MENOS multiplicacion'''

def p_multiplicacion(t):
    '''multiplicacion : casteo
                      | multiplicacion POR casteo
                      | multiplicacion DIV casteo
                      | multiplicacion MOD casteo'''

def p_casteo(t):
    '''casteo : unario
              | PARA nombretipo PARC casteo'''

def p_unario(t):
    '''unario : postfijo
              | INCREMENTO unario
              | DECREMENTO unario
              | operador casteo
              | SIZEOF unario
              | SIZEOF PARA nombretipo PARC'''

def p_operador(t):
    '''operador : ANPERSAND
                | POR
                | MAS
                | MENOS
                | ADMIRACION
                | NOTBIT'''

def p_postfijo(t):
    '''postfijo : inicio
                | postfijo CORCHETEA expresion CORCHETEC
                | postfijo PARA PARC
                | postfijo PARA listaargumentosexp PARC
                | postfijo PUNTO IDENTIFICADOR
                | postfijo PUNTERO IDENTIFICADOR
                | postfijo INCREMENTO
                | postfijo DECREMENTO
                | PARA nombretipo PARC LLAVEA listainicial LLAVEC
                | PARA nombretipo PARC LLAVEA listainicial COMA LLAVEC'''

def P_listaargumentosexp(t):
    '''listaargumentosexp : asignacion
                          | listaargumentosexp COMA asignacion'''

def p_listainicial(t):
    '''listainicial : '''

#------------------------------------------IMPORTS
import ply.yacc as yacc
parser = yacc.yacc()

#METODO DEL PARSER
def parse(input):
    return parser.parse(input)