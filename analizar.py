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
    'printf':'PRINTF',
    'scanf':'SCANF',
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
    r"(\"|').*?(\"|')"
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
    desc = 'El caracter: ' + t.value[0] + ' no es valido'
    nuevo = errores.Error('LEXICO',desc, t.lineno, t.lexpos)
    main.Editor.tablaErrores.newError(nuevo)
    t.lexer.skip(1)

import ply.lex as lex
import main
import errores
lexer = lex.lex()

#PRECEDENCIA
precedence = (
    #OPERADOR COMA
    #ASIGNACIONES
    #TERNARIO
    ('left','ADMIRACION','AND','OR'),
    ('left','BARRAOR'), 
    ('left','PICO'),
    ('left','ANPERSAND'),
    ('left','EQUIVALENTE','DIFERENTE'),
    ('left','MAYOR','MAYORIGUAL','MENOR','MENORIGUAL'),
    ('left','SHIFTL','SHIFTR'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV','MOD')
    #SIZEOF
    #CASTEOS
    #OPERADOR UNARIO
    #FUNCIONES
)

#---------------------------------ANALIZADOR SINTACTICO
from instrucciones import *

def p_start(t):
    'start : instrucciones'
    t[0] = t[1]

def p_instrucciones(t):
    'instrucciones : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_una_instruccion(t):
    'instrucciones : instruccion'
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : funcion
                   | declaracion
                   | printf'''
    t[0] = t[1]

def p_prinf(t):
    'printf : PRINTF PARA listaprint PARC PUNTOYCOMA'
    t[0] = Printf(t[3])

def p_listprint(t):
    'listaprint : listaprint COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_soloprint(t):
    'listaprint : expresion'
    t[0] = [t[1]]

def p_funcion(t):
    '''funcion : tipo IDENTIFICADOR PARA PARC LLAVEA LLAVEC'''
    t[0] = Funcion(t[1],t[2])

def p_declaracion(t):
    'declaracion : tipo lista_asignaciones PUNTOYCOMA'
    t[0] = Asignacion(t[1],t[2])

def p_lista_asignaciones(t):
    'lista_asignaciones : lista_asignaciones COMA asignacion'
    t[1].append(t[3])
    t[0] = t[1]

def p_una_asignacion(t):
    'lista_asignaciones : asignacion'
    t[0] = [t[1]]

def p_asignacion(t):
    '''asignacion : IDENTIFICADOR IGUAL expresion
                  | IDENTIFICADOR CORCHETEA CORCHETEC IGUAL expresion'''
    if(t[2] == '='):        
        t[0] = (t[1],t[3])
    else:
        t[0] = (t[1],t[5])

def p_asignacion_none(t):
    '''asignacion : IDENTIFICADOR
                  | IDENTIFICADOR CORCHETEA CORCHETEC'''
    t[0] = t[1]

def p_tipo(t):
    '''tipo : INT
            | CHAR
            | DOUBLE
            | FLOAT
            | VOID'''
    t[0] = t[1]

#------------------------------EXPRESIONES
def p_expNum(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    t[0] = OpNumero(t[1])

def p_expId(t):
    'expresion : IDENTIFICADOR'
    t[0] = OpId(t[1])

def p_expCadena(t):
    'expresion : CADENA'
    t[0] = OpCadena(t[1])

#METODO PARA MANEJAR LOS ERRORES SINTACTICOS
def p_error(t):
    if t:
        desc = 'El token: ' + str(t.value) + ' no se esperaba'
        nuevo = errores.Error('SINTACTICO',desc,t.lineno,t.lexpos)
        main.Editor.tablaErrores.newError(nuevo)
        parser.errok()
    else:
        desc = 'Error sintactico al final del archivo'
        nuevo = errores.Error('SINTACTICO',desc,'EOF','EOF')
        main.Editor.tablaErrores.newError(nuevo)
        


#------------------------------------------IMPORTS
import ply.yacc as yacc
parser = yacc.yacc()

#METODO DEL PARSER
def parse(input):
    return parser.parse(input)