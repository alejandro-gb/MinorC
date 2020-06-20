#CLASE QUE MANEJA LOS SIMBOLOS
class Simbolo():

    #CONSTRUCTOR DE UN SIMBOLO
    def __init__(self, id, temporal, tipo, valor, ambito , dimension = '', referencia = ''):
        self.id = id
        self.temporal = temporal
        self.tipo = tipo
        self.valor = valor
        self.ambito = ambito
        self.dimension = dimension
        self.referencia = referencia
    
#CLASE QUE CONTIENE LA TABLA DE SIMBOLOS
class TablaSimbolos():
    
    #CONSTRUCTOR
    def __init__(self, simbolos = {}):
        self.simbolos = simbolos

    #METODO PARA CREAR UN NUEVO SIMBOLO
    def newSimbolo(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    #METODO PARA RETORNAR UN SIMBOLO SEGUN SU ID
    def getSimbolo(self, id):
        if not id in self.simbolos:
            return None
        return self.simbolos[id]

    #METODO PARA DEFINIR UN SIMBOLO
    def setSimbolo(self,simbolo):
        if not simbolo.id in self.simbolos:
            return None
        else:
            self.simbolos[simbolo.id] = simbolo

    #METODO PARA DEFINIR EL VALOR DE UN SIMBOLO
    def setValor(self, id, valor):
        if not id in self.simbolos:
            return None
        self.simbolos[id].valor = valor

    #METODO PARA DEFINIR EL TIPO DE UN SIMBOLO
    def setTipo(self, id, tipo):
        if not id in self.simbolos:
            return None
        self.simbolos[id].tipo = tipo