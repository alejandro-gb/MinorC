#CLASE QUE DEFINE UN ERROR
class Error():
    #CONSTRUCTOR RECIBE EL TIPO, LA DESCRIPCION, LINEA Y POSICION DEL ERROR
    def __init__(self, tipo, desc, linea, pos):
        self.tipo = tipo
        self.desc = desc
        self.linea = linea
        self.pos = pos

#CLASE QUE MANEJA LA TABLA DE ERRORES
class TablaErrores():

    #CONSTRUCTOR
    def __init__(self, errores = {}):
        self.errores = errores

    #METODO QUE AGREGA UN ERROR A LA LISTA
    def newError(self, error) :
        self.errores[error.pos] = error

    #METODO QUE DEVUELVE UN ERROR
    def getError(self, pos) :
        if not pos in self.errores :
            return None
        return self.errores[pos]