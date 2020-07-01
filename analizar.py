#----------------------------------------ANALIZADOR LEXICO PARA MINOR C
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
    'COMENTARIOMULTI'
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

#METODO PARA ACEPTAR UN SOLO CARACTER ENTRE COMILLAS SIMPLES
def t_CARACTER(t):
    r"'.'"
    t.value = t.value[1:-1]
    return t 

#CARACTERES IGNORADOS
t_ignore = " \t\v\f"

#METODO PARA ACEPTAR UN COMENTARIO
def t_COMENTARIO(t):
    r'//.+\n'
    t.lexer.lineno += 1

#METODO PARA ACEPTAR UN COMENTARIO MULTILINEA
def t_COMENTARIOMULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

#METODO PARA ACEPTAR UNA NUEVA LINEA Y SUMAR LA CUENTA
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#METODO PARA RECONOCER UN ERROR LEXICO
def t_error(t):
    desc = 'El caracter: ' + str(t.value[0]) + ' no es valido'
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

#----------------------------------------------ANALIZADOR SINTACTICO
from instrucciones import *
import main
import gramatical
import errores

#GRAMATICA

def p_start(t):
    'start : instrucciones'
    addProduccion('START --> INSTRUCCIONES','AST = INSTRUCCIONES.VALOR')
    t[0] = t[1]

def p_instrucciones(t):
    'instrucciones : instrucciones instruccion'
    addProduccion('INSTRUCCIONES --> INSTRUCCIONES INSTRUCCION','INSTRUCCIONES.VAL = INSTRUCCIONES.VAL + INSTRUCCION.VAL')
    t[1].append(t[2])
    t[0] = t[1]

