#---------------------------------------IMPORTS
import tkinter as gui
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import time
import threading
from tkinter import PhotoImage, simpledialog
from tkinter.ttk import *
from graphviz import Digraph
import analizar
import tablaSimbolos
import errores
import ts as TS
from instruccionesAugus import *
import interprete as Inter
import gramatical
import optimizacion
from instrucciones import *


pathFile=''
comando_consola=''
ts_debug=TS.TablaDeSimbolos()
no_instruccion=0
ejecucion_automatica=1

#---------------------------------------BARRA DE MENU
class BarraDeMenu:

    # constructor recibe el componente 
    def __init__(self, parent):
        fuente = ("Arial",12)
        menubar = gui.Menu(parent.principal, font=fuente,bg='ivory4')
        parent.principal.config(menu=menubar)
        archivo = gui.Menu(menubar, font=fuente, tearoff=0)
        editar = gui.Menu(menubar, font=fuente, tearoff=0)
        ejecutar = gui.Menu(menubar, font=fuente, tearoff=0)
        opciones = gui.Menu(menubar, font=fuente, tearoff=0)
        debugin = gui.Menu(menubar, font = fuente, tearoff=0)
        ayuda = gui.Menu(menubar, font = fuente, tearoff=0)

        #lista de opciones de archivo
        archivo.add_command(label="Nuevo", command=parent.Nuevo)
        archivo.add_command(label="Abrir", command=parent.Abrir)
        archivo.add_command(label="Guardar", command=parent.Guardar)
        archivo.add_command(label="Guardar Como...", command = parent.Guardarcomo)
        archivo.add_separator()
        archivo.add_command(label="Salir", command=parent.principal.destroy)

        #lista de opciones de editar
        editar.add_command(label="Copiar", command=parent.Copiar)
        editar.add_command(label="Pegar", command=parent.Pegar)
        editar.add_command(label="Cortar", command=parent.Cortar)
        editar.add_separator()
        editar.add_command(label="Buscar", command=parent.Buscar)
        editar.add_command(label="Reemplazar", command = parent.Reemplazar)

        #lista de opciones de ejecutar
        ejecutar.add_command(label="Ejecutar", command=parent.AnalisisAsc)
        ejecutar.add_separator()
        ejecutar.add_command(label="Reporte de Errores", command=parent.VerReporteErrores)
        ejecutar.add_command(label="Tabla de simbolos", command=parent.VerTablaSimbolos)
        ejecutar.add_command(label="Reporte del AST", command=parent.VerAST)
        ejecutar.add_command(label="Reporte de Optimizacion", command=parent.VerOptimizacion)
        ejecutar.add_command(label="Reporte gramatical", command=parent.RepGramatical)

        #lista de opciones de opciones
        opciones.add_command(label="Cambiar Tema", command=parent.ColorTema)
        opciones.add_command(label="Numeros de linea", command=parent.QuitarNums)

        #lista de opciones de debugin
        debugin.add_command(label="Run debug", command= parent.SiguientePaso)
        #debugin.add_command(label="Next step", command= lambda: parent.test.set(1))
        debugin.add_command(label="Stop", command= parent.stop)
        #lista de opciones de ayuda
        ayuda.add_command(label="Ayuda", command=self.verAyuda)
        ayuda.add_separator()
        ayuda.add_command(label="Acerca De", command=self.verAcercaDe)

        #agregar los menus a la bara
        menubar.add_cascade(menu=archivo, label="Archivo")
        menubar.add_cascade(menu=editar, label="Editar")
        menubar.add_cascade(menu=ejecutar, label="Ejecutar")
        menubar.add_cascade(menu=opciones, label="Opciones")
        menubar.add_cascade(menu=debugin, label="Debug")
        menubar.add_cascade(menu=ayuda, label="Ayuda")

    # metodo para mostrar la ayuda en una alerta
    def verAyuda(self):
        messagebox.showinfo("Ayuda", "https://github.com/alejandr076/MinorC")

    # metodo para ver acerca de en una alerta
    def verAcercaDe(self):
        messagebox.showinfo("Acerca de"," Segundo proyecto de compiladores 2 \n Primer semestre 2020 \n Interprete MinorC \n Alejandro Garcia \n 201700801")

#--------------------------------------CLASE QUE MANEJA EL EDITOR DE TEXTO
class EditorAvanzado(gui.Frame):
    
    # constructor
    def __init__(self, master, *args, **kwargs):
        gui.Frame.__init__(self, *args, **kwargs)
        fuente = ("Arial",11)
        self.cuadro = gui.Text(self, selectbackground="light grey", width=120, height=20, font=fuente)
        self.scrollbar = gui.Scrollbar(self, orient=gui.VERTICAL, command=self.cuadro.yview)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.numeros_linea = NumerosLinea(self, width=20, bg='light grey')
        self.numeros_linea.attach(self.cuadro)

        self.scrollbar.pack(side=gui.RIGHT, fill=gui.Y)
        self.numeros_linea.pack(side=gui.LEFT, fill=gui.Y, padx=(5, 0))
        self.cuadro.pack(side=gui.TOP, fill=gui.BOTH, expand=True)

        self.cuadro.tag_configure("regs", foreground="firebrick4")
        self.cuadro.tag_configure("reservadas", foreground="steel blue")
        self.cuadro.tag_configure("goto", foreground="purple1")
        self.cuadro.tag_configure("signos", foreground="red")
        self.cuadro.tag_configure("agrup",foreground="orange")
        self.cuadro.tag_configure("com",foreground="gray")
        self.cuadro.tag_configure("buscar",background="sky blue")
        self.cuadro.tag_configure("normal",background="white")
        
        self.cuadro.bind("<Key>", self.delay)
        self.cuadro.bind("<Button-1>", self.numeros_linea.redraw)
        self.scrollbar.bind("<Button-1>", self.MousePress)
        self.cuadro.bind("<MouseWheel>", self.delay)

    # metodo para resaltar el lenguaje con colores
    def resaltarTexto(self, expresion, tag, inicio='1.0', fin='end', er=False):
        inicio = self.index(inicio)
        fin = self.index(fin)
        self.cuadro.mark_set("matchinicio", inicio)
        self.cuadro.mark_set("matchfin", inicio)
        self.cuadro.mark_set("limite", fin)

        contador = gui.IntVar()
        while True:
            indice = self.cuadro.search(expresion, "matchfin","limite", count=contador, regexp=er)
            
            if indice == "": break
            if contador.get() == 0: break # degenerate expresion which matches zero-length strings
            self.cuadro.mark_set("matchinicio", indice)
            self.cuadro.mark_set("matchfin", "%s+%sc" % (indice, contador.get()))
            self.cuadro.tag_add(tag, "matchinicio", "matchfin")

    # metodos que controla el mouse
    def MousePress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numeros_linea.redraw)

    def MouseRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numeros_linea.redraw)

    # metodo que redibuja el texto
    def delay(self, *args):
        self.resaltarTexto("(goto|if|struct)", "goto",er=True)
        self.resaltarTexto("(printf|scanf|break|case|char|signed|const|continue|default|do|double|else|static|float|for|if|int|return|sizeof|extern|switch|void|while)", "reservadas",er=True)
        self.resaltarTexto("(\\+|=|-|\\*|abs|%|!|\\||xor|and|\\^|<|~|\\?|>|;|:|/)", "signos",er=True)
        self.resaltarTexto("(\\[|\\]|\\(|\\)|\\{|\\})", "agrup",er=True)
        self.resaltarTexto("//(.)+([^\r\n])", "com",er=True)
        self.after(1, self.numeros_linea.redraw)

    #metodos para utilizar las funciones propias de text desde fuera
    def get(self, *args, **kwargs):
        return self.cuadro.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.cuadro.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.cuadro.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.cuadro.index(*args, **kwargs)

    def redraw(self):
        self.numeros_linea.redraw()

#--------------------------------------CLASE QUE CREA LOS NUMEROS DE LINEA
class NumerosLinea(gui.Canvas):

    #construtor
    def __init__(self, *args, **kwargs):
        gui.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.texto = None

    def attach(self, text_widget):
        self.texto = text_widget

    # actualizar los numeros
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.texto.index("@0,0")
        while True :
            dline= self.texto.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1, y, anchor="nw",text=linenum, fill="black")
            i = self.texto.index("%s+1line" % i)
            
#--------------------------------------CLASE PRINCIPAL QUE MANEJA LA INTERFAZ
class Editor:

    #VARIABLES GLOBALES
    resultado = ''
    tablaGlobal = tablaSimbolos.TablaSimbolos()
    tablaErrores = errores.TablaErrores()
    tablagramatical = gramatical.TablaGramatical()
    tablaoptimizacion = optimizacion.TablaOptimizacion()
    temp = 0
    param = 0
    numtag = 0
    numvar = 0
    numfunc = 0
    ismain = True
    iscall = False
    listaAugus = []
    stack = []
    stackLoop = []
    stackContinue = []
    returns = []
    stack2 = []
    namerecursive = ''
    isrecursive = False
    pathFile=''
    comando_consola=''
    ts_debug=TS.TablaDeSimbolos()
    no_instruccion=0
    ejecucion_automatica=1
    arbol = None
    dot = None
    i = 0
    resultadook = ''
    numbloques = 1
    lineasantes = -1
    lineasdespues = 0
    totallineas = 0
    optimizar = True

    #CONSTRUCTOR
    def __init__(self,principal):
        principal.title("Sin titulo - MinorC")
        principal.geometry("600x500")
        fuente = ("Arial",12)
        self.principal = principal
        self.nombre = None
        self.tema = 1
        self.numeros = 1
        self.test = gui.IntVar()
        self.test2 = gui.IntVar()
        self.textarea = EditorAvanzado(principal)
        self.textarea.cuadro.focus()
        self.textarea.pack(side=gui.TOP, fill=gui.BOTH, expand=True)
        self.prueba = gui.Button()
        self.photo = PhotoImage(file ="icon2.png")
        self.buttton = gui.Button(principal,image=self.photo,state='disabled', command= lambda: self.test2.set(1))
        self.buttton.pack(side=gui.LEFT,anchor=gui.N)        
        self.consola = gui.Text(principal, font=fuente, height=15, bg='dark khaki', fg="black", insertbackground='black')
        self.scrollbar = gui.Scrollbar(principal, orient=gui.VERTICAL, command=self.consola.yview)
        self.consola.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=gui.RIGHT, fill=gui.Y)
        self.consola.pack(side=gui.LEFT, fill=gui.BOTH, expand=True)
        self.menubar = BarraDeMenu(self)
        self.consola.bind("<Return>",self.comando_ingresado)

    #CAMBIAR EL TITULO DE LA VENTANA
    def CambiarTitulo(self, name=None):
        if name:
            self.principal.title(name + "- Augus")
        else:
            self.principal.title("Sin titulo - Augus")

    #CREAR UN NUEVO ARCHIVO
    def Nuevo(self):
        self.textarea.delete(1.0, gui.END)
        self.consola.delete(1.0,gui.END)
        self.nombre = None
        self.CambiarTitulo()

    #ABRIR UN ARCHIVO
    def Abrir(self):
        self.nombre = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All files","*.*"),("Python","*.py")])
        if self.nombre:
            self.textarea.delete(1.0, gui.END)
            with open(self.nombre, "r") as file:
                self.textarea.insert(1.0, file.read())
            self.CambiarTitulo(self.nombre)
            self.textarea.numeros_linea.redraw()
            self.textarea.delay()
    
    #GUARDAR EL DOCUMENTO
    def Guardar(self):
        if self.nombre:
            try:
                nuevo_contenido = self.textarea.get(1.0, gui.END)
                with open(self.nombre, "w") as file:
                    file.write(nuevo_contenido)
            except Exception as e:
                print(e)
        else:
            self.Guardarcomo()
    
    #GUARDAR COMO
    def Guardarcomo(self):
        try:
            guardar_nuevo = filedialog.asksaveasfilename(initialfile="Sin titulo.txt",defaultextension=".txt", filetypes=[("All files","*.*"),("Python","*.py")])
            nuevo_contenido = self.textarea.get(1.0, gui.END)
            with open(guardar_nuevo, "w") as file:
                file.write(nuevo_contenido)
            self.nombre = guardar_nuevo
            self.CambiarTitulo(self.nombre)
        except Exception as e:
            print(e)

    #COPIAR EL TEXTO
    def Copiar(self):
        self.textarea.clipboard_clear()
        self.textarea.clipboard_append(self.textarea.selection_get())

    #PEGAR EN EL TEXTO
    def Pegar(self):
        self.textarea.insert(gui.INSERT,self.textarea.clipboard_get())

    #CORTAR DEL TEXTO
    def Cortar(self):
        self.Copiar()
        self.textarea.delete('sel.first','sel.last')

    #BUSCAR EN EL TEXTO
    def Buscar(self):
        cadena = simpledialog.askstring('Buscar','Cadena a buscar:',parent=principal)
        self.textarea.resaltarTexto(cadena,'buscar')

    #REMPLAZAR EN EL TEXTO
    def Reemplazar(self):
        abuscar = simpledialog.askstring('Buscar','Cadena a buscar:',parent=principal)
        aremplazar = simpledialog.askstring('Reemplazar','Nueva cadena:',parent=principal)
        cadena = self.textarea.cuadro.get('1.0',gui.END)
        self.textarea.delete('1.0',gui.END)
        self.textarea.insert(gui.INSERT,cadena.replace(abuscar,aremplazar))

    def inc(self):
        self.i += 1
        return self.i

    def noOptimizar(self):
        self.optimizar = False
        self.AnalisisAsc()

    #METODO PARA HACER EL ANALISIS ASCENDENTE
    def AnalisisAsc(self):
        self.reset()
        self.consola.delete('1.0',gui.END)
        self.texto = str(self.textarea.cuadro.get('1.0',gui.END))
        self.instrucciones = analizar.parse(self.texto)
        #---------------
        self.dot = Digraph(name='AST',filename='AST',format='png')
        self.dot.node('start','start')
        self.dot.node('instrucciones','instrucciones')
        self.dot.edge('start','instrucciones')
        #---------------
        self.Interpretar(self.instrucciones, self.tablaGlobal)
        self.ReporteTablaSimbolos()
        self.ReporteErrores()
        self.totallineas += len(self.listaAugus)
        while(self.lineasantes != self.lineasdespues):
            self.lineasantes = len(self.listaAugus)
            self.OptimizarCodigo()
            for x in self.listaAugus:
                if(len(x)==0):
                    self.listaAugus.remove(x)
            self.lineasdespues = len(self.listaAugus)
            
        self.codigoOptimizado()
        self.ReporteOptimizacion()
        #print(self.resultado)
        try:
            f = open("CodigoAugus.txt","w")
            f.write(self.resultado)
            f.close
        except:
            print("Error al escribir en el archivo")
        try:
            f = open("CodigoOptimizado.txt","w")
            f.write(self.resultadook)
            f.close
        except:
            print("Error al escribir en el archivo")
        self.EjecutarAugus(self.resultado)
        if(len(self.tablaErrores.errores) != 0):
            self.VerReporteErrores()

