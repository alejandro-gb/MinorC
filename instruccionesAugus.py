class Instruccion :
    '''Clase abstracta instruccion'''

class Print(Instruccion) :

    def __init__(self,  valor) :
        self.valor = valor

class GoTo(Instruccion) :
    
    def __init__(self,  id) :
        self.id = id

class Etiqueta(Instruccion) :
    
    def __init__(self, id, instrucciones=[]) :
        self.id = id
        self.instrucciones=instrucciones


class ExitInstruccion(Instruccion) :
    
    def __init__(self):
        pass

class Unset(Instruccion) :

    def __init__(self, id) :
        self.id = id

class Read(Instruccion) :
    
    def __init__(self) :
        pass


class Absoluto(Instruccion) :
   
    def __init__(self, variable) :
        self.variable=variable

class Array(Instruccion) :
   
    def __init__(self,id) :
        self.id=id

class DeclaracionAsignacion(Instruccion) :

    def __init__(self, variable, valor) :
        self.id = variable
        self.valor = valor

class AsignacionArrSt(Instruccion) :
    
    def __init__(self, variable,indices, valor) :
        self.variable = variable
        self.indices = indices
        self.valor = valor

class Asignacion(Instruccion) :
    
    def __init__(self,  variable, valor) :
        self.variable = variable
        self.valor = valor


class If(Instruccion) : 
    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones




