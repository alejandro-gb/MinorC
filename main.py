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
        fuente = ("Arial",13)
        self.cuadro = gui.Text(self, selectbackground="light grey", width=120, height=20, font=fuente)
        self.scrollbar = gui.Scrollbar(self, orient=gui.VERTICAL, command=self.cuadro.yview)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.numeros_linea = NumerosLinea(self, width=20, bg='light grey')
        self.numeros_linea.attach(self.cuadro)

        self.scrollbar.pack(side=gui.RIGHT, fill=gui.Y)
        self.numeros_linea.pack(side=gui.LEFT, fill=gui.Y, padx=(5, 0))
        self.cuadro.pack(side=gui.TOP, fill=gui.BOTH, expand=True)

        self.cuadro.tag_configure("dolar", foreground="blue")
        self.cuadro.tag_configure("exit", foreground="red")
        self.cuadro.tag_configure("regs", foreground="firebrick4")
        self.cuadro.tag_configure("reservadas", foreground="steel blue")
        self.cuadro.tag_configure("goto", foreground="purple1")
        self.cuadro.tag_configure("signos", foreground="dark green")
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
        self.resaltarTexto("(break|case|char|signed|const|continue|default|do|double|else|static|float|for|if|int|return|sizeof|extern|switch|void|while)", "reservadas",er=True)
        self.resaltarTexto("(\\+|=|-|\\*|abs|%|!|\\||xor|and|\\^|<|~|\\?|>)", "signos",er=True)
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
    analisis_listo = False
    idcount = 0
    arbol = None
    newvar = None
    debug = False
    dot = None
    tipoanalisis = True
    terminar = False
    temp = 0
    i = 0    
    encontre = 'Global'

    #CONSTRUCTOR
    def __init__(self,principal):
        principal.title("Sin titulo - Augus")
        principal.geometry("1100x700")
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

    #INCREMENTAR EL CONTADOR
    def inc(self):
        self.i += 1
        return self.i

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

    #METODO PARA INTERPRETAR LAS INSTRUCCIONES
    def Interpretar(self, instrucciones, tabla):
        #try:
            #BUSCAR EL MAIN
            for x in instrucciones:
                if isinstance(x,Funcion):
                    if (x.nombre == 'main'):
                        self.InterpretarFuncion(x, tabla)
                        instrucciones.remove(x)
            
            for x in instrucciones:
                if isinstance(x,Asignacion) :
                    self.InterpretarAsignacion(x, tabla, 'global')

            for x in instrucciones:
                if isinstance(x,Funcion) : self.InterpretarFuncion(x, tabla)
        #except:
        #    messagebox.showerror('ERROR','NO SE INTERPRETO')
        
    #METODO PARA INTERPRETAR UNA FUNCION
    def InterpretarFuncion(self, funcion, tabla):
        tipo = funcion.tipo
        nombre = funcion.nombre + ':'
        self.concatenar(nombre)

    #METODO PARA INTERPRETAR UNA ASIGNACION
    def InterpretarAsignacion(self, ins, tabla, ambito):
        tipo = ins.tipo.lower()
        valor = ins.valor
        for nombre in ins.nombres:
            temporal = self.newTemp()
            if(type(nombre) is str):
                if(tipo == 'int'): valor = 0
                elif(tipo == 'char'): valor = "''"
                elif(tipo == 'float'): valor = 0.0
                elif(tipo == 'double'): valor = 0.0
                else: valor = 'None'
                simbolo = tablaSimbolos.Simbolo(nombre, temporal, tipo, valor, ambito)
                tabla.newSimbolo(simbolo)
                self.concatenar(temporal+' = '+str(valor))  
            elif(type(nombre) is tuple):
                temporal = self.newTemp()
                nom = nombre[0]
                valor = self.InterpretarOperacion(nombre[1],tabla)
                if(type(valor) is str):
                    valor = "'"+valor+"'"
                simbolo = tablaSimbolos.Simbolo(nom, temporal, tipo, valor, ambito)
                tabla.newSimbolo(simbolo)
                self.concatenar(temporal+' = '+str(valor)) 

    #METODO PARA INTERPRETAR UNA OPERACION 
    def InterpretarOperacion(self, operacion, tabla):
        if isinstance(operacion, OpNumero):
            return operacion.valor
        elif isinstance(operacion, OpCadena):
            return operacion.valor

    #METODO PARA ARMAR EL RESULTADO
    def concatenar(self,cadena):
        self.resultado = self.resultado + cadena + '\n'

    #METODO PARA CREAR UN NUEVO TEMPORAL
    def newTemp(self):
        new = '$t'+str(self.temp)
        self.temp += 1
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
        <th>Identificador</th>
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
            valo = str(val.valor)
            temp = str(val.temporal)
            ambit = str(val.ambito)
            tipo = str(val.tipo)
            dim = str(val.dimension)
            dire = str(val.referencia)
            tshtml += '<tr><td>' + ide + '</td>'+'<td>' + temp + '</td>'+'<td>' + valo + '</td><td>'+ tipo  +'</td><td>'+dim+'</td><td>'+ambit +'</td><td>'+dire+'</td></tr>\n'
        tshtml += '</table>\n</body>\n</html>'
        f = open('ReporteTS.html', "w")
        f.write(tshtml)
        f.close()

    #METODO PARA VER LA TABLA DE SIMBOLOS
    def VerTablaSimbolos(self):
        os.system('start '+os.path.realpath('ReporteTs.html'))
        
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

    #METODO PARA LIMPIAR LAS TABLAS Y VARIABLES
    def reset(self):
        self.resultado = ''
        self.temp = 0
        self.tablaGlobal.simbolos.clear()
        self.tablaErrores.errores.clear()

#--------------------------------------loop para mantener la ejecucion del editor
if __name__ == "__main__":
    principal = gui.Tk()
    principal.state("zoomed")
    contenido = Editor(principal)
    principal.mainloop()