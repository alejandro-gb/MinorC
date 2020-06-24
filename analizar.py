#----------------------------------------ANALIZADOR LEXICO

#DICCIONARIO CON LAS PALABRAS RESERVADAS
reservadas = {
    'break':'BREAK',
    'case':'CASE',
    'char':'CHAR',
    'continue':'CONTINUE',
    'default':'DEFAULT',
    'do':'DO',
    'double':'DOUBLE',
    'else':'ELSE',
    'float':'FLOAT',
    'for':'FOR',
    'goto':'GOTO',
    'if':'IF',
    'int':'INT',
    'return':'RETURN',
    'struct':'STRUCT',
    'sizeof':'SIZEOF',
    'switch':'SWITCH',
    'void':'VOID',
    'while':'WHILE',
    'printf':'PRINTF',
    'scanf':'SCANF',
}

#LISTA DE TOKENS
tokens = [
    'CADENA',
    'CARACTER',
    'ASSING_SHIFTR',
    'ASSING_SHIFTL',
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
    'BARRA',
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
t_ASSING_SHIFTR     = r'>>='
t_ASSING_SHIFTL     = r'<<='
t_ASSING_MAS        = r'\+='
t_ASSING_MENOS      = r'-='
t_ASSING_POR        = r'\*='
t_ASSING_DIV        = r'/='
t_ASSING_MOD        = r'%='
t_ASSING_AND        = r'&='
t_ASSING_OR         = r'\|='
t_ASSING_XOR        = r'\^='
t_SHIFTR            = r'>>'
t_SHIFTL            = r'<<'
t_INCREMENTO        = r'\+\+'
t_DECREMENTO        = r'\-\-'
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
t_ANPERSAND         = r'\&'
t_ADMIRACION        = r'\!'
t_NOTBIT            = r'\~'
t_MAS               = r'\+'
t_MENOS             = r'\-'
t_POR               = r'\*'
t_BARRA             = r'\/'
t_MOD               = r'\%'
t_MAYOR             = r'\>'
t_MENOR             = r'\<'
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
    r'".*?"'
    t.value = t.value[1:-1]
    return t 

def t_CARACTER(t):
    r"'.'"
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
    nuevo = errores.Error('LEXICO',desc, t.lexer.lineno, t.lexpos)
    main.Editor.tablaErrores.newError(nuevo)
    t.lexer.skip(1)

import ply.lex as lex
import main
import errores
lexer = lex.lex()

#PRECEDENCIA
precedence = (
    ('left','COMA'),
    ('right','ASSING_SHIFTR','ASSING_SHIFTL','ASSING_MAS','ASSING_MENOS','ASSING_POR','ASSING_DIV','ASSING_MOD','ASSING_AND','ASSING_OR','ASSING_XOR'),
    ('left','OR'),#logico
    ('left','AND'),#logico
    ('left','BARRAOR'),#bits
    ('left','PICO'),#bits
    ('left','ANPERSAND'),#bits
    ('left','EQUIVALENTE','DIFERENTE'),
    ('left','MAYOR','MAYORIGUAL','MENOR','MENORIGUAL'),
    ('left','SHIFTL','SHIFTR'),
    ('left','MAS','MENOS'),
    ('left','POR','BARRA','MOD'),
    ('right','UMENOS','SIZEOF','INCREMENTO','DECREMENTO','ADMIRACION','NOTBIT'),#PUNTEROS & Y *
    ('left','PARA','PARC','CORCHETEA','CORCHETEC','PUNTO','UINC','UDEC')
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
                   | printf
                   | arreglo
                   | asignacion
                   | while
                   | etiqueta
                   | goto
                   | dowhile
                   | if
                   | switch
                   | for
                   | nula
                   | return'''
    t[0] = t[1]

def p_nula(t):
    'nula : PUNTOYCOMA'
    pass

def p_return(t):
    'return : RETURN expresion PUNTOYCOMA'
    t[0] = Return(t[2],t.lexer.lineno)

def p_prinf(t):
    'printf : PRINTF PARA listaprint PARC PUNTOYCOMA'
    t[0] = Printf(t[3],t.lexer.lineno)

def p_listprint(t):
    'listaprint : listaprint COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_soloprint(t):
    'listaprint : expresion'
    t[0] = [t[1]]

def p_funcion(t):
    '''funcion : tipo IDENTIFICADOR PARA PARC LLAVEA instrucciones LLAVEC'''
    t[0] = Funcion(t[1],t[2],t[6],t.lexer.lineno)

def p_declaracion(t):
    'declaracion : tipo lista_impasignaciones PUNTOYCOMA'
    t[0] = Declaracion(t[1],t[2],t.lexer.lineno)

def p_arreglo(t):
    'arreglo : tipo IDENTIFICADOR lista_dimension PUNTOYCOMA'
    t[0] = Arreglo(t[1],t[2],t[3],t.lexer.lineno)

def p_arreglostr(t):
    'arreglo : tipo IDENTIFICADOR CORCHETEA CORCHETEC IGUAL expresion PUNTOYCOMA'
    t[0] = Arreglo(t[1],t[2],t[6],t.lexer.lineno)

def p_lista_impasignaciones(t):
    'lista_impasignaciones : lista_impasignaciones COMA implict_asignacion'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_dimension(t):
    'lista_dimension : lista_dimension dimension'
    t[1].append(t[2])
    t[0] = t[1]

def p_una_impasignacion(t):
    'lista_impasignaciones : implict_asignacion'
    t[0] = [t[1]]

def p_una_dimension(t):
    'lista_dimension : dimension'
    t[0] = [t[1]]

def p_impasignacion(t):
    'implict_asignacion : IDENTIFICADOR IGUAL expresion'        
    t[0] = (t[1],t[3])
    
def p_dimension(t):
    'dimension : CORCHETEA expresion CORCHETEC'
    t[0] = t[2]

def p_impasignacion_none(t):
    'implict_asignacion : IDENTIFICADOR'
    t[0] = t[1]

def p_asignacion(t):
    '''asignacion : IDENTIFICADOR signoassig expresion PUNTOYCOMA
                  | IDENTIFICADOR lista_dimension IGUAL expresion PUNTOYCOMA'''
    if(t[4] == ';'):
        t[0] = Asignacion(t[1], t[3], t[2], t.lexer.lineno)
    else:
        t[0] = Asignacion(t[1], t[4], None, t.lexer.lineno,t[2])

def p_signoassig(t):
    '''signoassig : IGUAL
                  | ASSING_MAS
                  | ASSING_MENOS
                  | ASSING_POR
                  | ASSING_DIV
                  | ASSING_MOD
                  | ASSING_AND
                  | ASSING_OR
                  | ASSING_XOR
                  | ASSING_SHIFTL
                  | ASSING_SHIFTR'''
    t[0] = t[1]

def p_tipo(t):
    '''tipo : INT
            | CHAR
            | DOUBLE
            | FLOAT
            | VOID'''
    t[0] = t[1]

def p_while(t):
    'while : WHILE PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = While(t[3],t[6],t.lexer.lineno)

def p_dowhile(t):
    'dowhile : DO LLAVEA instrucciones LLAVEC WHILE PARA expresion PARC PUNTOYCOMA'
    t[0] = Dowhile(t[7],t[3],t.lexer.lineno)

def p_etiqueta(t):
    'etiqueta : IDENTIFICADOR DOSPUNTOS'
    t[0] = Etiqueta(t[1],t.lexer.lineno)

def p_goto(t):
    'goto : GOTO IDENTIFICADOR PUNTOYCOMA'
    t[0] = Goto(t[2],t.lexer.lineno)

def p_soloif(t):
    '''if : IF PARA expresion PARC LLAVEA instrucciones LLAVEC'''
    t[0] = If(t[3],t[6],t.lexer.lineno)

def p_ifelses(t):
    'if : IF PARA expresion PARC LLAVEA instrucciones LLAVEC listaifelse'
    t[0] = If(t[3],t[6],t.lexer.lineno,t[8]) 

def p_listaifelse(t):
    'listaifelse : listaifelse ifelse'
    t[1].append(t[2])
    t[0] = t[1]

def p_listasoloifelse(t):
    'listaifelse : ifelse'
    t[0] = [t[1]]

def p_ifelse(t):
    '''ifelse : ELSE IF PARA expresion PARC LLAVEA instrucciones LLAVEC
              | ELSE LLAVEA instrucciones LLAVEC'''
    if(t[2] == '{'):
        t[0] = t[3]
    elif(t[3] == '('):
        t[0] = (t[4],t[7])

def p_switch(t):
    'switch : SWITCH PARA expresion PARC LLAVEA listacasos LLAVEC'
    t[0] = Switch(t[3],t[6],t.lexer.lineno)

def p_listacasos(t):
    'listacasos : listacasos tipocaso'
    t[1].append(t[2])
    t[0] = t[1]

def p_listauncaso(t):
    'listacasos : tipocaso'
    t[0] = [t[1]]

def p_tipocaso(t):
    '''tipocaso : caso
                | default'''
    t[0] = t[1]

def p_caso(t):
    'caso : CASE expresion DOSPUNTOS instrucciones'
    t[0] = (t[2],t[4],False)
    
def p_casobreak(t):
    'caso : CASE expresion DOSPUNTOS instrucciones BREAK PUNTOYCOMA'
    t[0] = (t[2],t[4],True)

def p_default(t):
    'default : DEFAULT DOSPUNTOS instrucciones'
    t[0] = t[3]

def p_for(t):
    'for : FOR PARA inicializacion expresion PUNTOYCOMA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = For(t[3],t[4],t[6],t[9],t.lexer.lineno)

def p_inicializar(t):
    '''inicializacion : declaracion
                      | asignacion'''
    t[0] = t[1]
#------------------------------EXPRESIONES
def p_exprexion(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion BARRA expresion
                 | expresion MOD expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion EQUIVALENTE expresion
                 | expresion DIFERENTE expresion
                 | expresion AND expresion
                 | expresion OR expresion
                 | expresion PICO expresion
                 | expresion ANPERSAND expresion
                 | expresion BARRAOR expresion
                 | expresion SHIFTR expresion
                 | expresion SHIFTL expresion
                 | PARA expresion PARC'''
    if t[2] == '+' :
        t[0] = OpNormal(t[1],t[3],Aritmetica.SUMA,t.lexer.lineno)
    elif t[2] == '-' :
        t[0] = OpNormal(t[1],t[3],Aritmetica.RESTA,t.lexer.lineno)
    elif t[2] == '*' :
        t[0] = OpNormal(t[1],t[3],Aritmetica.MULTI,t.lexer.lineno)
    elif t[2] == '/' :
        t[0] = OpNormal(t[1],t[3],Aritmetica.DIV,t.lexer.lineno)
    elif t[2] == '%' :
        t[0] = OpNormal(t[1],t[3],Aritmetica.MODULO,t.lexer.lineno)
    elif t[2] == '<' :
        t[0] = OpNormal(t[1],t[3],Relacional.MENOR,t.lexer.lineno)
    elif t[2] == '>' :
        t[0] = OpNormal(t[1],t[3],Relacional.MAYOR,t.lexer.lineno)
    elif t[2] == '<=' :
        t[0] = OpNormal(t[1],t[3],Relacional.MENORIGUAL,t.lexer.lineno)
    elif t[2] == '>=' :
        t[0] = OpNormal(t[1],t[3],Relacional.MAYORIGUAL,t.lexer.lineno)
    elif t[2] == '==' :
        t[0] = OpNormal(t[1],t[3],Relacional.EQUIVALENTE,t.lexer.lineno)
    elif t[2] == '!=' :
        t[0] = OpNormal(t[1],t[3],Relacional.DIFERENTE,t.lexer.lineno)
    elif t[2] == '&&' :
        t[0] = OpNormal(t[1],t[3],Logica.AND,t.lexer.lineno)
    elif t[2] == '||' :
        t[0] = OpNormal(t[1],t[3],Logica.OR,t.lexer.lineno)
    elif t[2] == '&' :
        t[0] = OpNormal(t[1],t[3],Bits.BITAND,t.lexer.lineno)
    elif t[2] == '|' :
        t[0] = OpNormal(t[1],t[3],Bits.BITOR,t.lexer.lineno)
    elif t[2] == '^' :
        t[0] = OpNormal(t[1],t[3],Bits.BITXOR,t.lexer.lineno)
    elif t[2] == '<<' :
        t[0] = OpNormal(t[1],t[3],Bits.BITSHL,t.lexer.lineno)
    elif t[2] == '>>' :
        t[0] = OpNormal(t[1],t[3],Bits.BITSHR,t.lexer.lineno)
    else:
        t[0] = t[2]
    
def p_tern(t):
    'expresion : PARA expresion PARC INTERROGACION expresion DOSPUNTOS expresion'
    t[0] = Ternario(t[2],t[5],t[7],t.lexer.lineno)

def p_cast(t):
    'expresion : PARA tipo PARC expresion'
    t[0] = Casteo(t[2],t[4],t.lexer.lineno)

def p_expNum(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    t[0] = OpNumero(t.lexer.lineno, t[1])

def p_menosExp(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = OpMenos(t[2],t.lexer.lineno)

def p_notbit(t):
    'expresion : NOTBIT expresion'
    t[0] = OpNotbit(t[2],t.lexer.lineno)

def p_notlog(t):
    'expresion : ADMIRACION expresion'
    t[0] = OpNotlog(t[2],t.lexer.lineno)

def p_oppreinc(t):
    'expresion : INCREMENTO expresion'
    t[0] = OpInc(t[2],t.lexer.lineno)

def p_oppredec(t):
    'expresion : DECREMENTO expresion'
    t[0] = OpDec(t[2],t.lexer.lineno)

def p_oppostinc(t):
    'expresion : expresion INCREMENTO %prec UINC'
    t[0] = OpPostInc(t[1],t.lexer.lineno)

def p_oppostdec(t):
    'expresion : expresion DECREMENTO %prec UDEC'
    t[0] = OpPostDec(t[1],t.lexer.lineno)

def p_expId(t):
    'expresion : IDENTIFICADOR'
    t[0] = OpId(t[1],t.lexer.lineno)

def p_expCadena(t):
    '''expresion : CADENA
                 | CARACTER'''
    t[0] = OpCadena(t[1],t.lexer.lineno)

def p_sizeof(t):
    '''expresion : SIZEOF PARA expresion PARC
                 | SIZEOF PARA tipo PARC'''
    t[0] = OpTam(t[3],t.lexer.lineno)

#METODO PARA MANEJAR LOS ERRORES SINTACTICOS
def p_error(t):
    if t:
        desc = 'El token: ' + str(t.value) + ' no se esperaba'
        nuevo = errores.Error('SINTACTICO',desc,t.lexer.lineno+1,t.lexpos)
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