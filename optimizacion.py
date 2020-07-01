#---------------------------------CLASE QUE DEFINE UNA OPTIMIZACION PARA EL REPORTE
class Optimizacion():
    #CONSTRUCTOR RECIBE LA OPTIMIZACION Y LA DESCRIPCION
    def __init__(self, optimizacion, desc, regla, linea):
        self.optimizacion = optimizacion
        self.desc = desc
        self.linea = linea
        self.regla = regla

#---------------------------------CLASE QUE MANEJA EL REPORTE DE OPTIMIZACION
class TablaOptimizacion():

    #CONTADOR DE CADA FILA
    contador = 0
    
    #CONSTRUCTOR RECIBE UN DICCIONARIO VACIL QUE ALMACENA LAS FILAS 
    def __init__(self, optimizaciones = {}):
        self.optimizaciones = optimizaciones

    #METODO PARA AGREGAR A LA TABLA
    def newOptimizacion(self,optimizacion):
        self.contador = self.contador + 1
        self.optimizaciones[self.contador] = optimizacion 

    #METODO QUE DEVUELVE UNA FILA DE LA TABLA SEGUN SU ID O NONE
    def getOptimizacion(self, id) :
        if not id in self.optimizaciones :
            return None
        return self.optimizaciones[id]