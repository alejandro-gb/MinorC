#---------------------------------------IMPORTS
import tkinter as gui
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage, simpledialog
from tkinter.ttk import *
from graphviz import Digraph
import analizar
import tablaSimbolos
import errores
from instrucciones import *

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
        ejecutar.add_command(label="Interpretar", command=parent.AnalisisAsc)
        ejecutar.add_separator()
        ejecutar.add_command(label="Reporte de Errores", command=parent.VerReporteErrores)
        ejecutar.add_command(label="Tabla de simbolos", command=parent.VerTablaSimbolos)
        ejecutar.add_command(label="Reporte del AST", command=parent.VerAST)
        ejecutar.add_command(label="Reporte gramatical", command=parent.RepGramatical)

        #lista de opciones de opciones
        opciones.add_command(label="Cambiar Tema", command=parent.ColorTema)
        opciones.add_command(label="Numeros de linea", command=parent.QuitarNums)

        #lista de opciones de debugin
        debugin.add_command(label="Run debug", command= parent.SiguientePaso)
        debugin.add_command(label="Next step", command= lambda: parent.test.set(1))
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
        fuente = ("Arial",14)
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
    temp = 0
    param = 0
    numtag = 0
    numvar = 0
    numfunc = 0
    ismain = True
    iscall = False
    stack = []
    stackLoop = []
    stackContinue = []
    returns = []
    namerecursive = ''
    isrecursive = False
    

    #CONSTRUCTOR
    def __init__(self,principal):
        principal.title("Sin titulo - MinorC")
        principal.geometry("600x500")
        fuente = ("Arial",13)
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

    #METODO PARA HACER EL ANALISIS ASCENDENTE
    def AnalisisAsc(self):
        self.reset()
        self.consola.delete('1.0',gui.END)
        self.texto = str(self.textarea.cuadro.get('1.0',gui.END))
        self.instrucciones = analizar.parse(self.texto)
        self.Interpretar(self.instrucciones, self.tablaGlobal)
        self.ReporteTablaSimbolos()
        self.ReporteErrores()
        self.consola.insert(gui.END,self.resultado)
        if(len(self.tablaErrores.errores) != 0):
            self.VerReporteErrores()

    #METODO PARA INTERPRETAR LAS INSTRUCCIONES
    def Interpretar(self, instrucciones, tabla):
        #try:

            self.stack.append('global')
            #BUSCAR INSTRUCCIONES GLOBALES
            for x in instrucciones:
                if   isinstance(x,Declaracion) : self.InterpretarDeclaracion(x, tabla, 'global')
                elif isinstance(x,Printf) : self.InterpretarPrintf(x,tabla)
                elif isinstance(x,Arreglo) : self.InterpretarArreglo(x,tabla,'global')
                elif isinstance(x,Asignacion) : self.InterpretarAsignacion(x,tabla)
                elif isinstance(x,Etiqueta) : self.InterpretarEtiqueta(x,tabla,'global')
                elif isinstance(x,Goto) : self.InterpretarGoto(x,tabla,'global')
            
            #BUSCAR EL MAIN
            for x in instrucciones:
                if isinstance(x,Funcion):
                    if (x.nombre == 'main'):
                        self.InterpretarMain(x, tabla)
                        instrucciones.remove(x)
            
            #BUSCAR LAS DEMAS FUNCIONES
            for x in instrucciones:
                if isinstance(x,Funcion) :  
                    self.concatenar('')
                    self.InterpretarFuncion(x, tabla)
            
            if self.returns:
                self.concatenar('regresos:')
                for r in self.returns:
                    self.concatenar('if($ra=='+str(r)+') goto ra'+str(r)+';')
                
        #except:
        #    messagebox.showerror('ERROR','NO SE INTERPRETO')

    #METODO PARA INTERPRETAR INSTRUCCIONES INTERNAS
    def InterpretarIns(self, lista, tabla, nombre):
        for x in lista:
            if   isinstance(x,Declaracion)  : self.InterpretarDeclaracion(x, tabla, nombre)
            elif isinstance(x,Printf)       : self.InterpretarPrintf(x,tabla)
            elif isinstance(x,Arreglo)      : self.InterpretarArreglo(x,tabla,nombre)
            elif isinstance(x,Asignacion)   : self.InterpretarAsignacion(x,tabla)
            elif isinstance(x,While)        : self.InterpretarWhile(x,tabla,nombre)
            elif isinstance(x,Dowhile)      : self.InterpretarDowhile(x,tabla,nombre)
            elif isinstance(x,Etiqueta)     : self.InterpretarEtiqueta(x,tabla,nombre)
            elif isinstance(x,Goto)         : self.InterpretarGoto(x,tabla,nombre)
            elif isinstance(x,If)           : self.InterpretarIf(x,tabla,nombre)
            elif isinstance(x,Switch)       : self.InterpretarSwitch(x,tabla,nombre)
            elif isinstance(x,Return)       : self.InterpretarReturn(x,tabla)
            elif isinstance(x,Break)        : self.InterpretarBreak(x,tabla)
            elif isinstance(x,Continue)     : self.InterpretarContinue(x,tabla)
            elif isinstance(x,Operacion)    : self.InterpretarOperacion(x,tabla)
            elif isinstance(x,For)          : self.InterpretarFor(x,tabla,nombre)
            elif isinstance(x,Funcion)      : self.errorSemantico('CORE_DUMPED',x.linea,'No se pueden hacer funciones anidadas')
            
    #METODO PARA INTERPRETAR UNA FUNCION
    def InterpretarFuncion(self, funcion, tabla):
        tipo    = funcion.tipo
        nombre  = funcion.nombre
        params  = funcion.listaparam
        ins     = funcion.lista

        num = self.getId()
        simbolo = tablaSimbolos.Simbolo(num, nombre, '', tipo, 'Funcion', 'global')
        tabla.newSimbolo(simbolo)
        self.stack.append(nombre)
        self.concatenar(nombre + ':')
        self.namerecursive = nombre
        nump = 0
        for param in params:
            nums = self.getId()
            temporal = self.newTemp()
            val = '$a'+str(nump)
            simbolo = tablaSimbolos.Simbolo(nums, param[1], temporal, param[0], val, nombre)
            tabla.newSimbolo(simbolo)
            self.concatenar(temporal + ' = ' + str(val) + ';')
            nump +=1;
        
        self.InterpretarIns(ins,tabla,nombre)
        self.stack.pop()
        self.iscall = False

    #METODO PARA INTERPRETAR UNA FUNCION
    def InterpretarMain(self, funcion, tabla):
        ins = funcion.lista
        num = self.getId()
        simbolo = tablaSimbolos.Simbolo(num, 'main', '', 'int', 'Funcion', 'global')
        tabla.newSimbolo(simbolo)
        self.stack.append('main')
        self.concatenar('main:')
        self.InterpretarIns(ins,tabla,'main')
        self.concatenar('exit;')
        self.stack.pop()
        self.ismain = False
        self.iscall = False

    #METODO PARA INTERPRETAR UNA ETIQUETA
    def InterpretarEtiqueta(self,ins,tabla,ambito):
        nomTag = ins.nombre
        self.concatenar(nomTag + ':')

    #METODO PARA INTERPRETAR UN SALTO GOTO
    def InterpretarGoto(self,ins,tabla,ambito):
        nomTag = ins.nombre
        self.concatenar('goto '+nomTag + ';')

    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarReturn(self, ret, tabla):
        if(self.ismain == False):
            tempstack = self.returns.copy()
            exp = self.InterpretarOperacion(ret.expresion,tabla)
            exptipo = exp[0]
            expval = str(exp[1])
            self.concatenar('$v0 = ' + expval +';') 
            if self.iscall:
                self.concatenar('$ra = $ra - 1;')
            self.iscall = False
            self.concatenar('goto regresos;')

    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarBreak(self,ret,tabla):
        fin = self.stackLoop[-1]
        self.concatenar('goto ' + fin + ';')

    #METODOD PARA INTERPRETAR UN RETURN
    def InterpretarContinue(self,ret,tabla):
        inicio = self.stackContinue[-1]
        self.concatenar('goto ' + inicio + ';')

    #METODO PARA INTERPRETAR UN FOR
    def InterpretarFor(self, ciclo, tabla, ambito):
        inicio = ciclo.inicial
        condicion = ciclo.condicion
        cambio = ciclo.cambio
        lista = ciclo.ins

        nombre = self.newTag('for') #ETIQUETA INICIO
        verdadero = nombre + 'V'    #ETIQUETA VERDADERA
        falso = nombre + 'F'        #ETIQUETA FALSA
        actualizar = nombre + 'A'   #ETIQUETA ACTUALIZAR
        
        self.stack.append(nombre)
        self.stackLoop.append(falso)
        self.stackContinue.append(actualizar)

        if isinstance(inicio, Declaracion):
            self.InterpretarDeclaracion(inicio,tabla,nombre)
        elif isinstance(inicio, Asignacion):
            self.InterpretarAsignacion(inicio,tabla)
        self.concatenar(nombre + ':')
        resultado = self.InterpretarOperacion(condicion,tabla)
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + verdadero + ';')
        self.concatenar('goto ' + falso + ';')
        self.concatenar(actualizar + ':')
        self.InterpretarOperacion(cambio,tabla)
        self.concatenar('goto '+ nombre +';')
        self.concatenar(verdadero +':')
        self.InterpretarIns(lista, tabla, nombre)
        self.concatenar('goto '+ actualizar +';')        
        self.concatenar(falso +':')
        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()
        
    #METODO PARA INTERPRETAR UN IF
    def InterpretarIf(self, ciclo, tabla, ambito):
        condicion = ciclo.condicion
        listaif = ciclo.listaif
        listaelse = ciclo.listaelse
        nombre = self.newTag('if')
        verdadero = nombre + 'V'
        falso = nombre + 'F'
        fin = nombre +'end'
        sielse = False

        self.stack.append(nombre)

        resultado = self.InterpretarOperacion(condicion,tabla)
        cond = resultado[1]
        self.concatenar('if(' + cond + ') goto ' + verdadero + ';')
        self.concatenar('goto ' + falso + ';')
        self.concatenar(verdadero + ':')
        self.InterpretarIns(listaif,tabla,nombre)
        if(listaelse is not None):
            for x in listaelse:
                if(type(x) is tuple):
                    condicionx = x[0]
                    listax = x[1]
                    self.concatenar('goto ' + fin + ';')
                    nombrex = self.newTag('elseif')
                    verdaderox = nombrex + 'V'
                    falsox = nombrex + 'F'
                    self.concatenar(falso + ':')
                    falso = falsox
                    resultadox = self.InterpretarOperacion(condicionx,tabla)
                    condx = resultadox[1]
                    self.concatenar('if(' + condx + ') goto ' + verdaderox + ';')
                    self.concatenar('goto ' + falso + ';')
                    self.concatenar(verdaderox + ':')
                    self.InterpretarIns(listax, tabla, nombre)
                    self.concatenar('goto ' + fin + ';')
                else:
                    sielse = True
                    if(len(listaelse) == 1):
                        self.concatenar('goto ' + fin + ';')
                    self.concatenar(falso + ':')
                    self.InterpretarIns(x,tabla,nombre)
                    self.concatenar(fin + ':')
        
        if(sielse == False):
            self.concatenar(falso + ':')

        self.stack.pop()

    #METODO PARA INTERPRETAR LOS SWITCHS
    def InterpretarSwitch(self, ciclo, tabla, ambito):
        exp = self.InterpretarOperacion(ciclo.expresion,tabla)
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
                aevaluar =self.InterpretarOperacion(caso[0],tabla)
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
                    scontador += 1
                    self.concatenar('if(' + expval + ' != ' + resvalor + ') goto ' + namecase + ';')
                    self.InterpretarIns(cuerpo,tabla,tag)
                    #if conbreak:
                    #    self.concatenar('goto ' + fin + ';')
                else:
                    self.errorSemantico('TYPE_ERROR',ciclo.linea,'El tipo a evaluar debe ser igual que evaluado')
            #DEFAULT
            else:
                haydef = True
                tagdef = tag + str(scontador-1)
                self.concatenar(tagdef + ':')
                self.InterpretarIns(caso,tabla,tag)
        if not haydef:
            self.concatenar(tag+str(scontador-1)+':')
        self.concatenar(fin + ':')
        
        self.stack.pop()
        self.stackLoop.pop()

    #METODO PARA INTERPRETAR UN DOWHILE
    def InterpretarDowhile(self,ciclo,tabla,ambito):
        condicion = ciclo.condicion
        ins = ciclo.lista
        
        regreso = self.newTag('dowhile')
        falso = regreso + 'F'
        
        self.stack.append(regreso)
        self.stackLoop.append(falso)
        self.stackContinue.append(regreso)

        self.concatenar(regreso + ':')
        self.InterpretarIns(ins,tabla,regreso)
        resultado = self.InterpretarOperacion(condicion,tabla)
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + regreso + ';')
        self.concatenar(falso + ':')
        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()

    #METODO PARA INTERPRETAR UN WHILE
    def InterpretarWhile(self,ciclo,tabla,ambito):
        condicion = ciclo.condicion
        ins = ciclo.lista
        
        regreso = self.newTag('while')  #ETIQUETA INICIO
        verdadero = regreso + 'V'       #ETIQUETA VERDADERA
        falso = regreso + 'F'           #ETIQUETA FALSA
        
        self.stack.append(regreso)
        self.stackLoop.append(falso)
        self.stackContinue.append(regreso)

        self.concatenar(regreso+':')
        resultado = self.InterpretarOperacion(condicion,tabla)
        cond = resultado[1]
        self.concatenar('if(' + cond + ')' + ' goto ' + verdadero + ';')
        self.concatenar('goto ' + falso + ';')
        self.concatenar(verdadero + ':')
        self.InterpretarIns(ins,tabla,regreso)
        self.concatenar('goto ' + regreso + ';')
        self.concatenar(falso + ':')
        
        self.stack.pop()
        self.stackLoop.pop()
        self.stackContinue.pop()
    
    #METODO PARA INTERPRETAR UN PRINTF
    def InterpretarPrintf(self,ins,tabla):
        lista = ins.listavalores
        forma = self.InterpretarOperacion(lista[0],tabla)
        newtipo = forma[0]
        newval = forma[1]
        toconcat = ''
        if(newtipo != 'char'):
            self.errorSemantico('FORMAT_ERROR',ins.linea,'Se debe definir el formato de lo que se imprime')
            return
        try:
            for i in range(1,len(lista)):
                resultado = self.InterpretarOperacion(lista[i],tabla)
                restipo = resultado[0]
                resval = resultado[1]
                tprint = 'print(' + str(resval) + ');'
                if(restipo == 'int' and ('%d' in newval or '%i' in newval)):
                    if('%d' in newval):
                        newval = newval.replace('%d','',1)
                    elif('%i' in newval):
                        newval = newval.replace('%i','',1)
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                elif((restipo == 'float' or restipo =='double') and '%f' in newval):
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%f','',1)
                elif(restipo == 'char' and '%c' in newval):
                    if('$' in str(resval)):
                        tprint = "print(" + str(resval) + ");"
                    else:
                        tprint = "print('" + str(resval) + "');"
                    toconcat += tprint + '\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%c','',1)
                elif(restipo == 'char*' and '%s' in newval):
                    toconcat += tprint+'\n'
                    toconcat += 'print("\\n");'+'\n'
                    newval = newval.replace('%s','',1)
                else:
                    self.errorSemantico('FORMAT_ERROR',ins.linea,'El formato para imprimir no concuerda con el tipo de la variable')
            tprint = 'print(\'' + str(newval) + '\');'
            if(str(newval) != ''):
                self.concatenar(tprint)
                self.concatenar('print("\\n");')
            if(toconcat != ''):
                self.concatenar(toconcat)
        except IndexError:
            self.errorSemantico('INDEX_ERROR',ins.linea,'Se intenta imprimir fuera de rango')
        except:
            self.errorSemantico('NONETYPE_ERROR',ins.linea,'Se intenta imprimir un valor que no existe')
     
    #METODO PARA INTERPRETAR UNA DECLARACION
    def InterpretarDeclaracion(self, ins, tabla, ambito):
        tipo = ins.tipo.lower()
        valor = ''

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
                        simbolo = tablaSimbolos.Simbolo(num, nombre, temporal, tipo, valor, ambito)
                        tabla.newSimbolo(simbolo)
                        self.concatenar(temporal + ' = ' + str(valor) + ';')
                    #IDENTIFICADOR VALOR
                    elif(type(nombre) is tuple):
                        identificador = nombre[0]
                        val = self.InterpretarOperacion(nombre[1], tabla, temporal)
                        newtipo = val[0]
                        valor = val[1]
                        if(self.VerificarTipo(newtipo, tipo)):#VERIFICAR TIPO
                            if(newtipo == 'char'):
                                if(len(valor) == 1):
                                    valor = "'" + valor + "'"
                                    simbolo = tablaSimbolos.Simbolo(num, identificador, temporal, tipo, valor, ambito)
                                    tabla.newSimbolo(simbolo)
                                    self.concatenar(temporal + ' = ' + str(valor) + ';')
                                    return
                                else:
                                    self.errorSemantico('TYPE_ERROR',ins.linea,'Un caracter nada mas')
                                    return
                            simbolo = tablaSimbolos.Simbolo(num, identificador, temporal, tipo, valor, ambito)
                            tabla.newSimbolo(simbolo)
                            if(type(valor) is not bool):
                                self.concatenar(temporal + ' = ' + str(valor) + ';')
                        else:
                            self.errorSemantico('TYPE_ERROR',ins.linea,'El tipo debe ser el mismo')
                else:
                    self.errorSemantico('VARIABLE_ERROR',ins.linea,'La variable ya ha sido declarada anteriormente')
            #except:
             #   self.errorSemantico('TYPE_ERROR',ins.linea,'No se pudo asignar el valor (type)')

    #METODO PRA INTERPRETAR UNA ASIGNACION
    def InterpretarAsignacion(self, ins, tabla):
        paravar = ins.paravar
        simbolo = self.BuscarSimbolo(paravar, tabla)
        if(simbolo is not None):
            paratemp = simbolo.temporal
            signo = ins.signo
            exp = self.InterpretarOperacion(ins.valor,tabla,paratemp)
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
                            simbolo.valor = newval
                        elif(signo == '+='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' + ' + str(newval) + ' ; ')
                        elif(signo == '-='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' - ' + str(newval) + ' ; ')
                        elif(signo == '*='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' * ' + str(newval) + ' ; ')
                        elif(signo == '/='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' / ' + str(newval) + ' ; ')
                        elif(signo == '%='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' % ' + str(newval) + ' ; ')
                        elif(signo == '<<='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' << ' + str(newval) + ' ; ')
                        elif(signo == '>>='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' >> ' + str(newval) + ' ; ')
                        elif(signo == '&='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' & ' + str(newval) + ' ; ')
                        elif(signo == '|='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' | ' + str(newval) + ' ; ')
                        elif(signo == '^='):
                            self.concatenar(simbolo.temporal + ' = ' + simbolo.temporal + ' ^ ' + str(newval) + ' ; ')
                            
                else:
                    expre = simbolo.temporal
                    numdim = simbolo.dimension
                    valor = simbolo.valor
                    if(len(numdim) == len(ins.dimensiones)):
                        for x in range(0,len(ins.dimensiones)):
                            posicion = self.InterpretarOperacion(ins.dimensiones[x],tabla)
                            val = posicion[1]
                            #if(val < numdim[x]):
                            expre += '[' + str(val) + ']'
                            try:
                                simbolo.valor[val] = newval
                            except:
                                simbolo.valor.append(newval)
                            #else:
                            #    self.errorSemantico('INDEX_ERROR',ins.linea,'Index out range')
                        expre += ' = ' + str(newval) + ';'
                        self.concatenar(expre)
                    else:
                        self.errorSemantico('INDEX_ERROR',ins.linea,'Index out range (#dimension)')
            else:
                self.errorSemantico('TYPE_ERROR',ins.linea,'El tipo debe ser el mismo')
        else:
            self.errorSemantico('NONE_ERROR',ins.linea,'La variable no ha sido declarada')

    #METODO PARA INTERPRETAR UN ARREGLO
    def InterpretarArreglo(self, ins, tabla, ambito):
        tipo = ins.tipo
        nombre = ins.nombre
        dimensiones = ins.dimensiones
        listaval = ins.listavalores
        valor = []
        if self.VerificarAmbito(nombre,ambito,tabla):
            ide = self.getId()
            temporal = self.newTemp()
            #TIPO ID LISTADIMENSIONES ;
            if(type(dimensiones) is list):
                numdim = len(dimensiones)
                dims = []
                for x in dimensiones:
                    if(type(x) is str):
                        dims.append(None)
                    else:
                        val = self.InterpretarOperacion(x, tabla)
                        newtipo = val[0]
                        newval = val[1]
                        dims.append(newval)
                self.concatenar(temporal + '=' + 'array();')
                if(listaval is not None):
                    if(len(dims) != len(listaval)):
                        self.errorSemantico('INDEX_ERROR',ins.linea,'las dimensiones y la inicializacion debe coincidir')
                        return
                    numerodim = 0
                    for x in listaval:
                        numeroelem = 0
                        for y in x:
                            resultado = self.InterpretarOperacion(y,tabla)
                            restipo = resultado[0]
                            resval = resultado[1]
                            if(dims[numerodim] == None):
                                dims[numerodim] = 100
                            if(numeroelem < dims[numerodim]):
                                if self.VerificarTipo(tipo, restipo):
                                    valor.append(resval)
                                    self.concatenar(temporal+'[' + str(numeroelem) + '] = '+str(resval) + ';')
                                    numeroelem += 1
                                else:
                                    self.errorSemantico('TYPE_ERROR',ins.linea,'Los elementos del arreglo deben ser del mismo tipo')
                            else:
                                self.errorSemantico('INDEX_ERROR',ins.linea,'El numero de elementos es mayor al declarado')
                        numerodim += 1
                for x in range(0,len(dims)):
                    if(dims[x] == 100):
                        dims[x] = None
                simbolo = tablaSimbolos.Simbolo(ide, nombre, temporal, tipo, valor, ambito, dims)
                tabla.newSimbolo(simbolo)
                
            #TIPO ID [] = EXPRESION ;
            else:
                resultado = self.InterpretarOperacion(dimensiones,tabla)
                valor = resultado[1]
                tipo = 'char*'
                simbolo = tablaSimbolos.Simbolo(nombre,temporal,tipo,valor,ambito)
                tabla.newSimbolo(simbolo)
                self.concatenar(temporal + '=' + "'" + valor + "';")
        else:
            self.errorSemantico('VARIABLE_ERROR',ins.linea,'La variable ya ha sido declarada anteriormente')

    #METODO PARA VERIFICAR SI LOS TIPOS SON IGUALES
    def VerificarTipo(self, tipo1, tipo2):
        if(tipo1 == 'int' and tipo2 == 'int'):
            return True
        elif(tipo1 == 'float' and (tipo2 == 'float' or tipo2 == 'double')):
            return True
        elif(tipo1 == 'char' and tipo2 == 'char'):
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
        elif(t1 == 'double' or t2 == 'double'):
            return 'float'
        else:
            return None

    #METODO PARA INTERPRETAR UNA OPERACION 
    def InterpretarOperacion(self, operacion, tabla, var = None):
        if isinstance(operacion, OpNumero):
            tipo = ''
            valor = operacion.valor
            if(type(valor) is int):
                tipo = 'int'
            elif(type(valor) is float):
                tipo = 'float'
            return (tipo,valor)
        elif isinstance(operacion, OpNormal):
            op1 = self.InterpretarOperacion(operacion.op1,tabla)
            tipo1 = op1[0]
            val1 = op1[1]
            
            signo = operacion.signo
            
            op2 = self.InterpretarOperacion(operacion.op2,tabla)
            tipo2 = op2[0]
            val2 = op2[1]
            
            valor1 = str(val1)
            valor2 = str(val2)
            
            if(op1 != None and op2 != None):
                #ARITMETICAS
                if signo == Aritmetica.SUMA:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' + ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' + ' + valor2
                        return (restipo , nval)       
                elif signo == Aritmetica.RESTA:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' - ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' - ' + valor2
                        return (restipo , nval)
                elif signo == Aritmetica.MULTI:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' * ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' * ' + valor2
                        return (restipo , nval)
                elif signo == Aritmetica.DIV:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' / ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' / ' + valor2
                        return (restipo , nval)
                elif signo == Aritmetica.MODULO:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' % ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' % ' + valor2
                        return (restipo , nval)
                    
                #RELACIONALES
                elif signo == Relacional.MAYOR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' > ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' > ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MENOR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' < ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' < ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MAYORIGUAL:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' >= ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' >= ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.MENORIGUAL:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' <= ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' <= ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.EQUIVALENTE:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' == ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' == ' + valor2
                        return (restipo , nval)
                elif signo == Relacional.DIFERENTE:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' != ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' != ' + valor2
                        return (restipo , nval)
                    
                #LOGICOS
                elif signo == Logica.AND:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' && ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' && ' + valor2
                        return (restipo , nval)
                elif signo == Logica.OR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' || ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' || ' + valor2
                        return (restipo , nval)

                #BITS
                elif signo == Bits.BITAND:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' & ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' & ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITOR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' | ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' | ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITXOR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' ^ ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' ^ ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITSHL:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' << ' + valor2 + ';'
                        self.concatenar(temporal)
                        valor1 = temp
                        return (restipo, temp)
                    else:
                        nval = valor1 + ' << ' + valor2
                        return (restipo , nval)
                elif signo == Bits.BITSHR:
                    restipo = self.checkOperacionTipo(tipo1,tipo2)
                    if(restipo is None):
                         self.errorSemantico('TYPE_ERROR',operacion.linea,'No se puede hacer la operacion entre tipos')
                    if(var is None):
                        temp = self.newTemp()
                        temporal = temp + ' = ' + valor1 + ' >> ' + valor2 + ';'
                        self.concatenar(temporal)
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
            return ('char',cadena)
        elif isinstance(operacion, OpId):
            variable = self.BuscarSimbolo(operacion.id,tabla)
            if(variable == None):
                self.errorSemantico('UNDEFINED_VARIABLE',operacion.linea,'La variable no existe')
                return None
            else:
                tipo = variable.tipo
                temporal = variable.temporal
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
                    for x in lista:
                        posicion = self.InterpretarOperacion(x,tabla)
                        postipo = posicion[0]
                        posval = str(posicion[1])
                        strtoreturn += '['+posval+']'
                    return(variable.tipo,strtoreturn)
                else:
                    self.errorSemantico('TYPE_VARIABLE',operacion.linea,'La variable no es arreglo')
                    return None
        elif isinstance(operacion, OpMenos):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval ='-' + str(exp[1])
            return(newtipo,newval)
        elif isinstance(operacion, OpNotbit):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = '~'+str(exp[1])
            return(newtipo,newval)
        elif isinstance(operacion, OpNotlog):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = '!'+str(exp[1])
            return(newtipo,newval)
        elif isinstance(operacion, OpTam):
            restipo = ''
            resval = ''
            if (type(operacion.exp) is str):
                restipo = operacion.exp
            else:
                res = self.InterpretarOperacion(operacion.exp,tabla)
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

            return('int',resval)
        elif isinstance(operacion, OpInc):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = str(exp[1])
            asignar = newval + ' = ' + newval + ' + 1;'
            self.concatenar(asignar)
            if var is not None:    
                newasig = var + ' = ' + newval + ';'
                self.concatenar(newasig)
            return(newtipo , True)
        elif isinstance(operacion, OpDec):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = str(exp[1])
            asignar = newval + ' = ' + newval + ' - 1;'
            self.concatenar(asignar)
            if var is not None:    
                newasig = var + ' = ' + newval + ';'
                self.concatenar(newasig)
            return(newtipo , True)
        elif isinstance(operacion, OpPostInc):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = str(exp[1])
            if var is not None:
                asignar = var + ' = ' + newval + ';'
                self.concatenar(asignar)
            newasig = newval + ' = ' + newval + ' + 1;'
            self.concatenar(newasig)
            return(newtipo , True)
        elif isinstance(operacion, OpPostDec):
            exp = self.InterpretarOperacion(operacion.exp,tabla)
            newtipo = exp[0]
            newval = str(exp[1])
            if var is not None:
                asignar = var + ' = ' + newval + ';'
                self.concatenar(asignar)
            newasig = newval + ' = ' + newval + ' - 1;'
            self.concatenar(newasig)
            return(newtipo, True)
        elif isinstance(operacion, Ternario):
            condicion =self.InterpretarOperacion(operacion.condicion,tabla)
            condval = condicion[1]
            estrue =self.InterpretarOperacion(operacion.verdadero,tabla)
            truetipo = estrue[0]
            trueval = estrue[1]
            esfalse = self.InterpretarOperacion(operacion.falso,tabla)
            falsetipo = esfalse[0]
            falseval = esfalse[1]
            tag = self.newTag('ternario')
            tagV = tag + 'V'
            tagF = tag + 'F'
            tagFin = tag + 'E'
            self.concatenar('if(' + condval + ') goto '+ tagV + ';')
            self.concatenar('goto ' + tagF + ';' )
            self.concatenar(tagV + ':')
            self.concatenar(var + ' = ' + str(trueval) + ';')
            self.concatenar('goto ' + tagFin + ';' )
            self.concatenar(tagF + ':')
            self.concatenar(var + ' = ' + str(falseval) + ';')
            self.concatenar(tagFin + ':')
            return(truetipo,True)
        elif isinstance(operacion, Casteo):
            tipo = operacion.tipo
            if(tipo == 'double'):
                tipo = 'float'
            exp = self.InterpretarOperacion(operacion.expresion,tabla)
            exptipo = exp[0]
            expval = exp[1]
            self.concatenar(expval + ' = (' + tipo + ')' + expval + ';')
            return(tipo,expval)
        elif isinstance(operacion, Llamada):

            self.iscall = True
            self.numfunc += 1
            self.returns.append(self.numfunc)
            self.concatenar('$ra = '+str(self.numfunc)+';')
            id = operacion.id
            if(self.namerecursive == id):
                self.isrecursive = True
                self.iscall = False
            valores = operacion.lista
            contparam = 0
            for valor in valores:
                parametro = self.InterpretarOperacion(valor, tabla)
                tipo = parametro[0]
                val = str(parametro[1])
                par = '$a'+str(contparam)
                self.concatenar(par + ' = ' + val + ';')
                contparam += 1
            
            self.concatenar('goto ' + id +';')
            tempstack = self.returns.copy()
            ra = str(tempstack[-1])
            self.concatenar('ra'+ra+':')
            tempstack.pop()
      
            return('int','$v0')
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
        pass

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

    #METODO PARA VER LA TABLA DE SIMBOLOS
    def VerTablaSimbolos(self):
        os.system('start '+os.path.realpath('ReporteTs.html'))
        
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

    #METODO PARA VER EL AST
    def VerAST(self):
        pass

    #METODO PARA ASIGNAR UN NUEVO ID A CADA SIMBOLO
    def getId(self):
        num = self.numvar
        self.numvar += 1
        return num

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
        analizar.lexer.lineno = 0
        self.stack.clear()
        self.stackLoop.clear()
        self.stackContinue.clear()
        self.returns.clear()
        self.ismain = True
        self.iscall = False

#--------------------------------------loop para mantener la ejecucion del editor
if __name__ == "__main__":
    principal = gui.Tk()
    principal.state("zoomed")
    contenido = Editor(principal)
    principal.mainloop()