def p_una_instruccion(t):
    'instrucciones : instruccion'
    addProduccion('INSTRUCCIONES --> INSTRUCCION','INSTRUCCIONES.VAL = INSTRUCCION.VAL')
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
                   | return
                   | break
                   | continue
                   | struct
                   | declastruct
                   | asignastruct
                   | llamada
                   | comentario'''
    t[0] = t[1]

def p_comments(t):
    '''comentario : COMENTARIO
                  | COMENTARIOMULTI'''
    pass

def p_struct(t):
    'struct : STRUCT IDENTIFICADOR LLAVEA instrucciones LLAVEC PUNTOYCOMA'
    addProduccion('STRUCT --> struct id { INSTRUCCIONES } ;','STRUCT.VAL = newstruct(id.lexval, instrucciones.val)')
    addProduccion('INSTRUCCION --> STRUCT','INSTRUCCION.VAL = STRUCT.VAL')
    t[0] = Struct(t[2],t[4],t.lexer.lineno)

def p_declastruct(t):
    'declastruct : STRUCT IDENTIFICADOR IDENTIFICADOR PUNTOYCOMA'
    addProduccion('ARREGLO --> struc id id ;', 'DECLASTRUCT.VAL = newDeclaStruct(id.lexval,id2.lexval)')
    addProduccion('INSTRUCCION --> DECLASTRUCT','INSTRUCCION.VAL = DECLASTRUCT.VAL')
    t[0] = NewStruct(t[2],t[3],t.lexer.lineno)

def p_asignastruct(t):
    'asignastruct : IDENTIFICADOR PUNTO asignacion'
    addProduccion('ASIGNASTRUCT --> id . ASIGNACION', 'ASIGNASTRUCT.VAL = newAsignastruct(id.lexval, ASIGNACION.VAL)')
    addProduccion('INSTRUCCION --> ASIGNASTRUCT','INSTRUCCION.VAL = ASIGNASTRUCT.VAL')
    t[0] = ToStruct(t[1],t[3],t.lexer.lineno)

def p_nula(t):
    'nula : PUNTOYCOMA'
    addProduccion('NULA --> ;', 'ignorar()')
    addProduccion('INSTRUCCION --> NULA',' ignorar()')
    pass

def p_return(t):
    '''return : RETURN expresion PUNTOYCOMA
              | RETURN PUNTOYCOMA'''
    if(t[2] == ';'):
        addProduccion('RETURN --> return ;', 'RETURN.VAL = newReturn( )')
        t[0] = Return(None,t.lexer.lineno)
    else:
        addProduccion('RETURN --> return EXPRESION ;', 'RETURN.VAL = newReturn(EXPRESION.VAL)')
        t[0] = Return(t[2],t.lexer.lineno)
    addProduccion('INSTRUCCION --> RETURN','INSTRUCCION.VAL = RETURN.VAL')

def p_break(t):
    'break : BREAK PUNTOYCOMA'
    addProduccion('BREAK --> break;', 'BREAK.VAL = newBreak()')
    addProduccion('INSTRUCCION --> BREAK','INSTRUCCION.VAL = BREAK.VAL')
    t[0] = Break(t.lexer.lineno)

def p_continue(t):
    'continue : CONTINUE PUNTOYCOMA'
    addProduccion('CONTINUE --> continue;', 'CONTINUE.VAL = newContinue()')
    addProduccion('INSTRUCCION --> CONTINUE','INSTRUCCION.VAL = CONTINUE.VAL')
    t[0] = Continue(t.lexer.lineno)

def p_prinf(t):
    'printf : PRINTF PARA listavalores PARC PUNTOYCOMA'
    addProduccion('PRINTF --> printf ( LISTAPRINT );','PRINTF.VAL = newPrint(LISTAPRINT.VAL)')
    addProduccion('INSTRUCCION --> PRINTF','INSTRUCCION.VAL = PRINTF.VAL')
    t[0] = Printf(t[3],t.lexer.lineno)

#def p_listprint(t):
#    'listaprint : listaprint COMA expresion'
#    addProduccion('LISTAPRINT --> LISTAPRINT , EXPRESION ','LISTAPRINT.VAL  = LISTAPRINT1.VAL + EXPRESION.VAL')
#    t[1].append(t[3])
#    t[0] = t[1]

#def p_soloprint(t):
#    'listaprint : expresion'
#    addProduccion('LISTAPRINT --> EXPRESION','LISTAPRINT.VAL = EXPRESION.VAL')
#    t[0] = [t[1]]

def p_funcion(t):
    '''funcion : tipo IDENTIFICADOR PARA opcionfunc LLAVEA instrucciones LLAVEC'''
    addProduccion('FUNCION --> TIPO id ( OPCIONFUNC ) { INSTRUCCIONES }','FUNCION.VAL = newFuncion(TIPO.VAL, id.lexval, OPCIONFUNC.VAL, instrucciones.val)')
    addProduccion('INSTRUCCION --> FUNCION','INSTRUCCION.VAL = FUNCION.VAL')
    t[0] = Funcion(t[1],t[2],t[4],t[6],t.lexer.lineno)

def p_opcionfunc(t):
    '''opcionfunc : PARC
                  | listaparams PARC'''
    if(t[1] == ')'):
        t[0] = None
    else:
        addProduccion('OPCIONFUNC --> ) | LISTAPARAMS )','OPCIONFUNC.VAL = LISTAPARAMS.VAL')
        t[0] = t[1]
    
def p_llamada(t):
    '''llamada : IDENTIFICADOR PARA PARC PUNTOYCOMA
               | IDENTIFICADOR PARA listavalores PARC PUNTOYCOMA'''
    t[0] = Call(t[1], t[3],t.lexer.lineno)

def p_listaparams(t):
    'listaparams : listaparams COMA parametro'
    addProduccion('LISTAPARAMS --> LISTAPARAMS , PARAMETRO','LISTAPARAMS.VAL = LISTAPARAMS.VAL + PARAMETRO.VAL')
    t[1].append(t[3])
    t[0] = t[1]

def p_listaparam(t):
    'listaparams : parametro'
    addProduccion('LISTAPARAMS --> PARAMETRO','LISTAPARAMS.VAL = PARAMETRO.VAL')
    t[0] = [t[1]]

def p_parametro(t):
    'parametro : tipo IDENTIFICADOR'
    addProduccion('PARAMETRO --> TIPO id','PARAMETRO.VAL = (TIPO.VAL , id.lexval)')
    t[0] = (t[1],t[2])

def p_declaracion(t):
    'declaracion : tipo lista_impasignaciones PUNTOYCOMA'
    addProduccion('DECLARACION --> TIPO LISTAIMPASIGNACIONES ;','DECLARACION.VAL = newDeclaracion(TIPO.VAL, LISTAIMPASIGNACIONES.VAL)')
    addProduccion('INSTRUCCION --> DECLARACION','INSTRUCCION.VAL = DECLARACION.VAL')
    t[0] = Declaracion(t[1],t[2],t.lexer.lineno)

def p_arreglo(t):
    'arreglo : tipo IDENTIFICADOR lista_dimension PUNTOYCOMA'
    addProduccion('ARREGLO --> TIPO id LISTADIMENSION;', 'ARREGLO.VAL = newArreglo(TIPO.VAL, id.lexval, LISTADIMENSION.VAL)')
    addProduccion('INSTRUCCION --> ARREGLO','INSTRUCCION.VAL = ARREGLO.VAL')
    t[0] = Arreglo(t[1], t[2], t[3], None, t.lexer.lineno)

def p_arregloinicializado(t):
    'arreglo : tipo IDENTIFICADOR lista_dimension IGUAL inicializacion PUNTOYCOMA'
    addProduccion('ARREGLO --> TIPO id LISTADIMENSION = INICIALIZACION;', 'ARREGLO.VAL = newArreglo(TIPO.VAL, id.lexval, LISTADIMENSION.VAL, INICIALIZACION.VAL)')
    addProduccion('INSTRUCCION --> ARREGLO','INSTRUCCION.VAL = ARREGLO.VAL')
    t[0] = Arreglo(t[1], t[2], t[3], t[5], t.lexer.lineno)

def p_inicializacion(t):
    '''inicializacion : LLAVEA listaini LLAVEC
                      | expresion'''
    if(t[1] == '{'):
        addProduccion('INICIALIZACION --> { LISTAINI }', 'INICIALIZACION.VAL = LISTAINI.VAL')
        t[0] = t[2]
    else:
        addProduccion('INICIALIZACION --> EXPRESION', 'INICIALIZACION.VAL = EXPRESION.VAL')
        t[0] = t[1]

def p_listaini(t):
    'listaini : listaini COMA inidimension'
    addProduccion('LISTAINI -->  LISTAINI , INIDIMENSION', 'LISTAINI.VAL = LISTAINI.VAL + INIDIMENSION.VAL')
    t[1].append(t[3])
    t[0] = t[1]

def p_unaini(t):
    'listaini : inidimension'
    addProduccion('LISTAINI --> INIDIMENSION', 'LISTAINI.VAL = INIDIMENSION.VAL')
    t[0] = [t[1]]

def p_inidimension(t):
    '''inidimension : LLAVEA listavalores LLAVEC
                    | listavalores'''
    if(t[1] == '{'):
        addProduccion('INIDIMENSION --> { LISTAVALORES }', 'INIDIMENSION.VAL = LISTAVALORES.VAL')
        t[0] = t[2]
    else:
        addProduccion('INIDIMENSION --> LISTAVALORES', 'INIDIMENSION.VAL = LISTAVALORES.VAL')
        t[0] = t[1]

def p_lista_impasignaciones(t):
    'lista_impasignaciones : lista_impasignaciones COMA implict_asignacion'
    addProduccion('LISTAIMPASIGNACIONES --> LISTAIMPASIGNACIONES , IMPLICITASIGNACION', 'LISTAIMPASIGNACIONES.VAL = LISTAIMPASIGNACIONES.VAL + IMPLICITASIGNACION.VAL')
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_dimension(t):
    'lista_dimension : lista_dimension dimension'
    addProduccion('LISTADIMENSION --> LISTADIMENSION DIMENSION', 'LISTADIMENSION.VAL = LISTADIMENSION.VAL + DIMENSION.VAL')
    t[1].append(t[2])
    t[0] = t[1]

def p_una_impasignacion(t):
    'lista_impasignaciones : implict_asignacion'
    addProduccion('LISTAIMPASIGNACIONES --> IMPLICITASIGNACIONES', 'LISTAIMPASIGNACIONES.VAL = IMPLICITASIGNACION.VAL')
    t[0] = [t[1]]

def p_una_dimension(t):
    'lista_dimension : dimension'
    addProduccion('LISTADIMENSION --> DIMENSION', 'LISTADIMENSION.VAL = DIMENSION.VAL')
    t[0] = [t[1]]

def p_impasignacion(t):
    'implict_asignacion : IDENTIFICADOR IGUAL expresion'
    addProduccion('IMPLICITASIGNACION --> id = EXPRESION', 'IMPLICITASIGNACION.VAL = (id.lexval, EXPRESION.VAL)')        
    t[0] = (t[1],t[3])
    
def p_dimension(t):
    '''dimension : CORCHETEA expresion CORCHETEC
                 | CORCHETEA CORCHETEC'''
    addProduccion('DIMENSION --> [] | [ EXPRESION ]', 'DIMENSION.VAL = EXPRESION.VAL')
    t[0] = t[2]

def p_impasignacion_none(t):
    'implict_asignacion : IDENTIFICADOR'
    addProduccion('IMPLICITASIGNACION --> id', 'IMPLICITASIGNACION.VAL = id.lexval')
    t[0] = t[1]

def p_asignacion(t):
    '''asignacion : IDENTIFICADOR signoassig expresion PUNTOYCOMA
                  | IDENTIFICADOR lista_dimension IGUAL expresion PUNTOYCOMA'''
    if(t[4] == ';'):
        addProduccion('ASIGNACION --> id SIGNOASSIG EXPRESION ;','ASIGNACION.VAL = newAsignacion(id.lexval,SIGNOASSIG.VAL, EXPRESION.VAL)')
        t[0] = asignacion(t[1], t[3], t[2], t.lexer.lineno)
    else:
        addProduccion('ASIGNACION --> id LISTADIMENSION = EXPRESION ;','ASIGNACION.VAL = newAsignacion(id.lexval, LISTADIMENSION.VAL, EXPRESION.VAL)')
        t[0] = asignacion(t[1], t[4], t[3], t.lexer.lineno,t[2])
    addProduccion('INSTRUCCION --> ASIGNACION','INSTRUCCION.VAL = ASIGNACION.VAL')

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
    addProduccion('SIGNOASSIG --> ' + t[1], 'SIGNOASSIG.VAL = ' + t[1])
    t[0] = t[1]

def p_tipo(t):
    '''tipo : INT
            | CHAR
            | DOUBLE
            | FLOAT
            | VOID'''
    addProduccion('TIPO --> ' + t[1], 'TIPO.VAL = ' + t[1])
    t[0] = t[1]

def p_while(t):
    'while : WHILE PARA expresion PARC LLAVEA instrucciones LLAVEC'
    addProduccion('WHILE --> while  ( EXPRESION ) { INSTRUCCIONES }', 'WHILE.VAL = newWhile(EXPRESION.VAL, INSTRUCCIONES.VAL)')
    addProduccion('INSTRUCCION --> WHILE','INSTRUCCION.VAL = WHILE.VAL')
    t[0] = While(t[3],t[6],t.lexer.lineno)

def p_dowhile(t):
    'dowhile : DO LLAVEA instrucciones LLAVEC WHILE PARA expresion PARC PUNTOYCOMA'
    addProduccion('DOWHILE --> do { INSTRUCCIONES } while ( EXPRESION ) ;', 'DOWHILE.VAL = newDowhile(INSTRUCCIONES.VAL, EXPRESION.VAL)')
    addProduccion('INSTRUCCION --> DOWHILE','INSTRUCCION.VAL = DOWHILE.VAL')
    t[0] = Dowhile(t[7],t[3],t.lexer.lineno)

def p_etiqueta(t):
    'etiqueta : IDENTIFICADOR DOSPUNTOS'
    addProduccion('ETIQUETA --> id :', 'ETIQUETA.VAL = newEtiqueta(id.lexval)')
    addProduccion('INSTRUCCION --> ETIQUETA','INSTRUCCION.VAL = ETIQUETA.VAL')
    t[0] = Etiqueta(t[1],t.lexer.lineno)

def p_goto(t):
    'goto : GOTO IDENTIFICADOR PUNTOYCOMA'
    addProduccion('GOTO --> goto id ;', 'GOTO.VAL = newGoto(id.lexval)')
    addProduccion('INSTRUCCION --> GOTO','INSTRUCCION.VAL = GOTO.VAL')
    t[0] = Goto(t[2],t.lexer.lineno)

def p_soloif(t):
    '''if : IF PARA expresion PARC LLAVEA instrucciones LLAVEC'''
    addProduccion('ARREGLO --> if ( EXPRESION ) { INSTRUCCIONES }', 'IF.VAL = newIf(EXPRESION.VAL, INSTRUCCIONES.VAL)')
    addProduccion('INSTRUCCION --> IF','INSTRUCCION.VAL = IF.VAL')
    t[0] = If(t[3],t[6],t.lexer.lineno)

def p_ifelses(t):
    'if : IF PARA expresion PARC LLAVEA instrucciones LLAVEC listaifelse'
    addProduccion('ARREGLO --> if ( EXPRESION ) { INSTRUCCIONES } LISTAIFELSE', 'IF.VAL = newIf(EXPRESION.VAL, INSTRUCCIONES.VAL, LISTAIFELSE.VAL)')
    addProduccion('INSTRUCCION --> IF','INSTRUCCION.VAL = IF.VAL')
    t[0] = If(t[3],t[6],t.lexer.lineno,t[8]) 

def p_listaifelse(t):
    'listaifelse : listaifelse ifelse'
    addProduccion('LISTAIFELSE --> LISTAIFELSE IFELSE','LISTAIFELSE.VAL = LISTAIFELSE.VAL + IFELSE.VAL')
    t[1].append(t[2])
    t[0] = t[1]

def p_listasoloifelse(t):
    'listaifelse : ifelse'
    addProduccion('LISTAIFELSE --> IFELSE','LISTAIFELSE.VAL = IFELSE.VAL')
    t[0] = [t[1]]

def p_ifelse(t):
    '''ifelse : ELSE IF PARA expresion PARC LLAVEA instrucciones LLAVEC
              | ELSE LLAVEA instrucciones LLAVEC'''
    if(t[2] == '{'):
        addProduccion('IFELSE --> else { INSTRUCCIONES }','IFELSE.VAL = INSTRUCCIONES.VAL ')
        t[0] = t[3]
    elif(t[3] == '('):
        addProduccion('IFELSE --> else if ( EXPRESION ) { INSTRUCCIONES } ','IFELSE.VAL = (EXPRESION.VAL, INSTRUCCIONES.VAL)')
        t[0] = (t[4],t[7])

def p_switch(t):
    'switch : SWITCH PARA expresion PARC LLAVEA listacasos LLAVEC'
    addProduccion('SWITCH --> switch ( EXPRESION ) { LISTACASOS } ', 'SWITCH.VAL = newSwitch(EXPRESION.VAL, LISTACASOS.VAL)')
    addProduccion('INSTRUCCION --> SWITCH','INSTRUCCION.VAL = SWITCH.VAL')
    t[0] = Switch(t[3],t[6],t.lexer.lineno)

def p_listacasos(t):
    'listacasos : listacasos tipocaso'
    addProduccion('LISTACASOS --> LISTACASOS TIPOCASO','LISTACASOS.VAL = LISTACASOS.VAL + TIPOCASO.VAL')
    t[1].append(t[2])
    t[0] = t[1]

def p_listauncaso(t):
    'listacasos : tipocaso'
    addProduccion('LISTACASOS --> TIPOCASO','LISTACASOS.VAL = TIPOCASO.VAL')
    t[0] = [t[1]]

def p_tipocaso(t):
    '''tipocaso : caso
                | default'''
    addProduccion('TIPOCASO --> CASO','TIPOCASO.VAL = CASO.VAL')
    t[0] = t[1]

def p_caso(t):
    'caso : CASE expresion DOSPUNTOS instrucciones'
    addProduccion('CASO --> case EXPRESION : INSTRUCCIONES','CASO.VAL = (EXPRESION.VAL, INSTRUCCIONES.VAL)')
    t[0] = (t[2],t[4])

def p_default(t):
    'default : DEFAULT DOSPUNTOS instrucciones'
    addProduccion('DEFAULT --> default : INSTRUCCIONES','DEFAULT.VAL = INSTRUCCIONES.VAL')
    t[0] = t[3]

def p_for(t):
    'for : FOR PARA inicializar expresion PUNTOYCOMA expresion PARC LLAVEA instrucciones LLAVEC'
    addProduccion('FOR --> for ( INICIALIZAR EXPRESION ; EXPRESION ) { INSTRUCCIONES }', 'FOR.VAL = newFor(INICIALIZAR.VAL, EXPRESION.VAL, EXPRESION2.VAL, INSTRUCCIONES.VAL)')
    addProduccion('INSTRUCCION --> FOR','INSTRUCCION.VAL = FOR.VAL')
    t[0] = For(t[3],t[4],t[6],t[9],t.lexer.lineno)

def p_inicializar(t):
    '''inicializar : declaracion
                      | asignacion'''
    addProduccion('INICIALIZAR --> DECLARACION ','INICIALIZAR.VAL = DECLARACION.VAL')
    t[0] = t[1]
#-----------------------------------------------EXPRESIONES
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
                 | expresion SHIFTL expresion'''
    addProduccion('EXPRESION --> EXPRESION '+ t[2] +' EXPRESION','EXPRESION.VAL = EXPRESION1.VAL'+ t[2]+' EXPRESION2.VAL')
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
    
