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
        ejecutar.add_command(label="Reporte de Errores", command=parent.Reporte)
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

#--------------------------------------clase que maneja el editor de texto
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
        self.resaltarTexto("\\$.([0-9])([0-9])*", "dolar",er=True)
        self.resaltarTexto("exit", "exit")
        self.resaltarTexto("(\\$ra|\\$sp)", "regs",er=True)
        self.resaltarTexto("(goto|if)", "goto",er=True)
        self.resaltarTexto("(main|unset|print|read|int|float|char)", "reservadas",er=True)
        self.resaltarTexto("(\\+|=|-|\\*|abs|%|!|\\||xor|and|\\^|<|>)", "signos",er=True)
        self.resaltarTexto("(\\[|\\]|\\(|\\))", "agrup",er=True)
        self.resaltarTexto("#(.)+([^\r\n])", "com",er=True)
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

#--------------------------------------clase que actualiza los numeros de linea
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
            
#--------------------------------------clase que maneja la ventana principal
class Editor:

    #variables
    resultado = ''
    analisis_listo = False
    idcount = 0
    arbol = None
    newvar = None
    debug = False
    dot = None
    tipoanalisis = True
    terminar = False

    i = 0    
    encontre = 'Global'

    #constructor
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

    def inc(self):
        self.i += 1
        return self.i

    #metodo para cambiar la ayuda de la ventana
    def CambiarTitulo(self, name=None):
        if name:
            self.principal.title(name + "- Augus")
        else:
            self.principal.title("Sin titulo - Augus")

    #metodo para crear un nuevo documento
    def Nuevo(self):
        self.textarea.delete(1.0, gui.END)
        self.consola.delete(1.0,gui.END)
        self.nombre = None
        self.CambiarTitulo()

    #metodo para abrir un documento
    def Abrir(self):
        self.nombre = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All files","*.*"),("Python","*.py")])
        if self.nombre:
            self.textarea.delete(1.0, gui.END)
            with open(self.nombre, "r") as file:
                self.textarea.insert(1.0, file.read())
            self.CambiarTitulo(self.nombre)
            self.textarea.numeros_linea.redraw()
            self.textarea.delay()
    
    #metodo para guardar un documento
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
    
    #metodo para hacer el guardar como
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

    #metodo para copiar
    def Copiar(self):
        self.textarea.clipboard_clear()
        self.textarea.clipboard_append(self.textarea.selection_get())

    #metodo para pegar
    def Pegar(self):
        self.textarea.insert(gui.INSERT,self.textarea.clipboard_get())

    #metodo para cortar
    def Cortar(self):
        self.Copiar()
        self.textarea.delete('sel.first','sel.last')

    #metodo para Buscar
    def Buscar(self):
        cadena = simpledialog.askstring('Buscar','Cadena a buscar:',parent=principal)
        self.textarea.resaltarTexto(cadena,'buscar')

    #metodo para reemplazar
    def Reemplazar(self):
        abuscar = simpledialog.askstring('Buscar','Cadena a buscar:',parent=principal)
        aremplazar = simpledialog.askstring('Reemplazar','Nueva cadena:',parent=principal)
        cadena = self.textarea.cuadro.get('1.0',gui.END)
        self.textarea.delete('1.0',gui.END)
        self.textarea.insert(gui.INSERT,cadena.replace(abuscar,aremplazar))

    #metodo para hacer el analisis ascendente
    def AnalisisAsc(self):
        pass
        
    # metodo para avanzar en el debug
    def SiguientePaso(self):
        pass

    # metodo para cambiar el color del tema
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

    # metodo para quitar los numeros de linea
    def QuitarNums(self):
        if (self.numeros == 1):
            self.textarea.numeros_linea.config(width=0)
            self.numeros = 0
        else:
            self.textarea.numeros_linea.config(width=20)
            self.numeros = 1

    # metodo para hacer el reporte gramatical
    def RepGramatical(self):
        pass

    # metodo para hacer el reporte de errores
    def Reporte(self):
        pass

    #metodo para hacer el reporte
    def VerTablaSimbolos(self):
        pass
        
    def stop(self):
        pass

    # metodo para crear un error semantico
    def errorSemantico(self,descripcion,info1,info2):
        pass

    # metodo para abrir el reporte del ast
    def VerAST(self):
        pass

    def reset(self):
        pass

#--------------------------------------loop para mantener la ejecucion del editor
if __name__ == "__main__":
    principal = gui.Tk()
    principal.state("zoomed")
    contenido = Editor(principal)
    principal.mainloop()