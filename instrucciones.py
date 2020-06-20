from enum import Enum

#CLASE ABSTRACTA DE LA QUE DERIVAN LAS INSTRUCCIONES
class Instruccion:
    pass

#CLASE QUE MANEJA LAS FUNCIONES
class Funcion(Instruccion):
    #CONSTRUCTOR RECIBE EL TIPO Y NOMBRE DE LA FUNCION
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

#CLASE QUE MANEJA UNA ASIGNACION
class Asignacion(Instruccion):
    #CONSTRUCTOR RECIBE EL TIPO, UNA LISTA DE NOMBRES Y EL VALOR DE UNA VARIABLE
    def __init__(self, tipo, nombres, valor = None, size = 0, ambito ='global'):
        self.tipo = tipo
        self.size = size
        self.nombres = nombres
        self.valor = valor

#CLASE QUE MANEJA EL PRINTF
class Printf(Instruccion):
    #CONSTRUCTOR RECIBE UNA LISTA DE VALORES
    def __init__(self, listavalores):
        self.listavalores = listavalores
        
        

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

#CLASE QUE DEFINE LOS NUMEROS
class OpNumero(Operacion):
    #CONSTRUCTOR RECIBE EL VALOR DEL NUMERO
    def __init__(self, valor = 0):
        self.valor = valor

#CLASE QUE DEFINE LOS STRINGS
class OpCadena(Operacion):
    #CONSTRUCTOR RECIBE LA CADENA
    def __init__(self, valor):
        self.valor = valor

#CLASE QUE DEFINE LOS IDENTIFICADORES
class OpId(Operacion):
    #CONSTRUCTOR RECIBE EL IDENTIFICADOR
    def __init__(self, id):
        self.id = id
        
        
        
