import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import Deivy
import Catalogo
import Traslado
import Producto
import Usuario
import os
import sys

def abrir_ventana_index(usuario_activo):
        # Configuración de Ventana
    configuracion_ventana = Deivy.Ventana(1280, 720, 'Grupo Loscar - Sistema Administrativo')
    mi_ventana = configuracion_ventana.construir()
    mi_ventana.state('zoomed')
    
    logo_referencia = []   
    ref = []     
    

    # Manejo de Rutas
    def recurso_ruta(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    directorio_actual = os.path.dirname(__file__)
    ruta_logo = os.path.join(directorio_actual, 'Imagenes', 'logo.png')
    logo = tk.PhotoImage(file=ruta_logo)
    mi_ventana.iconphoto(False, logo)
    logo_referencia.append(logo)
    
    frame_botones = tk.Frame(mi_ventana, bg='#0f9fcf', height=50)
    frame_botones.pack(fill='x')
    
    lista_btn = [('Producto.png', Producto.abrir_ventana_producto,0,0),('Traslado.png', lambda: Traslado.abrir_ventana_traslado(usuario_activo),0,1),('Producto.png', Catalogo.abrir_ventana_catalogo,0,2),('Usuario.png', Usuario.abrir_ventana_usuario,0,3)]
    
    path_base = os.path.dirname(__file__)
    
    for nombre, comando, fila, columna in lista_btn:      
        ruta = os.path.join(path_base, 'Imagenes', nombre)
        
        instancia_btn = Deivy.Boton(ruta, frame_botones,comando,5,5)
        boton = instancia_btn.crear_boton(40,40,fila,columna, '', '#0f9fcf')
        ref.append(boton)

    #barra_menu = tk.Menu(mi_ventana, 
                        ##fg='black', # Color de texto
                        #activebackground='#8ecda0', 
                        #bd=0,
                        #font=('sans-serif', 12, 'bold'))

    #opciones_menu = tk.Menu(barra_menu, 
                            #tearoff=0,
                            #fg='black',            
                            #activebackground='#B9FBC0', 
                            #activeforeground='black', 
                            #font=('sans-serif', 10))
    #opciones_menu.add_command(label='Producto', command=Producto.abrir_ventana_producto)
    #opciones_menu.add_command(label='Traslado', command=lambda: Traslado.abrir_ventana_traslado(usuario_activo))
    #opciones_menu.add_command(label='Catalogo', command=Catalogo.abrir_ventana_catalogo)
    #opciones_menu.add_command(label='Usuario', command=Usuario.abrir_ventana_usuario)
    
    #barra_menu.add_cascade(label='Opciones', 
                        #menu=opciones_menu,
                        #font=('sans-serif', 12, 'bold'))

    #mi_ventana.config(menu=barra_menu)

    # --- MANEJO DE FONDO ---
    ruta_fondo = os.path.join(directorio_actual, 'Imagenes', 'fondo.png')
    imagen_pil = Image.open(ruta_fondo) # Cargamos la imagen original con PIL

    # Función interna para redimensionar
    def ajustar_fondo(event):
        nuevo_ancho = event.width
        nuevo_alto = event.height
        
        # Redimensionar imagen al tamaño de la ventana
        imagen_res = imagen_pil.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        foto_tk = ImageTk.PhotoImage(imagen_res)

        # Actualizamos el Label que contiene el fondo
        lbl_fondo.config(image=foto_tk)
        lbl_fondo.image = foto_tk # Mantener referencia

    # Crear el Label del fondo
    lbl_fondo = tk.Label(mi_ventana)
    lbl_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # --- LABEL DE SESIÓN ---
    # Lo colocamos con .place o aseguramos que esté por encima
    lbl_session = tk.Label(mi_ventana, 
                           text=f"{usuario_activo}", 
                           font=('sans-serif', 8, 'bold'),
                           fg='#0055ff')
    lbl_session.place(x=20, y=10) # Usamos place para que flote sobre el fondo
    lbl_session.pack(side='right', anchor='n')
    
    # Aseguramos que el fondo se vaya atrás de todo
    lbl_fondo.lower()
    

    mi_ventana.bind('<Configure>', ajustar_fondo)
    

    


