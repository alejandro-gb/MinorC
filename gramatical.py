#---------------------------------clase que define una produccion para el reporte
class Produccion():
    # contructor recibe la produccion y las reglas semanticas
    def __init__(self,produccion,reglas):
        self.produccion = produccion
        self.reglas = reglas

#---------------------------------clase que maneja el reporte gramatical
class TablaGramatical():

    # variable contador para agregar un identificador a cada produccion
    contador = 0
    
    # contructor recibe un diccionario de producciones vacio por defecto 
    def __init__(self, producciones = {}):
        self.producciones = producciones

    # metodo para agregar una produccion a la tabla
    def newProduccion(self,produccion):
        self.contador = self.contador + 1
        self.producciones[self.contador] = produccion 

    # metodo que devuelve una produccion de la tabla segun su id si existe o none
    def getProduccion(self, id) :
        if not id in self.producciones :
            return None
        return self.producciones[id]