def p_exppar(t):
    'expresion : PARA expresion PARC'
    addProduccion('EXPRESION --> ( E )','EXPRESION.VAL = EXPRESION1.VAL')
    t[0] = t[2]

def p_tern(t):
    'expresion : PARA expresion PARC INTERROGACION expresion DOSPUNTOS expresion'
    addProduccion('EXPRESION --> ( EXPRESION ) ? EXPRESION : EXPRESION','EXPRESION.VAL = newTernario(EXPRESION.VAL, EXPRESION2.VAL, EXPRESION3.VAL)')
    t[0] = Ternario(t[2],t[5],t[7],t.lexer.lineno)

def p_cast(t):
    'expresion : PARA tipo PARC expresion'
    addProduccion('EXPRESION --> ( TIPO ) EXPRESION','EXPRESION.VAL = newCasteo(TIPO.VAL, EXPRESION.VAL)')
    t[0] = Casteo(t[2],t[4],t.lexer.lineno)


def p_ellamada(t):
    'expresion : IDENTIFICADOR PARA listavalores PARC'
    addProduccion('EXPRESION --> id ( LISTAVALORES )','EXPRESION.VAL = newLlamada(id.lexval, LISTAVALORES.VAL)')
    t[0] = Llamada(t[1], t[3], t.lexer.lineno)

