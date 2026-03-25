import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Ventana:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
    
    def construir(self):
        ventana = tk.Tk()
        ventana.update_idletasks()
        
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        
        posicion_x = (ancho_pantalla // 2) - (self.ancho // 2)
        posicion_y = (alto_pantalla // 2) - (self.alto // 2)

        ventana.geometry(f"{self.ancho}x{self.alto}+{posicion_x}+{posicion_y}")
        return ventana
    
class Boton:
    def __init__(self, nombre_archivo, contenedor, comando, padx, pady):
        self.nombre_archivo = nombre_archivo
        self.contenedor = contenedor
        self.comando = comando
        self.padx = padx
        self.pady = pady
        self.image_ref = None # Referencia para que no se borre la imagen
    
    
    def crear_boton(self,x=0, y=0, fila=0, columna=0, sticky='nsew', bg='#B9FBC0'):
        # Verificamos si ya tiene la extensión .png, si no, se la ponemos
        ruta = self.nombre_archivo if self.nombre_archivo.lower().endswith('.png') else f"{self.nombre_archivo}.png"
        
        try:
            imagen = Image.open(ruta)
            imagen_redimensionada = imagen.resize((x, y))
            self.image_ref = ImageTk.PhotoImage(imagen_redimensionada)
            
            boton = tk.Button(self.contenedor, 
                              image=self.image_ref, 
                              border=0,
                              bg= bg, # Volvemos al verde una vez que funcione
                              command=self.comando)
            
            # Doble seguro para la imagen
            boton.image = self.image_ref 
            
            # Usamos grid con sticky para que se centre en la celda
            boton.grid(row=fila, column=columna, padx=self.padx, pady=self.pady, sticky=sticky)
            return boton
            
        except Exception as e:
            print(f"Error al cargar la imagen en: {ruta}. Error: {e}")
            # Si falla la imagen, crea un botón de texto para que al menos veas algo
            boton_error = tk.Button(self.contenedor, text="Err", command=self.comando)
            boton_error.grid(row=fila, column=columna)
            return boton_error
        
class Labels:
    
    def __init__(self, contenedor, texto_label, fila, columna, orientacion, columnspan=None, rowspan=None):
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
                    foreground='#000',
                    font=("sans-serif", 12, "bold"),
                    anchor='e')
        lbl.grid(row=self.fila, column=self.columna, sticky=self.orientacion, pady=10, padx=5, rowspan=self.rowspan, columnspan=self.columnspan)
        return lbl

class Entrys:
    def  __init__(self, ventana,width,state,fila, columna, orientacion, rowspan=None, columnspan=None):
        self.ventana = ventana
        self.width = width
        self.state = state
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.columnspan = columnspan
        self.rowspan = rowspan        
        
    def crear_entry(self):
        entry = tk.Entry(self.ventana, 
                        width=self.width, 
                        font=("sans-serif", 10),
                        highlightthickness= 2,
                        highlightcolor='#30A050',
                        relief="flat",
                        border=0,
                        state=self.state)
        entry.grid(row=self.fila, column=self.columna, sticky=self.orientacion, pady=10, padx=5, rowspan=self.rowspan, columnspan=self.columnspan)
        
        return entry
    
class Textos:
    def  __init__(self, ventana, width, height, fila, columna, orientacion, rowspan=None, columnspan=None):
        self.ventana = ventana
        self.width = width
        self.height = height
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.columnspan = columnspan
        self.rowspan = rowspan   
    
    def crear_text(self):
        texto = tk.Text(self.ventana,
                            width=self.width,
                            height=self.height,
                            font=("sans-serif", 10),
                            highlightthickness=2,
                            highlightcolor='#30A050',
                            relief="flat")
        texto.grid(row=self.fila, column=self.columna, sticky=self.orientacion, pady=10, padx=5, rowspan=self.rowspan, columnspan=self.columnspan)
        
        return texto
    
class Combobox:
    def __init__(self, ventana, opciones_lista, row, column, sticky='center'):
        self.ventana = ventana
        self.opciones_lista = opciones_lista
        self.row = row
        self.column = column
        self.sticky = sticky
    
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
                            width=12,
                            style="Custom.TCombobox") # Aplicamos el estilo
        
        lista.grid(row=self.row, column=self.column, sticky=self.sticky, pady=10, padx=5)
        lista.set("Seleccionar")
        
        return lista
    