#-------------------------------------------------------INTERPRETE---------------------------------------

    #METODO PARA INTERPRETAR LAS INSTRUCCIONES
    def Interpretar(self, instrucciones, tabla):
        #try:

            self.stack.append('global')
            self.concatenar('main:')
            self.listaAugus.append(('etiqueta','main:'))
            self.concatenar('$s0 = array();')
            self.listaAugus.append(('asignacion','$s0',' = ','array()',';'))
            self.concatenar('$s1 = array();')
            self.listaAugus.append(('asignacion','$s1',' = ','array()',';'))
            self.concatenar('$sp = -1;')
            self.listaAugus.append(('asignacion','$sp',' = ','-1',';'))
            self.concatenar('$ra = -1;')
            self.listaAugus.append(('asignacion','$ra',' = ','-1',';'))
            #BUSCAR INSTRUCCIONES GLOBALES
            for x in instrucciones:
                if   isinstance(x, Declaracion) : self.InterpretarDeclaracion(x, tabla, 'global','instrucciones')
                elif isinstance(x, Printf) : self.InterpretarPrintf(x, tabla,'instrucciones')
                elif isinstance(x, Arreglo) : self.InterpretarArreglo(x, tabla, 'global','instrucciones')
                elif isinstance(x, asignacion) : self.InterpretarAsignacion(x, tabla,'instrucciones')
                elif isinstance(x, Etiqueta) : self.InterpretarEtiqueta(x, tabla, 'global','instrucciones')
                elif isinstance(x, Goto) : self.InterpretarGoto(x, tabla, 'global','instrucciones')
                elif isinstance(x, Struct) : self.InterpretarStruct(x, tabla, 'global','instrucciones')
                elif isinstance(x, IScanf) : self.InterpretarScan(x, tabla, 'global', 'instrucciones')
            
            #BUSCAR EL MAIN
            for x in instrucciones:
                if isinstance(x,Funcion):
                    if (x.nombre == 'main'):
                        self.InterpretarMain(x, tabla,'instrucciones')
                        instrucciones.remove(x)
            
            #BUSCAR LAS DEMAS FUNCIONES
            for x in instrucciones:
                if isinstance(x,Funcion) :  
                    #self.concatenar('')
                    self.InterpretarFuncion(x, tabla,'instrucciones')
            
            if self.returns:
                #self.concatenar('\n')
                self.concatenar('saltos:')
                self.listaAugus.append(('etiqueta','saltos:'))
                for r in reversed(range(0,len(self.returns))):
                    self.concatenar('if($s0[$ra] == '+str(self.returns[r]) + ') goto pop;')
                    self.listaAugus.append(('if','if(','$s0[$ra]',' == ',str(self.returns[r]),') goto ','pop',';'))

                self.concatenar('pop:')
                self.listaAugus.append(('etiqueta','pop:'))
                self.concatenar('$s2 = $s0[$ra];')
                self.listaAugus.append(('asignacion','$s2',' = ','$s0[$ra]',';'))
                self.concatenar('$ra = $ra - 1;')
                self.listaAugus.append(('operacion','$ra',' = ','$ra',' - ','1',';'))
                for r in reversed(range(0,len(self.returns))):
                    self.concatenar('if($s2 == '+str(self.returns[r]) + ') goto ra'+str(self.returns[r])+';')
                    self.listaAugus.append(('if','if(','$s2',' == ',str(self.returns[r]),') goto ','ra'+str(self.returns[r]),';'))
                                
        #except:
        #    messagebox.showerror('ERROR','NO SE INTERPRETO')

    #METODO PARA INTERPRETAR INSTRUCCIONES INTERNAS
    def InterpretarIns(self, lista, tabla, nombre, padre = None):
        for x in lista:
            if   isinstance(x, Declaracion)  : self.InterpretarDeclaracion(x, tabla, nombre, padre)
            elif isinstance(x, Printf)       : self.InterpretarPrintf(x,tabla, padre)
            elif isinstance(x, Arreglo)      : self.InterpretarArreglo(x,tabla,nombre, padre)
            elif isinstance(x, asignacion)   : self.InterpretarAsignacion(x,tabla, padre)
            elif isinstance(x, While)        : self.InterpretarWhile(x,tabla,nombre, padre)
            elif isinstance(x, Dowhile)      : self.InterpretarDowhile(x,tabla,nombre, padre)
            elif isinstance(x, Etiqueta)     : self.InterpretarEtiqueta(x,tabla,nombre, padre)
            elif isinstance(x, Goto)         : self.InterpretarGoto(x,tabla,nombre, padre)
            elif isinstance(x, If)           : self.InterpretarIf(x,tabla,nombre, padre)
            elif isinstance(x, Switch)       : self.InterpretarSwitch(x,tabla,nombre, padre)
            elif isinstance(x, Return)       : self.InterpretarReturn(x,tabla, padre)
            elif isinstance(x, Break)        : self.InterpretarBreak(x,tabla, padre)
            elif isinstance(x, Continue)     : self.InterpretarContinue(x,tabla, padre)
            elif isinstance(x, Operacion)    : self.InterpretarOperacion(x,tabla, padre)
            elif isinstance(x, For)          : self.InterpretarFor(x,tabla,nombre, padre)
            elif isinstance(x, Struct)       : self.InterpretarStruct(x, tabla, nombre, padre)
            elif isinstance(x, NewStruct)    : self.InterpretarNewStruct(x, tabla, nombre, padre)
            elif isinstance(x, ToStruct)     : self.InterpretarToStruct(x, tabla, nombre, padre)
            elif isinstance(x, Call)         : self.InterpretarCall(x, tabla, padre)
            elif isinstance(x, IScanf)       : self.InterpretarScan(x, tabla, nombre, padre)
            elif isinstance(x, Funcion)      : self.errorSemantico('CORE_DUMPED',x.linea,'No se pueden hacer funciones anidadas')
            
    #METODO PARA INTERPRETAR UNA FUNCION
    def InterpretarFuncion(self, funcion, tabla, padre = None):
        tipo    = funcion.tipo
        nombre  = funcion.nombre
        params  = funcion.listaparam
        ins     = funcion.lista
        
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Funcion')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',tipo)
        self.dot.node(tree + 'h2',nombre)
        self.dot.node(tree + 'h3','parametros')
        self.dot.node(tree + 'h4','instrucciones')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        self.dot.edge(tree,tree + 'h3')
        self.dot.edge(tree,tree + 'h4')
        #---------AST
        
        num = self.getId()
        simbolo = tablaSimbolos.Simbolo(num, nombre, '', tipo, 'Funcion', 'global')
        tabla.newSimbolo(simbolo)
        self.stack.append(nombre)
        self.concatenar(nombre + ':')
        self.listaAugus.append(('etiqueta',nombre + ':'))
        self.namerecursive = nombre
        nump = 0
        if params:
            for param in params:
                #-----------AST
                numparam = str(self.inc())
                nameparam = numparam + 'param'
                self.dot.node(nameparam, param[1])
                self.dot.edge(tree + 'h3', nameparam)
                #-----------AST
                nums = self.getId()
                #temporal = self.newTemp()
                val = '$a'+str(nump)
                simbolo = tablaSimbolos.Simbolo(nums, param[1], val, param[0], val, nombre)
                tabla.newSimbolo(simbolo)
                #self.concatenar(temporal + ' = ' + str(val) + ';')
                nump +=1;
        
        self.InterpretarIns(ins, tabla, nombre, tree + 'h4')
        self.concatenar('goto saltos;')
        self.listaAugus.append(('salto','goto ','saltos',';'))
        self.stack.pop()

    #METODO PARA INTERPRETAR UNA LLAMADA A FUNCION
    def InterpretarCall(self, llamada, tabla, padre):
        nombre = llamada.id
        params = llamada.listaparam
        funcion = self.BuscarSimbolo(nombre,tabla)

        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Llamada')
        self.dot.edge(padre, tree)
        self.dot.node(tree + '1', nombre)
        self.dot.node(tree + '2','ListaParamtros')
        self.dot.edge(tree, tree + '1')
        self.dot.edge(tree, tree + '2')
        #---------AST

        self.returns.append(self.numfunc)
        self.concatenar('$ra = $ra + 1;')
        self.listaAugus.append(('operacion','$ra',' = ','$ra',' + ','1',';'))
        self.concatenar('$s0[$ra] = '+str(self.numfunc)+';')
        self.listaAugus.append(('asignacion','$s0[$ra]',' = ',str(self.numfunc),';'))
        #TIENE PARAMETROS
        if(type(params) is list):
            contparam = 0
            for param in params:
                parametro = self.InterpretarOperacion(param, tabla, tree + '2')
                tipo = parametro[0]
                val = str(parametro[1])
                par = '$a'+str(contparam)
                self.concatenar(par + ' = ' + val + ';')
                self.listaAugus.append(('asignacion',par,' = ',val,';'))
                self.concatenar('$sp = $sp + 1;')
                self.listaAugus.append(('operacion','$sp',' = ','$sp',' + ','1',';'))
                self.concatenar('$s1[$sp] = ' + par + ';' )
                self.listaAugus.append(('asignacion','$s1[$sp]',' = ',par,';'))
                contparam += 1
                    
        self.concatenar('goto ' + nombre +';')
        self.listaAugus.append(('salto','goto ',nombre,';'))
        self.concatenar('ra' + str(self.numfunc) + ':')
        self.listaAugus.append(('etiqueta','ra' + str(self.numfunc) + ':'))
        self.numfunc += 1
            
    #METODO PARA INTERPRETAR UNA FUNCION
    def InterpretarMain(self, funcion, tabla, padre = None):
        ins = funcion.lista
        
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree, 'Funcion')
        self.dot.edge(padre, tree)
        self.dot.node(tree + 'h1', 'int')
        self.dot.node(tree + 'h2', 'main')
        self.dot.node(tree + 'h3', 'instrucciones')
        self.dot.edge(tree, tree + 'h1')
        self.dot.edge(tree, tree + 'h2')
        self.dot.edge(tree, tree + 'h3')
        #---------AST
        
        num = self.getId()
        simbolo = tablaSimbolos.Simbolo(num, 'main', '', 'int', 'Funcion', 'global')
        tabla.newSimbolo(simbolo)
        self.stack.append('main')
        self.InterpretarIns(ins,tabla,'main', tree + 'h3')
        self.concatenar('exit;')
        self.listaAugus.append(('salida','exit;'))
        self.stack.pop()
        self.ismain = False
        #self.iscall = False

    #METODO PARA INTERPRETAR UNA ETIQUETA
    def InterpretarEtiqueta(self,ins,tabla,ambito, padre = None):
        nomTag = ins.nombre
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree, 'Etiqueta')
        self.dot.edge(padre, tree)
        self.dot.node(tree + 'h1', nomTag)
        self.dot.edge(tree, tree + 'h1')
        #---------AST
        self.concatenar(nomTag + ':')
        self.listaAugus.append(('etiqueta',nomTag + ':'))


    #METODO PARA INTERPRETAR UN SALTO GOTO
    def InterpretarGoto(self,ins,tabla,ambito, padre = None):
        nomTag = ins.nombre
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree, 'Goto')
        self.dot.edge(padre, tree)
        self.dot.node(tree + 'h1', nomTag)
        self.dot.edge(tree, tree + 'h1')
        #---------AST
        self.concatenar('goto ' + nomTag + ';')
        self.listaAugus.append(('salto','goto ',nomTag,';'))

    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarReturn(self, ret, tabla, padre = None):
        if ret.expresion is not None:
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree, 'Return')
            self.dot.edge(padre, tree)
            self.dot.node(tree + 'h1', 'Expresion')
            self.dot.edge(tree, tree + 'h1')
            
            #---------AST
            
            if(self.ismain == False):
                exp = self.InterpretarOperacion(ret.expresion, tabla, tree + 'h1')
                exptipo = exp[0]
                expval = str(exp[1])
                self.concatenar('$v0 = ' + expval +';')
                self.listaAugus.append(('asignacion','$v0',' = ',expval,';'))
                self.concatenar('goto saltos;')
                self.listaAugus.append(('salto','goto ','saltos',';'))

    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarBreak(self,ret,tabla, padre = None):
        fin = self.stackLoop[-1]
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree, 'Break')
        self.dot.edge(padre, tree)
        #---------AST
        self.concatenar('goto ' + fin + ';')
        self.listaAugus.append(('salto','goto ',fin,';'))


    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarContinue(self,ret,tabla, padre = None):
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree, 'Continue')
        self.dot.edge(padre, tree)
        #---------AST
        inicio = self.stackContinue[-1]
        self.concatenar('goto ' + inicio + ';')
        self.listaAugus.append(('salto','goto ',inicio,';'))

    #METODO PARA INTERPRETAR UN FOR
    def InterpretarFor(self, ciclo, tabla, ambito, padre = None):
        inicio = ciclo.inicial
        condicion = ciclo.condicion
        cambio = ciclo.cambio
        lista = ciclo.ins

        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'For')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','Inicial')
        self.dot.node(tree + 'h2','condicion')
        self.dot.node(tree + 'h3','cambio')
        self.dot.node(tree + 'h4','instrucciones')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        self.dot.edge(tree,tree + 'h3')
        self.dot.edge(tree,tree + 'h4')
        #---------AST

        nombre = self.newTag('for') #ETIQUETA INICIO
        verdadero = nombre + 'V'    #ETIQUETA VERDADERA
        falso = nombre + 'F'        #ETIQUETA FALSA
        actualizar = nombre + 'A'   #ETIQUETA ACTUALIZAR
        
        self.stack.append(nombre)
        self.stackLoop.append(falso)
        self.stackContinue.append(actualizar)

        self.addOpti(2,"Codigo invariante: El valor inicial solo se calcula una vez dentro del bucle",str(ciclo.linea),24)
        if isinstance(inicio, Declaracion):
            self.InterpretarDeclaracion(inicio,tabla,nombre,tree + 'h1')
        elif isinstance(inicio, asignacion):
            self.InterpretarAsignacion(inicio,tabla,tree + 'h1')
        self.concatenar(nombre + ':')
        self.listaAugus.append(('etiqueta',nombre + ':'))
        resultado = self.InterpretarOperacion(condicion, tabla, tree + 'h2')
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + verdadero + ';')
        self.listaAugus.append(('if','if(',cond,') goto ', verdadero,';'))
        self.concatenar('goto ' + falso + ';')
        self.listaAugus.append(('salto','goto ',falso,';'))
        self.concatenar(actualizar + ':')
        self.listaAugus.append(('etiqueta',actualizar + ':'))
        self.InterpretarOperacion(cambio, tabla, tree + 'h3')
        self.concatenar('goto '+ nombre +';')
        self.listaAugus.append(('salto','goto ',nombre,';'))
        self.concatenar(verdadero +':')
        self.listaAugus.append(('etiqueta',verdadero +':'))
        self.InterpretarIns(lista, tabla, nombre, tree + 'h4')
        self.concatenar('goto '+ actualizar +';')
        self.listaAugus.append(('salto','goto ',actualizar,';'))        
        self.concatenar(falso +':')
        self.listaAugus.append(('etiqueta',falso + ':'))
        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()
        
    #METODO PARA INTERPRETAR UN IF
    def InterpretarIf(self, ciclo, tabla, ambito, padre = None):
        condicion   = ciclo.condicion
        insif       = ciclo.listaif
        listaelse  = ciclo.listaelse
        
        #--------------------------------------------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'If')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','condicion')
        self.dot.node(tree + 'h2','instrucciones')
        self.dot.node(tree + 'h3','listaelse')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        self.dot.edge(tree,tree + 'h3')
        #--------------------------------------------AST
        
        nombre      = self.newTag('if')
        verdadero   = nombre + 'V'
        falso       = nombre + 'F'
        fin         = nombre +'end'
        hayelse     = False

        self.stack.append(nombre)

        resultado = self.InterpretarOperacion(condicion, tabla, tree + 'h1')
        cond = resultado[1]
        self.concatenar('if(!' + cond + ') goto ' + falso + ';')
        self.listaAugus.append(('if','if(!',cond,') goto ', falso,';'))
        self.InterpretarIns(insif, tabla, nombre, tree + 'h2')
        self.concatenar('goto ' + fin + ';')
        self.listaAugus.append(('salto','goto ',fin,';'))
        self.concatenar(falso + ':')
        self.listaAugus.append(('etiqueta',falso + ':'))

        self.addOpti(1,"Negando la concidion del if se elimina un salto innecesario.",ciclo.linea,3)
        self.totallineas += 2        
        if(listaelse is not None):
             for x in listaelse:
                 if(type(x) is tuple):
                     condicionx = x[0]
                     listax = x[1]
                     
                     #-----------AST
                     newifelse = str(self.inc())
                     newname = newifelse + 'p'
                     self.dot.node(newname, 'Else If')
                     self.dot.edge(tree + 'h3', newname)
                     #-----------AST

                     nombrex = self.newTag('elseif')
                     falsox = nombrex + 'F'
                     resultadox = self.InterpretarOperacion(condicionx, tabla, newname)
                     condx = resultadox[1]
                     self.concatenar('if(!' + condx + ') goto ' + falsox + ';')
                     self.listaAugus.append(('if','if(!',condx,') goto ', falsox,';'))
                     self.InterpretarIns(listax, tabla, nombre, newname)
                     self.concatenar('goto ' + fin + ';')
                     self.listaAugus.append(('salto','goto ',fin,';'))
                     self.concatenar(falsox + ':')
                     self.listaAugus.append(('etiqueta',falsox + ':'))
                 else:
                    #------------AST
                    self.dot.node(tree + 'else', 'Else')
                    self.dot.edge(tree + 'h3', tree + 'else')
                    #------------AST
                    self.InterpretarIns(x, tabla, nombre, tree + 'else')
                    
        self.concatenar(fin + ':')
        self.listaAugus.append(('etiqueta',fin + ':'))
        self.stack.pop()

    #METODO PARA INTERPRETAR LOS SWITCHS
    def InterpretarSwitch(self, ciclo, tabla, ambito, padre = None):
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Switch')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','Expresion')
        self.dot.node(tree + 'h2','ListaCasos')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        exp = self.InterpretarOperacion(ciclo.expresion,tabla,tree + 'h1')
        exptipo = exp[0]
        expval = exp[1]
        lista = ciclo.listacasos   
        tag = self.newTag('switch')
        fin = tag + 'Fin'
        
        self.stack.append(tag)
        self.stackLoop.append(fin)
        
        scontador = 0
        haydef = False
        for caso in lista:
            #CASO NORMAL
            if(type(caso) is tuple):
                #---------AST
                numast = str(self.inc())
                nameast = numast + 'p'
                self.dot.node(nameast,'Caso')
                self.dot.edge(tree + 'h2',nameast)
                #---------AST
                aevaluar =self.InterpretarOperacion(caso[0],tabla,nameast)
                restipo = aevaluar[0]
                resvalor = aevaluar[1]
                if self.VerificarTipo(exptipo,restipo):
                    if (restipo == 'char'):
                        resvalor = "'"+resvalor+"'"
                    cuerpo = caso[1]
                    #conbreak = caso[2]
                    namecase = tag+str(scontador)
                    if(scontador != 0):
                        previa = tag+str(scontador-1)
                        self.concatenar(previa+':')
                        self.listaAugus.append(('etiqueta',previa+':'))
                    scontador += 1
                    self.concatenar('if(' + str(expval) + ' != ' + str(resvalor) + ') goto ' + namecase + ';')
                    self.listaAugus.append(('if','if(',str(expval),' != ',str(resvalor),') goto ',namecase,';'))
                    self.InterpretarIns(cuerpo,tabla,tag,nameast)
                else:
                    self.errorSemantico('TYPE_ERROR',ciclo.linea,'El tipo a evaluar debe ser igual que evaluado')
            #DEFAULT
            else:
                #---------AST
                numdefast = str(self.inc())
                namedefast = numdefast + 'p'
                self.dot.node(namedefast,'Default')
                self.dot.edge(tree + 'h2',namedefast)
                #---------AST
                haydef = True
                tagdef = tag + str(scontador-1)
                self.concatenar(tagdef + ':')
                self.listaAugus.append(('etiqueta',tagdef + ':'))
                self.InterpretarIns(caso,tabla,tag,namedefast)
        if not haydef:
            self.concatenar(tag+str(scontador-1)+':')
            self.listaAugus.append(('etiqueta',tag+str(scontador-1)+':'))            
        self.concatenar(fin + ':')
        self.listaAugus.append(('etiqueta',fin+':'))            

        self.stack.pop()
        self.stackLoop.pop()

    #METODO PARA INTERPRETAR UN DOWHILE
    def InterpretarDowhile(self,ciclo,tabla,ambito, padre = None):
        condicion = ciclo.condicion
        ins = ciclo.lista
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Dowhile')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','Condicion')
        self.dot.node(tree + 'h2','Instrucciones')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        regreso = self.newTag('dowhile')
        falso = regreso + 'F'
        
        self.stack.append(regreso)
        self.stackLoop.append(falso)
        self.stackContinue.append(regreso)

        self.concatenar(regreso + ':')
        self.listaAugus.append(('etiqueta',regreso+':'))            

        self.InterpretarIns(ins,tabla,regreso,tree + 'h2')
        resultado = self.InterpretarOperacion(condicion, tabla, tree + 'h1')
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + regreso + ';')
        self.listaAugus.append(('if','if(',cond,') goto ', regreso,';'))
        self.concatenar(falso + ':')
        self.listaAugus.append(('etiqueta',falso+':'))            

        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()

    #METODO PARA INTERPRETAR UN WHILE
    def InterpretarWhile(self,ciclo,tabla,ambito, padre = None):
        condicion = ciclo.condicion
        ins = ciclo.lista
        
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'While')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','Condicion')
        self.dot.node(tree + 'h2','Instrucciones')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST

        regreso = self.newTag('while')  #ETIQUETA INICIO
        verdadero = regreso + 'V'       #ETIQUETA VERDADERA
        falso = regreso + 'F'           #ETIQUETA FALSA
        
        self.stack.append(regreso)
        self.stackLoop.append(falso)
        self.stackContinue.append(regreso)

        self.concatenar(regreso+':')
        self.listaAugus.append(('etiqueta',regreso+':'))
        resultado = self.InterpretarOperacion(condicion,tabla,tree + 'h1')
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + verdadero + ';')
        self.listaAugus.append(('if','if(',cond,') goto ', verdadero,';'))
        self.concatenar('goto ' + falso + ';')
        self.listaAugus.append(('salto','goto ',falso,';'))
        self.concatenar(verdadero + ':')
        self.listaAugus.append(('etiqueta',verdadero+':'))
        self.InterpretarIns(ins,tabla,regreso,tree + 'h2')
        self.concatenar('goto ' + regreso + ';')
        self.listaAugus.append(('salto','goto ',regreso,';'))
        self.concatenar(falso + ':')
        self.listaAugus.append(('etiqueta',falso+':'))
        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()
    
    #METODO PARA INTERPRETAR UN PRINTF
    def InterpretarPrintf(self,ins,tabla, padre = None):
        lista = ins.listavalores
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Printf')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','ListaValores')
        self.dot.edge(tree,tree + 'h1')
        #---------AST
        forma = self.InterpretarOperacion(lista[0],tabla,tree + 'h1')
        newtipo = forma[0]
        newval = forma[1]
        toconcat = ''
        if(newtipo != 'char'):
            self.errorSemantico('FORMAT_ERROR',ins.linea,'Se debe definir el formato de lo que se imprime')
            return
        try:
            for i in range(1,len(lista)):
                resultado = self.InterpretarOperacion(lista[i],tabla,tree + 'h1')
                restipo = resultado[0]
                resval = resultado[1]
                tprint = 'print(' + str(resval) + ');'
                if((restipo == 'int' or restipo == 'void') and ('%d' in newval or '%i' in newval)):
                    if('%d' in newval):
                        newval = newval.replace('%d','',1)
                    elif('%i' in newval):
                        newval = newval.replace('%i','',1)
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                elif((restipo == 'float' or restipo == 'double' or restipo == 'void') and '%f' in newval):
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%f','',1)
                elif((restipo == 'char' or restipo == 'void') and '%c' in newval):
                    if('$' in str(resval)):
                        tprint = "print(" + str(resval) + ");"
                    else:
                        tprint = "print('" + str(resval) + "');"
                    toconcat += tprint + '\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%c','',1)
                elif((restipo == 'char*' or restipo == 'void') and '%s' in newval):
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%s','',1)
                else:
                    self.errorSemantico('FORMAT_ERROR',ins.linea,'El formato para imprimir no concuerda con el tipo de la variable')
            tprint = 'print(\'' + str(newval) + '\');'
            if(str(newval) != ''):
                self.concatenar(tprint)
                self.listaAugus.append(('print',tprint))
                self.concatenar('print("\\n");')
                self.listaAugus.append(('print','print("\\n");'))
            if(toconcat != ''):
                self.concatenar(toconcat)
                self.listaAugus.append(('print',toconcat))
        except IndexError:
            self.errorSemantico('INDEX_ERROR',ins.linea,'Se intenta imprimir fuera de rango')
        except:
            self.errorSemantico('NONETYPE_ERROR',ins.linea,'Se intenta imprimir un valor que no existe')
     
    #METODO PARA INTERPRETAR UN SCANF COMO EN C
    def InterpretarScan(self, ins, tabla, ambito, padre = None):
        lista = ins.listavalores
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Scanf')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1','ListaValores')
        self.dot.edge(tree,tree + 'h1')
        #---------AST
        forma = self.InterpretarOperacion(lista[0],tabla,tree + 'h1')
        newtipo = forma[0]
        newval = forma[1]
        if(('%' in newval) == False):
            self.errorSemantico('FORMAT_ERROR',ins.linea,'Se debe definir el formato de lo que se lee')
            return
        for i in range(1,len(lista)):
            resultado = self.InterpretarOperacion(lista[i],tabla,tree + 'h1')
            restipo = resultado[0]
            resval = str(resultado[1])
            if('&' in resval):
                resval = resval.replace('&','')
            if((restipo == 'int' or restipo == 'void') and ('%d' in newval or '%i' in newval)):
                if('%d' in newval):
                    newval = newval.replace('%d','',1)
                elif('%i' in newval):
                    newval = newval.replace('%i','',1)
                self.concatenar(resval + ' = read();')
                self.listaAugus.append(('read',resval,' = read();'))
            elif((restipo == 'float' or restipo == 'double' or restipo == 'void') and '%f' in newval):
                newval = newval.replace('%f','',1)
                self.concatenar(resval + ' = read();')
                self.listaAugus.append(('read',resval,' = read();'))
            elif((restipo == 'char' or restipo == 'void') and '%c' in newval):
                newval = newval.replace('%c','',1)
                self.concatenar(resval + ' = read();')
                self.listaAugus.append(('read',resval,' = read();'))
            elif((restipo == 'char*' or restipo == 'void') and '%s' in newval):
                newval = newval.replace('%s','',1)
                self.concatenar(resval + ' = read();')
                self.listaAugus.append(('read',resval,' = read();'))
            else:
                self.errorSemantico('FORMAT_ERROR',ins.linea,'El formato para imprimir no concuerda con el tipo de la variable')

    #METODO PARA INTERPRETAR UNA DECLARACION
    def InterpretarDeclaracion(self, ins, tabla, ambito, padre = None):
        tipo = ins.tipo.lower()
        valor = ''
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Declaracion')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',tipo)
        self.dot.node(tree + 'h2','ListaNombres')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        for nombre in ins.nombres:
            #try:
                if((type(nombre) is str and self.VerificarAmbito(nombre, ambito ,tabla)) or (self.VerificarAmbito(nombre[0], ambito, tabla))):
                    temporal = self.newTemp()
                    num = self.getId()
                    #SOLO IDENTIFICADOR
                    if(type(nombre) is str):
                        if  (tipo == 'int'): valor = 0
                        elif(tipo == 'char'): valor = "''"
                        elif(tipo == 'float'): valor = 0.0
                        elif(tipo == 'double'): valor = 0.0
                        else: valor = 'None'
                        #---------AST
                        numnew = str(self.inc())
                        treenew = numnew + 'p'
                        self.dot.node(treenew,'Variable')
                        self.dot.edge(tree + 'h2',treenew)
                        self.dot.node(treenew + 'h1',nombre)
                        self.dot.edge(treenew, treenew + 'h1')
                        #---------AST
                        simbolo = tablaSimbolos.Simbolo(num, nombre, temporal, tipo, valor, ambito)
                        tabla.newSimbolo(simbolo)
                        self.concatenar(temporal + ' = ' + str(valor) + ';')
                        self.listaAugus.append(('asignacion',temporal,' = ',str(valor),';'))
                    #IDENTIFICADOR VALOR
                    elif(type(nombre) is tuple):
                        identificador = nombre[0]
                        #---------AST
                        numnew = str(self.inc())
                        treenew = numnew + 'p'
                        self.dot.node(treenew,'Variable')
                        self.dot.edge(tree + 'h2',treenew)
                        self.dot.node(treenew + 'h1',identificador)
                        self.dot.edge(treenew, treenew + 'h1')
                        #---------AST
                        val = self.InterpretarOperacion(nombre[1], tabla, treenew, temporal)
                        newtipo = val[0]
                        valor = val[1]
                        if(self.VerificarTipo(newtipo, tipo)):#VERIFICAR TIPO
                            if(newtipo == 'char'):
                                if(len(valor) == 1):
                                    valor = "'" + valor + "'"
                                    simbolo = tablaSimbolos.Simbolo(num, identificador, temporal, tipo, valor, ambito)
                                    tabla.newSimbolo(simbolo)
                                    self.concatenar(temporal + ' = ' + str(valor) + ';')
                                    self.listaAugus.append(('asignacion',temporal,' = ',str(valor),';'))
                                    return
                                else:
                                    self.errorSemantico('TYPE_ERROR',ins.linea,'Un caracter nada mas')
                                    return
                            simbolo = tablaSimbolos.Simbolo(num, identificador, temporal, tipo, valor, ambito)
                            tabla.newSimbolo(simbolo)
                            if(type(valor) is not bool):
                                self.concatenar(temporal + ' = ' + str(valor) + ';')
                                self.listaAugus.append(('asignacion',temporal,' = ',str(valor),';'))

                        else:
                            self.errorSemantico('TYPE_ERROR',ins.linea,'El tipo debe ser el mismo')
                else:
                    self.errorSemantico('VARIABLE_ERROR',ins.linea,'La variable ya ha sido declarada anteriormente')
            #except:
             #   self.errorSemantico('TYPE_ERROR',ins.linea,'No se pudo asignar el valor (type)')

    #METODO PARA INTERPRETAR UN STRUCT
    def InterpretarStruct(self, ins, tabla, ambito, padre = None):
        idstruct = ins.id
        listains = ins.lista
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Struct')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',idstruct)
        self.dot.node(tree + 'h2','Instrucciones')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        temporal = self.newTemp()
        num = self.getId()
        valor = []
        self.concatenar(temporal + ' = array();')
        self.listaAugus.append(('asignacion',temporal,' = ','array()',';'))
        for ins in listains:
            #---------AST
            numnew = str(self.inc())
            treenew = numnodo + 'p'
            self.dot.node(treenew,'Variable')
            self.dot.edge(tree + 'h2',treenew)
            #---------AST
            if isinstance(ins, Declaracion):
                tipo = ins.tipo
                for nombre in ins.nombres:
                    #---------AST
                    self.dot.node(nombre+numnew,nombre)
                    self.dot.edge(treenew,nombre+numnew)
                    self.dot.node(tipo+numnew,tipo)
                    self.dot.edge(treenew,tipo+numnew)
                    #---------AST
                    valor.append((tipo,nombre))
            elif isinstance(ins, Arreglo):
                tipo = ins.tipo
                opciones = ins.nombre
                for opcion in opciones:
                    nombre = opcion[0]
                    #--------AST
                    self.dot.node(nombre + numnew,nombre)
                    self.dot.edge(treenew,nombre + numnew)
                    self.dot.node(tipo + numnew,tipo)
                    self.dot.edge(treenew, tipo + numnew)
                    #--------AST
                    dimensiones = opcion[1]
                    valor.append((tipo,nombre,'array'))
            else:
                self.errorSemantico('INSTRUCTION_ERROR',ins.linea,'en un struct solo se declaran variables')
        simbolo = tablaSimbolos.Simbolo(num, idstruct, temporal, 'STRUCT', valor, ambito, [])
        tabla.newSimbolo(simbolo)

    #CLASE QUE MANEJA LA DECLARACION DE UN STRUCT
    def InterpretarNewStruct(self, ins, tabla, ambito, padre = None):
        sim = self.BuscarSimbolo(ins.idstruct,tabla)
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'NewStruct')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',ins.idstruct)
        self.dot.node(tree + 'h2',ins.idvar)
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        if sim is None:
            self.errorSemantico('VARIABLE_ERROR',ins.linea,'La variable no existe')
        else:
            if(sim.tipo == 'STRUCT'):
                sizeval = ''
                newtemp = ''
                if ins.listadim is not None:
                    for dim in ins.listadim:
                        newtemp = self.newTemp()
                        self.concatenar(newtemp + ' = array();')
                        self.listaAugus.append(('asignacion',newtemp,' = ','array()',';'))
                        size = self.InterpretarOperacion(dim, tabla, tree+'h2')
                        sizeval = size[1]
                num = self.getId()
                simbolo = tablaSimbolos.Simbolo(num, ins.idvar, newtemp, sim.nombre, len(sim.dimension),ambito, sizeval)
                sim.dimension.append(len(sim.dimension))
                tabla.newSimbolo(simbolo)
            else:
                self.errorSemantico('TYPE_ERROR',ins.linea,'La variable no es un struct')

    #CLASE QUE MANEJA LA ASIGNACION A UN STRUCT
    def InterpretarToStruct(self,ins,tabla,ambito, padre = None):
        sim = self.BuscarSimbolo(ins.id, tabla)
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'NewStruct')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',ins.id)
        self.dot.node(tree + 'h2','Asignacion')
        self.dot.edge(tree,tree + 'h1')
        self.dot.edge(tree,tree + 'h2')
        #---------AST
        if sim is None:
            self.errorSemantico('VARIABLE_ERROR',ins.linea,'no es parte del struct')
        else:
            struct = self.BuscarSimbolo(sim.tipo,tabla)
            temp = struct.temporal
            asig = ins.asigna
            parte = asig.paravar
            valor = self.InterpretarOperacion(asig.valor, tabla, tree + 'h2')
            valtipo = valor[0]
            valval = valor[1]
            dims = ins.listadim
            if dims is not None:
                for d in dims:
                    result = self.InterpretarOperacion(d, tabla, tree+'h1')
                    resval = result[1]
                    temp = temp + '[' + str(resval) + ']'
            if(asig.dimensiones is None):
                if(valtipo == 'char'):
                    valval = "'"+valval+"'"
                self.concatenar(temp + "[" + str(sim.valor) + "]['"+parte+"'] = " + str(valval) + ';')
                self.listaAugus.append(('asignacion',temp + "[" + str(sim.valor) + "]['"+parte+"']",' = ',str(valval),';'))
            else:
                toconcat = temp + "[" + str(sim.valor) + "]['" + parte + "']"
                for dimension in asig.dimensiones:
                    posicion = self.InterpretarOperacion(dimension,tabla,tree + 'h2')
                    val = posicion[1]
                    toconcat += '[' + str(val) + ']'
                extra = str(resval)
                extra2 = toconcat
                toconcat += ' = ' + extra + ';'
                
                self.concatenar(toconcat)
                self.listaAugus.append(('asignacion',extra2,' = ',extra,';'))


    #METODO PRA INTERPRETAR UNA ASIGNACION
    def InterpretarAsignacion(self, ins, tabla, padre = None):
        paravar = ins.paravar
        simbolo = self.BuscarSimbolo(paravar, tabla)
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Asignacion')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',paravar)
        self.dot.node(tree + 'h2',ins.signo)
        self.dot.node(tree + 'h3','Valor')
        self.dot.edge(tree, tree + 'h1')
        self.dot.edge(tree, tree + 'h2')
        self.dot.edge(tree, tree + 'h3')
        #---------AST
        if(simbolo is not None):
            paratemp = simbolo.temporal
            signo = ins.signo
            exp = self.InterpretarOperacion(ins.valor, tabla, tree + 'h3', paratemp)
            newtipo = exp[0]
            newval = exp[1]
            if(self.VerificarTipo(newtipo,simbolo.tipo)):
                #ID = E;
                if(ins.dimensiones is None):
                    if(type(newval) is not bool):
                        if(newtipo == 'char'):
                            newval = "'" + newval + "'"
                        if(signo == '='):
                            self.concatenar(simbolo.temporal + ' = ' + str(newval) + ';')
                            self.listaAugus.append(('asignacion',simbolo.temporal,' = ',str(newval),';'))
                            simbolo.valor = newval
                        elif(signo == '+='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' + ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' + ',str(newval),';'))
                        elif(signo == '-='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' - ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' - ',str(newval),';'))
                        elif(signo == '*='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' * ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' * ',str(newval),';'))
                        elif(signo == '/='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' / ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' / ',str(newval),';'))
                        elif(signo == '%='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' % ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' % ',str(newval),';'))
                        elif(signo == '<<='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' << ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' << ',str(newval),';'))
                        elif(signo == '>>='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' >> ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' >> ',str(newval),';'))
                        elif(signo == '&='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' & ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' & ',str(newval),';'))
                        elif(signo == '|='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' | ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' | ',str(newval),';'))
                        elif(signo == '^='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' ^ ' + str(newval) + ' ; ')
                            self.listaAugus.append(('operacion',simbolo.temporal,' = ',simbolo.temporal,' ^ ',str(newval),';'))
                #ASIGNAR A ARREGLO
                else:
                    self.dot.node(tree + 'h4','ListaDimensiones')
                    self.dot.edge(tree, tree + 'h4')
                    expre = simbolo.temporal
                    numdim = simbolo.dimension
                    valor = simbolo.valor
                    if(len(numdim) == len(ins.dimensiones)):
                        for x in range(0,len(ins.dimensiones)):
                            posicion = self.InterpretarOperacion(ins.dimensiones[x],tabla,tree + 'h4')
                            val = posicion[1]
                            expre += '[' + str(val) + ']'
                            try:
                                simbolo.valor[val] = newval
                            except:
                                simbolo.valor.append(newval)
                        expre += ' = ' + str(newval) + ';'
                        self.concatenar(expre)
                        self.listaAugus.append(('nop',expre))
                    else:
                        self.errorSemantico('INDEX_ERROR',ins.linea,'Index out range (#dimension)')
            else:
                self.errorSemantico('TYPE_ERROR',ins.linea,'El tipo debe ser el mismo as')
        else:
            self.errorSemantico('NONE_ERROR',ins.linea,'La variable no ha sido declarada')

    #METODO PARA INTERPRETAR UN ARREGLO
    def InterpretarArreglo(self, ins, tabla, ambito, padre = None):
        tipo = ins.tipo
        opciones = ins.nombre
        #dimensiones = ins.dimensiones
        #listaval = ins.listavalores
        valor = []
        #---------AST
        numnodo = str(self.inc())
        tree = numnodo + 'p'
        self.dot.node(tree,'Arreglo')
        self.dot.edge(padre,tree)
        self.dot.node(tree + 'h1',tipo)
        self.dot.node(tree + 'h2','Arreglo')
        self.dot.node(tree + 'h3','LISTADIMENSIONES')
        self.dot.node(tree + 'h4','LISTAVALORES')
        self.dot.edge(tree, tree + 'h1')
        self.dot.edge(tree, tree + 'h2')
        self.dot.edge(tree, tree + 'h3')
        self.dot.edge(tree, tree + 'h4')
        #---------AST
        for opcion in opciones:
            nombre = opcion[0]
            dimensiones = opcion[1]
            listaval = None
            if(len(opcion) == 3):
                listaval = opcion[2]
            if self.VerificarAmbito(nombre,ambito,tabla):
                ide = self.getId()
                temporal = self.newTemp()
                #TIPO ID LISTADIMENSIONES ;
                numdim = len(dimensiones)
                dims = []
                for x in dimensiones:
                    if(type(x) is str):
                        dims.append(100)
                    else:
                        val = self.InterpretarOperacion(x, tabla,tree + 'h3')
                        newtipo = val[0]
                        newval = val[1]
                        dims.append(newval)
                    
                self.concatenar(temporal + ' = ' + 'array();')
                self.listaAugus.append(('asignacion',temporal,' = ','array()',';'))
                if(listaval is not None):
                    if(type(listaval) is not list):
                        resultado = self.InterpretarOperacion(listaval,tabla,tree + 'h4')
                        valor = resultado[1]
                        tipo = 'char*'
                        simbolo = tablaSimbolos.Simbolo(ide, nombre, temporal, tipo, valor, ambito)
                        tabla.newSimbolo(simbolo)
                        if('$' in valor):
                            self.concatenar(temporal + ' = ' + valor + ';')
                            self.listaAugus.append(('asignacion',temporal,' = ',valor,';'))
                        else:    
                            self.concatenar(temporal + ' = ' + "'" + valor + "';")
                            self.listaAugus.append(('asignacion','$s0',' = ',"'" + valor + "'",';'))
                        return
                    else:
                        for x in range(0,len(listaval)):
                            for y in range(0,len(listaval[x])):
                                resultado = self.InterpretarOperacion(listaval[x][y],tabla,tree + 'h4')
                                restipo = resultado[0]
                                resval = resultado[1]
                                if self.VerificarTipo(tipo, restipo):
                                    valor.append(resval)
                                    if(len(dimensiones) == 1):
                                        if(len(listaval[x]) < dims[0]+1 ):
                                            self.concatenar(temporal + '['+str(y)+'] = '+str(resval)+';')
                                            self.listaAugus.append(('asignacion',temporal + '['+str(y)+']',' = ',str(resval),';'))

                                        else:
                                            self.errorSemantico('INDEX_ERROR',ins.linea,'Exeso de elementos en el inicializador del array')
                                    else:
                                        if(len(listaval) < dims[0]+1):
                                            if(len(listaval[x]) < dims[1]+1):
                                                self.concatenar(temporal + '['+str(x)+']['+str(y)+'] = '+str(resval)+';')
                                                self.listaAugus.append(('asignacion',temporal + '['+str(x)+']['+str(y)+']',' = ',str(resval),';'))

                                            else:
                                                self.errorSemantico('INDEX_ERROR',ins.linea,'Exeso de elementos en el inicializador del array')
                                        else:
                                            self.errorSemantico('INDEX_ERROR',ins.linea,'Exeso de elementos en el inicializador del array')
                                else:
                                    self.errorSemantico('TYPE_ERROR',ins.linea,'Los elementos del arreglo deben ser del mismo tipo')
            
                for x in range(0,len(dims)):
                    if(dims[x] == 100):
                        dims[x] = None
                simbolo = tablaSimbolos.Simbolo(ide, nombre, temporal, tipo, valor, ambito, dims)
                tabla.newSimbolo(simbolo)
            else:
                self.errorSemantico('VARIABLE_ERROR',ins.linea,'La variable ya ha sido declarada anteriormente')

    #METODO PARA VERIFICAR SI LOS TIPOS SON IGUALES
    def VerificarTipo(self, tipo1, tipo2):
        if(tipo1 == 'int' and (tipo2 == 'int' or tipo2 == 'double')):
            return True
        elif(tipo1 == 'float' and (tipo2 == 'float' or tipo2 == 'double' or tipo2 == 'int')):
            return True
        elif(tipo1 == 'double' and (tipo2 == 'double' or tipo2 == 'float')):
            return True
        elif(tipo1 == 'char' and tipo2 == 'char'):
            return True
        elif(tipo2 == 'void' or tipo1 == 'void'):
            return True
        else:
            return False

    #METODO PARA VERIFICAR EL AMBITO DE LAS VARIABLES
    def VerificarAmbito(self, nombre, ambito, tabla):
        for sim in tabla.simbolos:
            simbolo = tabla.getSimbolo(sim)
            nom = simbolo.nombre
            am = simbolo.ambito
            if(nom == nombre and am == ambito):
                return False
        return True

    #METODO PARA BUSCAR UN SIMBOLO EN LA TABLA CON EL AMBITO NECESARIO
    def BuscarSimbolo(self, nombre, tabla):
        tempstack = self.stack.copy()
        while tempstack:
            ambito = tempstack[-1]
            for sim in tabla.simbolos:
                simbolo = tabla.getSimbolo(sim)
                nom = simbolo.nombre
                am = simbolo.ambito
                if(nom == nombre and am == ambito):
                    return simbolo
            
            tempstack.pop()
        return None

    #METODO PARA VERIFICAR EL TIPO DE LAS OPERACIONES
    def checkOperacionTipo(self, t1,t2):
        if(t1 == 'int' and t2 == 'int'):
            return 'int'
        elif(t1 == 'float' or t2 == 'float'):
            return 'float'
        elif(t1 == 'int' and t2 == 'double'):
            return 'int'
        elif(t1 == 'int' and t2 == 'float'):
            return 'int'
        elif(t1 == 'double' or t2 == 'double'):
            return 'float'
        elif(t1 == 'char' or t2 == 'char'):
            return 'char'
        else:
            return None

    #METODO PARA INTERPRETAR UNA OPERACION 
    def InterpretarOperacion(self, operacion, tabla, padre = None, var = None):
        if isinstance(operacion, OpNumero):
            tipo = ''
            valor = operacion.valor
            if(type(valor) is int):
                tipo = 'int'
            elif(type(valor) is float):
                tipo = 'float'
            #---------AST
            #numnodo = str(self.inc())
            #tree = numnodo + 'p'
            #self.dot.node(tree,str(valor))
            #self.dot.edge(padre,tree)
            #---------AST
            return (tipo,valor)
        elif isinstance(operacion, OpNormal):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            
            op1 = self.InterpretarOperacion(operacion.op1,tabla,tree + '1')
            op2 = self.InterpretarOperacion(operacion.op2,tabla,tree + '3')
            signo = operacion.signo

            if(op1 != None and op2 != None):
                tipo1 = op1[0]
                val1 = op1[1]
                tipo2 = op2[0]
                val2 = op2[1]
                valor1 = str(val1)
                valor2 = str(val2)

                self.dot.node(tree + '1',valor1)
                self.dot.node(tree + '3',valor2)
                self.dot.edge(padre,tree + '1')
                self.dot.edge(padre,tree + '2')
                self.dot.edge(padre,tree + '3')
                #---------AST

                #ARITMETICAS
                if signo == Aritmetica.SUMA:
                    self.dot.node(tree + '2','+')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' + ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' + ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' + ' + valor2
                        return (restipo , nval)       
                elif signo == Aritmetica.RESTA:
                    self.dot.node(tree + '2','-')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' - ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' - ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' - ' + valor2
                        return (restipo , nval)
                elif signo == Aritmetica.MULTI:
                    self.dot.node(tree + '2','*')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' * ' + valor2 + ';'
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' * ',valor2,';'))
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' * ' + valor2
                        return (restipo , nval)
                elif signo == Aritmetica.DIV:
                    self.dot.node(tree + '2','/')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' / ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' / ',valor2,';'))
                        valor1 = temp
                        return ('double', temp)
                    else:
                        nval = valor1 + ' / ' + valor2
                        return ('double' , nval)
                elif signo == Aritmetica.MODULO:
                    self.dot.node(tree + '2','%')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' % ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' % ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' % ' + valor2
                        return (restipo , nval)
                    
                #RELACIONALES
                elif signo == Relacional.MAYOR:
                    self.dot.node(tree + '2','>')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' > ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' > ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' > ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MENOR:
                    self.dot.node(tree + '2','<')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' < ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' < ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' < ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MAYORIGUAL:
                    self.dot.node(tree + '2','>=')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' >= ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' >= ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' >= ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MENORIGUAL:
                    self.dot.node(tree + '2','<=')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' <= ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' <= ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' <= ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.EQUIVALENTE:
                    self.dot.node(tree + '2','==')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo == 'char'):
                        valor2 = "'" + valor2 + "'"
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' == ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' == ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' == ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.DIFERENTE:
                    self.dot.node(tree + '2','!=')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' != ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' != ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' != ' + valor2
                        return (restipo , nval)
                    
                #LOGICOS
                elif signo == Logica.AND:
                    self.dot.node(tree + '2','&&')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' && ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' && ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' && ' + valor2
                        return (restipo , nval)
                elif signo == Logica.OR:
                    self.dot.node(tree + '2','||')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' || ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' || ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' || ' + valor2
                        return (restipo , nval)

                #BITS
                elif signo == Bits.BITAND:
                    self.dot.node(tree + '2','&')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' & ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' & ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' & ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITOR:
                    self.dot.node(tree + '2','|')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' | ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' | ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' | ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITXOR:
                    self.dot.node(tree + '2','^')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' ^ ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' ^ ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' ^ ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITSHL:
                    self.dot.node(tree + '2','<<')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' << ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' << ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' << ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITSHR:
                    self.dot.node(tree + '2','>>')
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' >> ' + valor2 + ';'
                        self.concatenar(temporal)
                        self.listaAugus.append(('operacion',temp,' = ',valor1,' >> ',valor2,';'))
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' >> ' + valor2
                        return (restipo , nval)
                else:
                    return None
            else:
                self.errorSemantico('OPERATION_ERROR',operacion.linea,'Operacion invalida (operandos?)')
                return None

                return None
        elif isinstance(operacion, OpCadena):
            cadena = operacion.valor
            if('\\n' in cadena):
                cadena = cadena.replace('\\n','')
            if("\\'" in cadena):
                cadena = cadena.replace("\\'","'")
            if("\\\\" in cadena):
                cadena = cadena.replace("\\\\","\\")
            if("\\t" in cadena):
                cadena = cadena.replace("\\t","    ")
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,str(cadena))
            self.dot.edge(padre,tree)
            #---------AST
            return ('char',cadena)
        elif isinstance(operacion, OpId):
            variable = self.BuscarSimbolo(operacion.id,tabla)
            if(variable == None):
                self.errorSemantico('UNDEFINED_VARIABLE',operacion.linea,'La variable no existe')
                return None
            else:
                tipo = variable.tipo
                temporal = variable.temporal
                #---------AST
                numnodo = str(self.inc())
                tree = numnodo + 'p'
                self.dot.node(tree,operacion.id)
                self.dot.edge(padre,tree)
                #---------AST
                return(tipo,temporal)
        elif isinstance(operacion, Acceso):
            variable = self.BuscarSimbolo(operacion.id,tabla)
            lista = operacion.lista
            if(variable == None):
                self.errorSemantico('UNDEFINED_VARIABLE',operacion.linea,'La variable no existe')
                return None
            else:
                if(type(variable.dimension) is list):
                    strtoreturn = variable.temporal
                    for x in range(0,len(lista)):
                        posicion = self.InterpretarOperacion(lista[x],tabla,padre)
                        postipo = posicion[0]
                        posval = str(posicion[1])
                        #if( posicion[1] < variable.dimension[x]):
                        strtoreturn += '['+posval+']'
                        #else:
                        #    self.errorSemantico('INDEX_VARIABLE',operacion.linea,'La posicion no existe')
                    return(variable.tipo,strtoreturn)
                else:
                    self.errorSemantico('TYPE_VARIABLE',operacion.linea,'La variable no es arreglo')
                    return None
        elif isinstance(operacion, OpMenos):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            
            exp = self.InterpretarOperacion(operacion.exp,tabla,tree + '2')
            newtipo = exp[0]
            temp = self.newTemp()
            self.concatenar(temp + ' = -' + str(exp[1]) + ';')
            self.listaAugus.append(('unaria',temp,' = ','-',str(exp[1]),';'))
            newval ='-' + str(exp[1])

            self.dot.node(tree + '1','-')
            self.dot.node(tree + '2',str(exp[1]))
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo,temp)
        elif isinstance(operacion, OpNotbit):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            
            exp = self.InterpretarOperacion(operacion.exp, tabla, tree + '2')
            newtipo = exp[0]
            temp = self.newTemp()
            self.concatenar(temp + ' = ~' + str(exp[1]) + ';')
            self.listaAugus.append(('unaria',temp,' = ','~',str(exp[1]),';'))
            newval = '~'+str(exp[1])
            
            self.dot.node(tree + '1','~')
            self.dot.node(tree + '2',str(exp[1]))
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo,temp)
        elif isinstance(operacion, OpNotlog):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'

            exp = self.InterpretarOperacion(operacion.exp, tabla, tree + '2')
            newtipo = exp[0]
            temp = self.newTemp()
            self.concatenar(temp + ' = !' + str(exp[1]) + ';')
            self.listaAugus.append(('unaria',temp,' = ','!',str(exp[1]),';'))
            newval = '!'+str(exp[1])
            
            self.dot.node(tree + '1','!')
            self.dot.node(tree + '2',str(exp[1]))
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo,temp)
        elif isinstance(operacion, OpTam):
            restipo = ''
            resval = ''
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            if (type(operacion.exp) is str):
                restipo = operacion.exp
            else:
                res = self.InterpretarOperacion(operacion.exp, tabla, tree + '2')
                restipo = res[0]
                resval = res[1]
            if(restipo == 'int'):
                resval = 4
            elif(restipo == 'char'):
                resval = 1
            elif(restipo == 'float'):
                resval = 4
            elif(restipo == 'double'):
                resval = 8
            else:
                self.errorSemantico('TYPE_ERROR',operacion.linea,'Sizeof de tipos basicos')
                resval = 0
            self.dot.node(tree + '1','Sizeof')
            self.dot.node(tree + '2',str(resval))
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return('int',resval)
        elif isinstance(operacion, OpInc):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            
            exp = self.InterpretarOperacion(operacion.exp, tabla, tree + '2')
            newtipo = exp[0]
            newval = str(exp[1])
            asignar = newval + ' = ' + newval + ' + 1;'
            self.listaAugus.append(('operacion',newval,' = ',newval,' + ','1',';'))
            self.concatenar(asignar)
            if var is not None:    
                newasig = var + ' = ' + newval + ';'
                self.concatenar(newasig)
                self.listaAugus.append(('asignacion',var,' = ',newval,';'))

            self.dot.node(tree + '1','++')
            self.dot.node(tree + '2',newval)
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST            
            return(newtipo , True)
        elif isinstance(operacion, OpDec):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'

            exp = self.InterpretarOperacion(operacion.exp,tabla, tree + '2')
            newtipo = exp[0]
            newval = str(exp[1])
            asignar = newval + ' = ' + newval + ' - 1;'
            self.concatenar(asignar)
            self.listaAugus.append(('operacion',newval,' = ',newval,' - ','1',';'))
            if var is not None:    
                newasig = var + ' = ' + newval + ';'
                self.concatenar(newasig)
                self.listaAugus.append(('asignacion',var,' = ',newval,';'))
            
            self.dot.node(tree + '1','--')
            self.dot.node(tree + '2',newval)
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo , True)
        elif isinstance(operacion, OpPostInc):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'

            exp = self.InterpretarOperacion(operacion.exp, tabla, tree + '1')
            newtipo = exp[0]
            newval = str(exp[1])
            if var is not None:
                asignar = var + ' = ' + newval + ';'
                self.concatenar(asignar)
                self.listaAugus.append(('asignacion',var,' = ',newval,';'))

            newasig = newval + ' = ' + newval + ' + 1;'
            self.concatenar(newasig)
            self.listaAugus.append(('operacion',newval,' = ',newval,' + ','1',';'))

            
            self.dot.node(tree + '1',newval)
            self.dot.node(tree + '2','++')
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo , True)
        elif isinstance(operacion, OpPostDec):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'

            exp = self.InterpretarOperacion(operacion.exp, tabla, tree + '1')
            newtipo = exp[0]
            newval = str(exp[1])
            if var is not None:
                asignar = var + ' = ' + newval + ';'
                self.concatenar(asignar)
                self.listaAugus.append(('asignacion',var,' = ',newval,';'))
            newasig = newval + ' = ' + newval + ' - 1;'
            self.concatenar(newasig)
            self.listaAugus.append(('operacion',newval,' = ',newval,' - ','1',';'))


            self.dot.node(tree + '1',newval)
            self.dot.node(tree + '2','--')
            self.dot.edge(padre,tree + '1')
            self.dot.edge(padre,tree + '2')
            #---------AST
            return(newtipo, True)
        elif isinstance(operacion, Ternario):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'Ternario')
            self.dot.edge(padre, tree)
            self.dot.node(tree + '1','condicion')
            self.dot.node(tree + '2','verdadero')
            self.dot.node(tree + '3','falso')
            self.dot.edge(tree, tree + '1')
            self.dot.edge(tree, tree + '2')
            self.dot.edge(tree, tree + '3')
            #---------AST

            condicion =self.InterpretarOperacion(operacion.condicion, tabla, tree + '1')
            condval = condicion[1]
            estrue =self.InterpretarOperacion(operacion.verdadero, tabla, tree + '2')
            truetipo = estrue[0]
            trueval = estrue[1]
            esfalse = self.InterpretarOperacion(operacion.falso, tabla, tree + '3')
            falsetipo = esfalse[0]
            falseval = esfalse[1]
            tag = self.newTag('ternario')
            tagV = tag + 'V'
            tagF = tag + 'F'
            tagFin = tag + 'E'
            self.concatenar('if(' + condval + ') goto '+ tagV + ';')
            self.listaAugus.append(('if','if(',condval,') goto ', tagV,';'))
            self.concatenar('goto ' + tagF + ';' )
            self.listaAugus.append(('salto','goto ',tagF,';'))
            self.concatenar(tagV + ':')
            self.listaAugus.append(('etiqueta',tagV+':'))
            self.concatenar(var + ' = ' + str(trueval) + ';')
            self.listaAugus.append(('asignacion',var,' = ',str(trueval),';'))
            self.concatenar('goto ' + tagFin + ';' )
            self.listaAugus.append(('salto','goto ',tagFin,';'))
            self.concatenar(tagF + ':')
            self.listaAugus.append(('etiqueta',tagF+':'))
            self.concatenar(var + ' = ' + str(falseval) + ';')
            self.listaAugus.append(('asignacion',var,' = ',str(falseval),';'))
            self.concatenar(tagFin + ':')
            self.listaAugus.append(('etiqueta',tagFin+':'))

            return(truetipo,True)
        elif isinstance(operacion, Casteo):
            tipo = operacion.tipo
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'Cast')
            self.dot.edge(padre, tree)
            self.dot.node(tree + '1',tipo)
            self.dot.node(tree + '2','expresion')
            self.dot.edge(tree, tree + '1')
            self.dot.edge(tree, tree + '2')
            #---------AST
            if(tipo == 'double'):
                tipo = 'float'
            exp = self.InterpretarOperacion(operacion.expresion, tabla, tree + '2')
            exptipo = exp[0]
            expval = exp[1]
            self.concatenar(expval + ' = (' + tipo + ')' + expval + ';')
            self.listaAugus.append(('cast',expval,' = ','('+tipo+')',expval,';'))
            return(tipo,expval)
        elif isinstance(operacion, Llamada):
            nombre = operacion.id
            params = operacion.lista
            funcion = self.BuscarSimbolo(nombre,tabla)
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'Llamada')
            self.dot.edge(padre, tree)
            self.dot.node(tree + '1', nombre)
            self.dot.node(tree + '2','ListaParamtros')
            self.dot.edge(tree, tree + '1')
            self.dot.edge(tree, tree + '2')
            #---------AST

            self.returns.append(self.numfunc)
            self.concatenar('$ra = $ra + 1;')
            self.listaAugus.append(('operacion','$ra',' = ','$ra',' + ','1',';'))
            self.concatenar('$s0[$ra] = '+str(self.numfunc)+';')
            self.listaAugus.append(('asignacion','$s0[$ra]',' = ',str(self.numfunc),';'))
            #TIENE PARAMETROS
            if(type(params) is list):
                contparam = 0
                for param in params:
                    parametro = self.InterpretarOperacion(param, tabla, tree + '2')
                    tipo = parametro[0]
                    val = str(parametro[1])
                    par = '$a'+str(contparam)
                    self.concatenar(par + ' = ' + val + ';')
                    self.listaAugus.append(('asignacion',par,' = ',val,';'))

                    self.concatenar('$sp = $sp + 1;')
                    self.listaAugus.append(('operacion','$sp',' = ','$sp',' + ','1',';'))
                    self.concatenar('$s1[$sp] = ' + par + ';')
                    self.listaAugus.append(('asignacion','$s1[$sp]',' = ',par,';'))

                    contparam += 1
                    
            self.concatenar('goto ' + nombre +';')
            self.listaAugus.append(('salto','goto ',nombre,';'))
            self.concatenar('ra' + str(self.numfunc) + ':')
            self.listaAugus.append(('etiqueta','ra' + str(self.numfunc)+':'))
            contparam = 0
            for param in params:
                if(self.ismain == False):
                    self.concatenar('$sp = $sp - 1;')
                    self.listaAugus.append(('operacion','$sp',' = ','$sp',' - ','1',';'))
                self.concatenar('$a' + str(contparam) + ' = $s1[$sp];')
                self.listaAugus.append(('asignacion','$a' + str(contparam),' = ','$s1[$sp]',';'))
                contparam += 1
            self.numfunc += 1
                
            return('int','$v0')
        elif isinstance(operacion, Referencia):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'Referencia')
            self.dot.edge(padre, tree)
            #---------AST
            resultado = self.InterpretarOperacion(operacion.exp, tabla, tree + '1')
            restipo = resultado[0]
            resval = resultado[1]
            tostr = '&'+str(resval)

            self.dot.node(tree + '1', tostr)
            self.dot.edge(tree, tree + '1')

            return(restipo,tostr)
        elif isinstance(operacion, fromStruct):
            objeto = self.BuscarSimbolo(operacion.ide,tabla)
                                    
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'fromStruct')
            self.dot.edge(padre, tree)
            self.dot.node(tree + '1', operacion.ide)
            self.dot.node(tree + '2','Expresion')
            self.dot.edge(tree, tree + '1')
            self.dot.edge(tree, tree + '2')
            #---------AST

            if objeto is not None:
                objetoname = objeto.nombre
                objetonum = objeto.valor
                objetotipo = objeto.tipo
                struct = self.BuscarSimbolo(objetotipo,tabla)
                if struct is not None:
                    toreturn = ''
                    if operacion.listadim is not None:
                        strtemp = ''
                        for i in operacion.listadim:
                            restemp = self.InterpretarOperacion(i,tabla,tree+'h1')
                            restempval = str(restemp[1])
                            strtemp += '[' + restempval + ']'
                        toreturn = struct.temporal + strtemp +'['+ str(objetonum) + ']'
                    else:
                       toreturn = struct.temporal + '['+ str(objetonum) + ']' 
                    variables = struct.valor
                    tipotoreturn = 'void'
                    if isinstance(operacion.exp, Acceso):
                        name = operacion.exp.id
                        toreturn += "['" + name + "']"
                        for x in operacion.exp.lista:
                            posicion = self.InterpretarOperacion(x, tabla, tree + '2')
                            postipo = posicion[0]
                            toreturn += '[' + str(posicion[1]) + ']' 
                    elif isinstance(operacion.exp, OpId):
                        name = operacion.exp.id
                        toreturn += "['" + name + "']"
                    else:
                        self.errorSemantico('INVALID_INSTRUCTION', operacion.linea, 'No se puede accesar al struc de esta forma')    
                    return(tipotoreturn,toreturn)
                else:
                    self.errorSemantico('UNDEFINED_STRUCT', operacion.linea, 'El struct no existe')
            else:
                self.errorSemantico('UNDEFINED_VARIABLE', operacion.linea, 'La variable no existe')
        elif isinstance(operacion, Scanf):
            #---------AST
            numnodo = str(self.inc())
            tree = numnodo + 'p'
            self.dot.node(tree,'Scanf')
            self.dot.edge(padre,tree)
            #---------AST
            return('void','read()')
        else:
            self.errorSemantico('OPERATION_ERROR',operacion.linea,'No se pudo hacer ninguna operacion')

    #METODO PARA ARMAR EL RESULTADO
    def concatenar(self,cadena):
        self.resultado = self.resultado + cadena + '\n'

    #METODO PARA CREAR UN NUEVO TEMPORAL
    def newTemp(self):
        new = '$t' +str(self.temp)
        self.temp += 1
        return new

    #METODO PARA CREAR UN NUEVO PARAMETRO
    def newParam(self):
        new = '$a' +str(self.param)
        self.param += 1
        return new

    #METODO PARA DEVOLVER UN NUMERO JUNTO A UNA ETIQUETA
    def newTag(self,texto):
        new = texto + str(self.numtag)
        self.numtag += 1
        return new 

