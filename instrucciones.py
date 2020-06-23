from enum import Enum

#CLASE ABSTRACTA DE LA QUE DERIVAN LAS INSTRUCCIONES
class Instruccion:
    pass

#CLASE QUE MANEJA LAS FUNCIONES
class Funcion(Instruccion):
    #CONSTRUCTOR RECIBE EL TIPO NOMBRE DE LA FUNCION Y LA LISTA DE INSTRCCIONES
    def __init__(self, tipo, nombre, lista, linea):
        self.tipo = tipo
        self.nombre = nombre
        self.linea = linea
        self.lista = lista

#CLASE QUE MANEJA UNA DECLARACION
class Declaracion(Instruccion):
    #CONSTRUCTOR RECIBE EL TIPO, UNA LISTA DE NOMBRES Y EL VALOR DE UNA VARIABLE
    def __init__(self, tipo, nombres, linea):
        self.tipo = tipo
        self.nombres = nombres
        self.linea = linea

#CLASE QUE MANEJA LAS ASIGNACIONES
class Asignacion(Instruccion):
    #CONSTRUCTOR RECIBE EL ID Y EL VALOR
    def __init__(self, paravar, valor, linea, dimensiones = None):
        self.paravar = paravar
        self.dimensiones = dimensiones
        self.valor = valor
        self.linea = linea

#CLASE QUE MANEJA LOS ARREGLOS
class Arreglo(Instruccion):
    #CONSTRUCTOR RECIBE EL TIPO, NOMBRE, DIMENSIONES
    def __init__(self, tipo, nombre, dimensiones,linea):
        self.tipo = tipo
        self.nombre = nombre
        self.dimensiones = dimensiones
        self.linea = linea
        
#CLASE QUE MANEJA LOS CICLOS WHILE
class While(Instruccion):
    #CONSTRUCTOR RECIBE CONDICION Y LA LISTA DE INSTRUCCIONES
    def __init__(self, condicion, lista, linea):
        self.condicion = condicion
        self.lista = lista
        self.linea = linea

#CLASE QUE MANEJA LOS DOWHILE
class Dowhile(Instruccion):
    def __init__(self,condicion,lista, linea):
        self.condicion = condicion
        self.lista = lista
        self.linea = linea

#CLASE QUE MANEJA LAS ETIQUETAS
class Etiqueta(Instruccion):
    #CONSTRUCTOR RECIBE EL NOMBRE DE LA ETIQUETA
    def __init__(self,nombre,linea):
        self.nombre = nombre
        self.linea = linea

#CLASE QUE MANEJA LOS INCONDICIONALES
class Goto(Instruccion):
    #CONSTRUCTOR RECIBE EL NOMBRE DE LA ETIQUETA A LA QUE SALTA
    def __init__(self,nombre,linea):
        self.nombre = nombre
        self.linea = linea
        
#CLASE QUE MANEJA EL PRINTF
class Printf(Instruccion):
    #CONSTRUCTOR RECIBE UNA LISTA DE VALORES
    def __init__(self, listavalores,linea):
        self.listavalores = listavalores
        self.linea = linea
        
#CLASE QUE MANEJA LOS IFS 
class If(Instruccion):
    #CONSTRUCTOR RECIBE LA CONDICION Y LA LISTA DE INSTRUCCIONES DEL IF Y EL ELSE
    def __init__(self,condicion, listaif,linea, listaelse = None):
        self.condicion = condicion
        self.listaif = listaif
        self.listaelse = listaelse
        self.linea = linea

#CLASE QUE MANEJA LOS SWITCH
class Switch(Instruccion):
    #CONSTRUCTOR RECIBE LA EXPRESION, LISTA DE CASOS
    def __init__(self, expresion, listacasos, linea):
        self.listacasos = listacasos
        self.expresion = expresion
        self.linea = linea

#CLASE QUE MANEJA LOS CICLOS FOR
class For(Instruccion):
    #CONSTRUCTOR RECIBE LA INICIALIZACION, LA CONDICION , EL CAMBIO, LA LISTA DE INSTRUCCIONES
    def __init__(self, inicial,condicion,cambio,ins,linea):
        self.inicial = inicial
        self.condicion = condicion
        self.cambio = cambio
        self.ins = ins
        self.linea = linea

#CLASE PARA MANEJAR LOS RETURNS
class Return(Instruccion):
    #CONSTRUCTOR RECIBE LA EXPRESION Y LA LINEA
    def __init__(self,expresion,linea):
        self.expresion = expresion
        self.linea = linea

#CLASE QUE ENUMERA LOS TIPOS DE OPERACION ARITMETICA
class Aritmetica(Enum):
    SUMA = 1
    RESTA = 2
    MULTI = 3
    DIV = 4
    MODULO = 5

#CLASE QUE ENUMERA LOS TIPOS DE OPERACION RELACIONAL
class Relacional(Enum):
    MAYOR = 1
    MENOR = 2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    EQUIVALENTE = 5
    DIFERENTE = 6

#CLASE QUE ENUMERA LOS TIPOS DE OPERACION DE BITS
class Bits(Enum):
    BITAND = 1
    BITOR = 2
    BITXOR = 3
    BITSHL = 4
    BITSHR = 5

#CLASE QUE ENUMERA LOS TIPOS DE OPERACION LOGICA
class Logica(Enum):
    AND = 1
    OR = 2
    NOT = 3
    XOR = 4

#CLASE ABSTRACTA DE LA QUE DERIVAN LAS OPERACIONES
class Operacion():
    pass

#CLASE QUE DEFINE UNA OPERACION NORMAL
class OpNormal(Operacion):
    #CONSTRUCTOR RECIBE LOS OPERANDOS Y EL SIGNO
    def __init__(self, op1, op2, signo,linea):
        self.op1 = op1
        self.op2 = op2
        self.signo = signo
        self.linea = linea
        
#CLASE QUE DEFINE LOS NUMEROS
class OpNumero(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR DEL NUMERO
    def __init__(self, linea, valor = 0):
        self.valor = valor
        self.linea = linea

#CLASE QUE DEFINE LOS STRINGS
class OpCadena(Operacion):
    #CONSTRUCTOR RECIBE LA CADENA
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea

#CLASE QUE DEFINE LOS IDENTIFICADORES
class OpId(Operacion):
    #CONSTRUCTOR RECIBE EL IDENTIFICADOR
    def __init__(self, id, linea):
        self.id = id
        self.linea = linea

#CLASE QUE MANEJA -E
class OpMenos(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea

#CLASE QUE MANEJA ~E
class OpNotbit(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea        
        
#CLASE QUE MANEJA !E
class OpNotlog(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea  

#CLASE QUE MANEJA ++E
class OpInc(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea  

#CLASE QUE MANEJA --E
class OpDec(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea  


#CLASE QUE MANEJA E++
class OpPostInc(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea  

#CLASE QUE MANEJA E--
class OpPostDec(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR A NEGAR
    def __init__(self,exp,linea):
        self.exp = exp
        self.linea = linea 