def p_listavals(t):
    'listavalores : listavalores COMA expresion'
    addProduccion('LISTAVALORES --> LISTAVALORES , EXPRESION','LISTAVALORES.VAL = LISTAVALORES.VAL + EXPRESION.VAL')
    t[1].append(t[3])
    t[0] = t[1]

def p_listaunval(t):
    'listavalores : expresion'
    addProduccion('LISTAVALORES --> EXPRESION','LISTAVALORES.VAL = EXPRESION.VAL')
    t[0] = [t[1]]

def p_expNum(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    addProduccion('EXPRESION --> numero','EXPRESION.VAL = numero.val')
    t[0] = OpNumero(t.lexer.lineno, t[1])

def p_menosExp(t):
    'expresion : MENOS expresion %prec UMENOS'
    addProduccion('EXPRESION --> -EXPRESION','EXPRESION.VAL = -EXPRESION1.VAL')
    t[0] = OpMenos(t[2],t.lexer.lineno)

def p_notbit(t):
    'expresion : NOTBIT expresion'
    addProduccion('EXPRESION --> ~E','EXPRESION.VAL = ~EXPRESION1.VAL')
    t[0] = OpNotbit(t[2],t.lexer.lineno)

def p_notlog(t):
    'expresion : ADMIRACION expresion'
    addProduccion('EXPRESION --> !EXPRESION','EXPRESION.VAL = !EXPRESION1.VAL')
    t[0] = OpNotlog(t[2],t.lexer.lineno)

def p_oppreinc(t):
    'expresion : INCREMENTO expresion'
    addProduccion('EXPRESION --> ++EXPRESION','EXPRESION.VAL = ++EXPRESION1.VAL')
    t[0] = OpInc(t[2],t.lexer.lineno)

def p_oppredec(t):
    'expresion : DECREMENTO expresion'
    addProduccion('EXPRESION --> --E','EXPRESION.VAL = --EXPRESION1.VAL')
    t[0] = OpDec(t[2],t.lexer.lineno)

def p_oppostinc(t):
    'expresion : expresion INCREMENTO %prec UINC'
    addProduccion('EXPRESION --> EXPRESION++','EXPRESION.VAL = EXPRESION1.VAL++')
    t[0] = OpPostInc(t[1],t.lexer.lineno)

def p_oppostdec(t):
    'expresion : expresion DECREMENTO %prec UDEC'
    addProduccion('EXPRESION --> EXPRESION --','EXPRESION.VAL = EXPRESION1.VAL--')
    t[0] = OpPostDec(t[1],t.lexer.lineno)

def p_expId(t):
    'expresion : IDENTIFICADOR'
    addProduccion('EXPRESION --> id','EXPRESION.VAL = id.lexval')
    t[0] = OpId(t[1],t.lexer.lineno)

def p_expCadena(t):
    '''expresion : CADENA
                 | CARACTER'''
    addProduccion('EXPRESION --> cadena','EXPRESION.VAL = cadena.lexval')
    t[0] = OpCadena(t[1],t.lexer.lineno)

def p_sizeof(t):
    '''expresion : SIZEOF PARA expresion PARC
                 | SIZEOF PARA tipo PARC'''
    addProduccion('EXPRESION --> SIZEOF( EXPRESION )','EXPRESION.VAL = SIZEOF(EXPRESION)')
    t[0] = OpTam(t[3],t.lexer.lineno)

def p_acceso(t):
    'expresion : IDENTIFICADOR lista_dimension'
    addProduccion('EXPRESION --> id LISTADIMENSION','EXPRESION.VAL = newAcceso(id.lexval, LISTADIMENSION.VAL)')
    t[0] = Acceso(t[1],t[2],t.lexer.lineno)

def p_referencia(t):
    '''expresion : ANPERSAND expresion
                 | POR expresion'''
    addProduccion('EXPRESION --> &E','EXPRESION.VAL = &EXPRESION1.VAL')
    t[0] = Referencia(t[2],t.lexer.lineno)

def p_expscan(t):
    'expresion : SCANF PARA PARC'
    addProduccion('EXPRESION --> scanf()','EXPRESION.VAL = newScan()')
    t[0] = Scanf(t.lexer.lineno)

def p_fromStruct(t):
    'expresion : IDENTIFICADOR PUNTO expresion'
    addProduccion('EXPRESION --> id . EXPRESION','EXPRESION.VAL = (id.lexval, EXPRESION.VAL)')
    t[0] = fromStruct(t[1],t[3],t.lexer.lineno)    

#METODO PARA AGREGAR UNA PRODUCCION AL REPORTE GRAMATICAL
def addProduccion(produccion, regla):
    prod = gramatical.Produccion(produccion,regla)
    main.Editor.tablagramatical.newProduccion(prod)

#METODO PARA MANEJAR LOS ERRORES SINTACTICOS
def p_error(t):
    if t:
        desc = 'El token: ' + str(t.value) + ' no se esperaba'
        nuevo = errores.Error('SINTACTICO',desc,t.lexer.lineno,t.lexpos)
        main.Editor.tablaErrores.newError(nuevo)
        parser.errok()
    else:
        desc = 'Error sintactico al final del archivo'
        nuevo = errores.Error('SINTACTICO',desc,'EOF','EOF')
        main.Editor.tablaErrores.newError(nuevo)
        return
        
#------------------------------------------IMPORTS
import ply.yacc as yacc
parser = yacc.yacc()

#METODO PARA HACER EL RECONOCIENTO RECIBE EL TEXTO A RECONOCER
def parse(input):
    lexer.lineno = 1
    parsear = parser.parse(input, lexer = lexer)
    return parsear