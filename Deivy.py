import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Ventana:
    def __init__(self, ancho, alto, titulo=""):
        self.ancho = ancho
        self.alto = alto
        self.titulo = titulo

    def construir(self):
        try:
            if tk._default_root is None:
                self.ventana = tk.Tk()
            else:
                self.ventana = tk.Toplevel()
        except:
            self.ventana = tk.Toplevel()
        
        self.ventana.title(self.titulo)
        
        self.ventana.update_idletasks()
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        posicion_x = (ancho_pantalla // 2) - (self.ancho // 2)
        posicion_y = (alto_pantalla // 2) - (self.alto // 2)

        self.ventana.geometry(f"{self.ancho}x{self.alto}+{posicion_x}+{posicion_y}")
       
        return self.ventana
    
class Boton:
    def __init__(self, ruta_archivo, contenedor, comando, padx, pady):
        self.ruta_archivo = resource_path(ruta_archivo) 
        self.contenedor = contenedor
        self.comando = comando
        self.padx = padx
        self.pady = pady
        self.image_ref = None 

    def crear_boton(self, imgtamx=0, imgtamy=0, fila=0, columna=0, sticky='nsew', bg='#0f9fcf'):      
        try:
            if not os.path.exists(self.ruta_archivo):
                raise FileNotFoundError(f"No existe: {self.ruta_archivo}")

            imagen = Image.open(self.ruta_archivo)
            imagen_redimensionada = imagen.resize((imgtamx, imgtamy), Image.LANCZOS) # Añadido LANCZOS para calidad
            
            self.image_ref = ImageTk.PhotoImage(imagen_redimensionada, master=self.contenedor)
            
            boton = tk.Button(self.contenedor, 
                              image=self.image_ref, 
                              border=0,
                              bg=bg, 
                              activebackground=bg,
                              command=self.comando)
            
            boton.image = self.image_ref 
            boton.grid(row=fila, column=columna, padx=self.padx, pady=self.pady, sticky=sticky)
            return boton
            
        except Exception as e:
            print(f"Error en Botón ({self.ruta_archivo}): {e}")
            boton_error = tk.Button(self.contenedor, text="Error", command=self.comando, bg="red")
            boton_error.grid(row=fila, column=columna)
            return boton_error
        
class Labels:
    def __init__(self, contenedor, texto_label, fila, columna, orientacion, columnspan=1, rowspan=1):
        self.contenedor = contenedor
        self.texto_label =texto_label
        self.columna = columna
        self.fila = fila
        self.orientacion = orientacion 
        self.rowspan = rowspan
        self.columnspan= columnspan
    
    def crear_label(self):
        lbl = tk.Label(self.contenedor,
                    text=self.texto_label,
                    bg='#E2E2E2',
                    font=("sans-serif", 12, "bold"),
                    anchor='e')
        lbl.grid(row=self.fila, column=self.columna, sticky=self.orientacion, pady=10, padx=5, rowspan=self.rowspan, columnspan=self.columnspan)
        return lbl

class Entrys:
    def  __init__(self, ventana,width,state,fila, columna, orientacion, rowspan=None, columnspan=None, show=''):
        self.ventana = ventana
        self.width = width
        self.state = state
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.columnspan = columnspan
        self.rowspan = rowspan        
        self.show = show
        
    def crear_entry(self):
        entry = tk.Entry(self.ventana,
                        width=self.width,
                        font=("sans-serif", 10),
                        highlightthickness= 2,
                        highlightcolor='#30A050',
                        relief="flat",
                        border=0,
                        state=self.state,
                        show=self.show)
        entry.grid(row=self.fila, 
                   column=self.columna, 
                   sticky=self.orientacion, 
                   pady=10, 
                   padx=5, 
                   rowspan=self.rowspan, 
                   columnspan=self.columnspan)
        return entry
    
class Textos:
    def  __init__(self, ventana, width, height, fila, columna, orientacion, rowspan=None, columnspan=None, estado='normal'):
        self.ventana = ventana
        self.width = width
        self.height = height
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.columnspan = columnspan
        self.rowspan = rowspan   
        self.estado = estado
    
    def crear_text(self):
        texto = tk.Text(self.ventana,
                            width=self.width,
                            height=self.height,
                            font=("sans-serif", 10),
                            highlightthickness=2,
                            highlightcolor='#30A050',
                            relief="flat",
                            state=self.estado)
        texto.grid(row=self.fila, column=self.columna, sticky=self.orientacion, pady=10, padx=5, rowspan=self.rowspan, columnspan=self.columnspan)
        
        return texto
    
class Combobox:
    def __init__(self, ventana, opciones_lista, row, column, sticky='we', width=12):
        self.ventana = ventana
        self.opciones_lista = opciones_lista
        self.row = row
        self.column = column
        self.sticky = sticky
        self.width = width
    
    def crear_combobox(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TCombobox", 
                        fieldbackground="#ffffff",
                        font=("sans-serif", 10))
        
        lista = ttk.Combobox(self.ventana, 
                            values=self.opciones_lista, 
                            state="readonly", 
                            font=("sans-serif", 10),
                            width=self.width,
                            style="Custom.TCombobox") # Aplicamos el estilo
        
        lista.grid(row=self.row, column=self.column, sticky=self.sticky, pady=10, padx=5)
        lista.set("Seleccionar")
        
        return lista
    
