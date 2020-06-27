from enum import Enum

class TIPO_DATO(Enum) :
    ENTERO = 1
    FLOTANTE = 2
    CADENA = 3
    ARREGLO = 4
    CHAR = 5
    UNDEFINED=6
    REFERENCIA=7

class Simbolo() :
    
    def __init__(self, id, tipo,valor, dimension=[],ambito="",referencia=[]) :
        self.id = id
        self.tipo = tipo
        self.valor=valor
        self.dimension=dimension
        self.ambito=ambito
        self.referencia=referencia

class Funcion():
    
    def __init__(self,id,tipo,parametros=[],referencia=[]):
        self.id=id
        self.tipo=tipo
        self.parametros=parametros
        self.referencia=referencia

class TablaDeSimbolos() :
    
    def __init__(self, simbolos = {},funciones={}) :
        self.simbolos = simbolos.copy()
        self.funciones = funciones.copy()

    def agregar(self, simbolo) :

        self.simbolos[simbolo.id] = simbolo
    
    def agregarFuncion(self,funcion):
        self.funciones[funcion.id]=funcion

    def obtenerFuncion(self,id) :
        if not id in self.funciones :
            #print('Error: funcion ',id,' no definida.')
            return None
        return self.funciones[id]

    def actualizarFuncion(self,id,tipo) :
        if not id in self.funciones :
            #print('Error: variable ',id, ' no definida.')
            pass
        else :
            self.funciones[id].tipo = tipo
    
    def actualizarRefFuncion(self,id,index) :
        if not id in self.funciones :
            #print('Error: variable ',id, ' no definida.')
            pass
        else :
            if index not in self.funciones[id].referencia:
                self.funciones[id].referencia.append(index)

    def actualizarFuncionPar(self,id,params) :
        if not id in self.funciones :
            #print('Error: variable ',id, ' no definida.')
            pass
        else :
            self.funciones[id].parametros = params 

    def obtener(self, id,rep=0) :
        if not id in self.simbolos :
            #print('Error: variable ', id, ' no definida.')
            return None
        if self.simbolos[id].tipo == TIPO_DATO.REFERENCIA:
            if rep==0 :
                return self.simbolos[id].valor
            else:
                self.simbolos[id].valor=self.simbolos[id].valor.valor
                return self.simbolos[id]
        return self.simbolos[id]

    def actualizar(self, id,tipo, valor, dimension=[]) :
        if not id in self.simbolos :
            print('Error: variable ',id, ' no definida.')
        else :
            #self.simbolos[simbolo.id] = simbolo
            self.simbolos[id].tipo = tipo
            self.simbolos[id].valor = valor
            self.simbolos[id].dimension= dimension
    
    def unset(self,id):
        if not id in self.simbolos:
            print("Error-Unset: Variable no definida")
        else:
            del self.simbolos[id]