#-------------------------------------------------------------------------------------------------

    #METODO PARA AVANZAR EN EL DEBUG
    def SiguientePaso(self):
        pass

    #METODO PARA CAMBIAR EL COLOR DEL TEMA DEL EDITOR
    def ColorTema(self):
        if (self.tema == 1):
            self.textarea.numeros_linea.config(bg='slate gray')
            self.principal.config(bg='slate gray')
            self.textarea.config(bg='slate gray')
            self.textarea.cuadro.config(bg='dim gray',foreground='snow',insertbackground='white')
            self.consola.config(bg='black',fg='yellow green', insertbackground='yellow green')
            self.tema = 0
        else:
            self.textarea.numeros_linea.config(bg='light grey')
            self.principal.config(bg='light grey')
            self.textarea.config(bg='light grey')
            self.textarea.cuadro.config(bg='white',foreground='black',insertbackground='black')
            self.consola.config(bg='dark khaki',fg='black', insertbackground='black')
            self.tema = 1

    #METODO PARA QUITAR LOS NUMEROS DE LINEA DEL EDITOR
    def QuitarNums(self):
        if (self.numeros == 1):
            self.textarea.numeros_linea.config(width=0)
            self.numeros = 0
        else:
            self.textarea.numeros_linea.config(width=20)
            self.numeros = 1

    #METODO PARA HACER EL REPORTE GRAMATICAL
    def RepGramatical(self):
        f = open('ReporteGr.html', "a")
        tshtml = '''<html>
        <head>
        <style>
        table {
        width:100%;
        }
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        }
        th, td {
        padding: 15px;
        text-align: left;
        }
        table#t01 tr:nth-child(even) {
        background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
        background-color: #fff;
        }
        table#t01 th {
        background-color: green;
        color: white;
        }
        </style>
        </head>
        <body>
        <h2>Reporte Gramatical</h2>
        <table id="t01">
        <tr>
        <th>Produccion</th>
        <th>Regla semantica</th> 
        </tr>'''
        f.write(tshtml)
        for k, v in (self.tablagramatical.producciones.items()):
            proc = self.tablagramatical.getProduccion(k)
            tshtml3 = '<tr><td>' + proc.produccion + '</td><td>' + proc.reglas + '</td></tr>\n'
            f.write(tshtml3)        
        
        tshtml2 = '</table>\n</body>\n</html>'
        f.write(tshtml2)
        f.close()
        os.system('start '+os.path.realpath('ReporteGr.html'))

    #METODO PARA HACER EL REPORTE DE ERRORES
    def ReporteErrores(self):
        contador = 1
        tshtml = '''<html>
        <head>
        <style>
        table {
        width:100%;
        }
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        }
        th, td {
        padding: 15px;
        text-align: left;
        }
        table#t01 tr:nth-child(even) {
        background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
        background-color: #fff;
        }
        table#t01 th {
        background-color: red;
        color: white;
        }
        </style>
        </head>
        <body>
        <h2>Tabla de Errores</h2>
        <table id="t01">
        <tr>
        <th>Numero</th>
        <th>Tipo</th> 
        <th>Descripcion</th>
        <th>Linea</th>
        <th>Posicion </th>
        </tr>
         '''
        for x in self.tablaErrores.errores: 
            error = self.tablaErrores.getError(x)
            num = str(contador)
            tipo = str(error.tipo)
            desc = str(error.desc)
            linea = str(error.linea)
            pos = str(error.pos)
            tshtml += '<tr><td>' + num + '</td><td>' + tipo + '</td><td>'+ desc  +'</td><td>' + linea + '</td><td>'+ pos +'</td></tr>\n'
            contador = contador + 1
        tshtml += '</table>\n</body>\n</html>'
        f = open('ReporteEr.html', "w")
        f.write(tshtml)
        f.close()

    #METODO PARA CREAR EL REPORTE DE LA TABLA DE SIMBOLOS
    def ReporteTablaSimbolos(self):
        tshtml = '''<html>
        <head>
        <style>
        table {
        width:100%;
        }
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        }
        th, td {
        padding: 15px;
        text-align: left;
        }
        table#t01 tr:nth-child(even) {
        background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
        background-color: #fff;
        }
        table#t01 th {
        background-color: black;
        color: white;
        }
        </style>
        </head>
        <body>
        <h2>Tabla de simbolos</h2>
        <table id="t01">
        <tr>
        <th>Id</th>
        <th>Nombre</th>
        <th>Temporal</th>
        <th>Valor</th> 
        <th>Tipo</th>
        <th>Dimension</th>
        <th>Declarada en </th>
        <th>Referencia</th>
        </tr>
         '''
        for x in self.tablaGlobal.simbolos: 
            val = self.tablaGlobal.getSimbolo(x)
            ide = str(x)
            nombre = str(val.nombre)
            valo = str(val.valor)
            temp = str(val.temporal)
            ambit = str(val.ambito)
            tipo = str(val.tipo)
            dim = str(val.dimension)
            dire = str(val.referencia)
            tshtml += '<tr><td>' + ide + '</td>'+'<td>' + nombre + '</td>'+'<td>' + temp + '</td>'+'<td>' + valo + '</td><td>'+ tipo  +'</td><td>'+dim+'</td><td>'+ambit +'</td><td>'+dire+'</td></tr>\n'
        tshtml += '</table>\n</body>\n</html>'
        f = open('ReporteTS.html', "w")
        f.write(tshtml)
        f.close()

    #METODO PARA CREAR EL REPORTE DE OPTIMIZACION
    def ReporteOptimizacion(self):
        tshtml = '''<html>
        <head>
        <style>
        table {
        width:100%;
        }
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        }
        th, td {
        padding: 15px;
        text-align: left;
        }
        table#t01 tr:nth-child(even) {
        background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
        background-color: #fff;
        }
        table#t01 th {
        background-color: orange;
        color: white;
        }
        </style>
        </head>
        <body>
        <h2>Reporte de Optimizacion</h2>'''
        tshtml += '<h3>Numero de bloques:  '+str(self.numbloques)+'</h3>'
        tshtml += '<h3>Numero de lineas antes de optimizar:  '+str(self.totallineas)+'</h3>'
        tshtml += '<h3>Numero de lineas despues de optimizar:  '+str(self.lineasdespues)+'</h3>'
        if(self.lineasdespues != 0):
            tshtml += '<h3>Lineas ahorradas:  '+str(self.totallineas - self.lineasdespues)+'</h3>'
        tshtml += '''<table id="t01">
        <tr>
        <th>Id</th>
        <th>Nombre</th>
        <th>Descripcion</th>
        <th>Regla</th>
        <th>Linea</th>
        </tr>
         '''
        conop = 1
        for k, v in (self.tablaoptimizacion.optimizaciones.items()):
            opti = self.tablaoptimizacion.getOptimizacion(k)
            tshtml += '<tr><td>' + str(conop) + '</td><td>' + opti.optimizacion + '</td><td>' + opti.desc + '</td><td>' + str(opti.regla) + '</td><td>' + str(opti.linea) + '</td></tr>\n'
            conop += 1

        tshtml += '</table>\n</body>\n</html>'
        f = open('ReporteOp.html', "w")
        f.write(tshtml)
        f.close()

    #METODO PARA VER LA TABLA DE SIMBOLOS
    def VerTablaSimbolos(self):
        os.system('start '+os.path.realpath('ReporteTs.html'))
        
    #METODO PARA HACER EL REPORTE DE OPTIMIZACION
    def VerOptimizacion(self):
        os.system('start '+os.path.realpath('ReporteOp.html'))

    #METODO PARA VER EL REPORTE DE ERRORES
    def VerReporteErrores(self):
        os.system('start '+os.path.realpath('ReporteEr.html'))

    #METODO PARA DETENER EL DEBUG
    def stop(self):
        pass

    #METODO PARA AGREGAR UN ERROR SEMANTICO
    def errorSemantico(self,descripcion,info1,info2):
        nuevo = errores.Error('SEMANTICO',descripcion,info1,info2)
        self.tablaErrores.newError(nuevo)

    #METODO PARA AGREGAR UN REGISTRO DE OPTIMIZACION
    def addOpti(self, num, desc, linea, regla):
        tipo = ''
        if(num == 1):
            tipo = "MIRILLA"
        else:
            tipo = "BLOQUE"
        opti = optimizacion.Optimizacion(tipo,desc,str(regla),linea)
        self.tablaoptimizacion.newOptimizacion(opti)
    
    #METODO PARA VER EL AST
    def VerAST(self):
        self.dot.render('Ast',view=True)

    #METODO PARA ASIGNAR UN NUEVO ID A CADA SIMBOLO
    def getId(self):
        num = self.numvar
        self.numvar += 1
        return num

    #METODO PARA OPTIMIZAR
    def OptimizarCodigo(self):
        self.numbloques = 1
        numlineas = len(self.listaAugus)
        eliminar = []
        operaciones = []
        asignaciones = []
        for x in range(0,numlineas):
            tupla = self.listaAugus[x]
            if(len(tupla) != 0):
                tipo = tupla[0]
                numsig = x+1
                if(numsig < numlineas):
                    siguiente = self.listaAugus[numsig]
                    if(len(siguiente) != 0):
                        tiponext = siguiente[0]
            if(tipo == 'asignacion'):
                n = tupla[1]
                val = tupla[3]
                asig = ((n,val))
                #if('$t' in val):
                if(' ' in val):
                    newop = val.split(' ')
                    newtupla = ('operacion',n,' = ',newop[0],' ' + newop[1] + ' ',newop[2],';')
                    self.listaAugus[x] = newtupla
                    self.listaAugus[x] = newtupla
            if(tipo == 'operacion'):
                n = tupla[1]
                o1 = tupla[3]
                s = tupla[4]
                o2 = tupla[5]
                operacion = (n,o1,s,o2)
                if(s == ' / '):
                    if(o2 == '1'):
                        if(o1 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (/1)",'A'+str(x),11)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (/1)",'A'+str(x),15)
                            newtupla = ('asignacion',n,' = ',o1,';')
                            self.listaAugus[x] = newtupla
                    if(o1 == '0'):
                        self.addOpti(1,"Simplificacion algebraica y por fuerza: (0/)",'A'+str(x),18)
                        newtupla = ('asignacion',n,' = ','0',';')
                        self.listaAugus[x] = newtupla
                elif(s == ' * ' ):
                    if(o1 == '1'):
                        if(o2 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (*1)",'A'+str(x),10)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (*1)",'A'+str(x),14)
                            newtupla = ('asignacion',n,' = ',o2,';')
                            self.listaAugus[x] = newtupla
                    if(o2 == '1'):
                        if(o1 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (*1)",'A'+str(x),10)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (*1)",'A'+str(x),14)
                            newtupla = ('asignacion',n,' = ',o1,';')
                            self.listaAugus[x] = newtupla
                    if(o1 == '0' or o2 == '0'):
                        self.addOpti(1,"Simplificacion algebraica y por fuerza: (*0)",'A'+str(x),17)
                        newtupla = ('asignacion',n,' = ','0',';')
                        self.listaAugus[x] = newtupla
                    if(o1 == '2'):
                        self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ en lugar de *)",'A'+str(x),16)
                        newtupla = ('operacion',n,' = ',o2,' + ',o2,';')
                        self.listaAugus[x] = newtupla
                    if(o2 == '2'):
                        self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ en lugar de *)",'A'+str(x),16)
                        newtupla = ('operacion',n,' = ',o1,' + ',o1,';')
                        self.listaAugus[x] = newtupla
                elif(s == ' + '):
                    if(o1 == '0'):
                        if(o2 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ 0)",'A'+str(x),8)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ 0)",'A'+str(x),12)
                            newtupla = ('asignacion',n,' = ',o2,';')
                            self.listaAugus[x] = newtupla
                    if(o2 == '0'):
                        if(o1 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ 0)",'A'+str(x),8)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (+ 0)",'A'+str(x),12)
                            newtupla = ('asignacion',n,' = ',o1,';')
                            self.listaAugus[x] = newtupla
                elif(s ==' - '):
                    if(o2 == '0'):
                        if(o1 == n):
                            eliminar.append(x)
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (- 0)",'A'+str(x),9)
                        else:
                            self.addOpti(1,"Simplificacion algebraica y por fuerza: (- 0)",'A'+str(x),13)
                            newtupla = ('asignacion',n,' = ',o1,';')
                            self.listaAugus[x] = newtupla
                operaciones.append(operacion)
                for op in operaciones:
                    if(op != operacion):
                        if(op[1] == operacion[1] and op[2] == operacion[2] and op[3] == operacion[3]):
                            if('$a' in operacion[1] or ('$v' in operacion[1]) or ('$s' in operacion[1])):
                                pass
                            else:
                                newtupla = ('asignacion',n,' = ',op[0],';')
                                self.listaAugus[x] = newtupla
                                self.addOpti(2,"Subexpresion Comun",'A'+str(x),21)
            if(tipo == 'salto'):
                self.numbloques += 1
                if(tiponext != 'etiqueta'):
                    eliminar.append(numsig)
                    self.addOpti(2,"Codigo muerto: El codigo despues de un salto incondicional nunca se ejecuta",'A'+str(numsig),20)
                else:
                    n = tupla[2]
                    ntag = siguiente[1].replace(":",'')
                    if(n == ntag):
                        eliminar.append(x)
                        self.addOpti(1,"Codigo inalcanzable: La etiqueta del salto esta justo despues",'A'+str(x),2)

        while eliminar:
            num = eliminar[0]
            self.listaAugus[num] = ()
            eliminar.pop(0)
        

    def codigoOptimizado(self):
        for x in self.listaAugus:
            for y in range(1,len(x)):
                self.resultadook += x[y]
            if(len(x)!=0):
                self.resultadook += '\n'

    #METODO PARA EJECUTAR EL ANALISIS ASCENDENTE DE AUGUS EN EL INTERPRETE DE AUGUS
    def EjecutarAugus(self, texto):
        global ts_debug, no_instruccion, waitForCommand, ejecucion_automatica
        ejecucion_automatica = 1
        waitForCommand = 0
        Inter.limpiarValores()
        Inter.inicializarEjecucionAscendente(texto, self.consola)
        Inter.inicializarTS()
        i = 0
        while i < len(Inter.instrucciones):
            if waitForCommand == 0 or waitForCommand == 2: #0=Sin Entrada, 1=Esperando, 2=Comando Ingresado
                if i < len(Inter.instrucciones) :
                    is_asig = Inter.instrucciones[i]
                    if isinstance(is_asig,Asignacion): 
                        # COMANDO PARA LEER DE CONSOLA
                        if isinstance(is_asig.valor,Read) and waitForCommand == 0:
                            waitForCommand = 1
                            no_instruccion = i
                            return None
                    #EJECUTAR INSTRUCCION
                    instr_temp = Inter.ejecutarInstruccionUnitaria(1,i)
                    if instr_temp is not None:
                        if instr_temp == -10 : # EXIT
                            i = len(Inter.instrucciones)
                        else: #GOTO
                            i = instr_temp
                    waitForCommand = 0
                else:
                    messagebox.showinfo("Finalizado","Ultima instruccion ejecutada.")
            i = i + 1

    def comando_ingresado(self,event):
        global waitForCommand
        waitForCommand=2
        if ejecucion_automatica == 1:
            self.continuar_ejecucionAsc()

    def continuar_ejecucionAsc(self):
        global no_instruccion, waitForCommand
        while no_instruccion<len(Inter.instrucciones):
            if waitForCommand == 0 or waitForCommand == 2: #0=Sin Entrada, 1=Esperando, 2=Comando Ingresado
                if no_instruccion<len(Inter.instrucciones) :
                    is_asig=Inter.instrucciones[no_instruccion]
                    if isinstance(is_asig,Asignacion): 
                        # COMANDO PARA LEER DE CONSOLA
                        if isinstance(is_asig.valor,Read) and waitForCommand == 0:
                            waitForCommand=1
                            #no_instruccion=i
                            return None
                    #EJECUTAR INSTRUCCION
                    instr_temp=Inter.ejecutarInstruccionUnitaria(1,no_instruccion)
                    if instr_temp is not None:
                        if instr_temp==-10 : # EXIT
                            no_instruccion=len(Inter.instrucciones)
                        else: #GOTO
                            no_instruccion=instr_temp
                    waitForCommand=0
                    no_instruccion+=1
                else:
                    messagebox.showinfo("Finalizado","Ultima instruccion ejecutada.")

    #METODO PARA LIMPIAR LAS TABLAS Y VARIABLES
    def reset(self):
        self.resultado = ''
        self.temp = 0
        self.param = 0
        self.numvar = 0
        self.numtag = 0
        self.numfunc = 0
        self.tablaGlobal.simbolos.clear()
        self.tablaErrores.errores.clear()
        self.tablagramatical.producciones.clear()
        self.tablaoptimizacion.optimizaciones.clear()
        self.stack.clear()
        self.stackLoop.clear()
        self.stackContinue.clear()
        self.returns.clear()
        self.ismain = True
        self.arbol = None
        self.i = 0
        self.resultadook = ''
        self.dot = None
        self.listaAugus.clear()
        self.numbloques = 1
        self.lineasantes = -1
        self.lineasdespues = 0
        self.totallineas = 0
        try:
            f = open('ReporteGr.html', "w")
            f.write('')
            f.close()
        except:
            messagebox.showinfo("Error","No se pudo abrir el archivo del reporte gramatical")

#--------------------------------------LOOP PARA MANTENAR LA EJECUCION DEL PROGRAMA
if __name__ == "__main__":
    principal = gui.Tk()
    principal.state("zoomed")
    contenido = Editor(principal)
    principal.mainloop()