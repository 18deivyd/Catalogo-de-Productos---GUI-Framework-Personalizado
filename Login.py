import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Deivy
from PIL import ImageTk, Image 
import os
import Index
import mysql.connector
import Database
import sys

def recurso_ruta(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def validar_login():
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    
    try:
        conexion = Database.conectar_db()
        cursor = conexion.cursor()
        
        consulta = "SELECT * FROM usuario WHERE usuario_seccion = %s AND clave = %s AND activo = 1"
        cursor.execute(consulta, (usuario, clave))
        resultado = cursor.fetchone()
        
        if resultado:
            # Login exitoso
            v_login.destroy()
            Index.abrir_ventana_index(usuario)
        else:
            messagebox.showerror("Error", "Usuario o clave incorrectos")
            
        conexion.close()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Base de Datos", f"No se pudo conectar: {err}")

    # --- Interfaz del Login ---
configuracion_ventana = Deivy.Ventana(300,200, "Login - GrupoLosCar")
v_login = configuracion_ventana.construir()
v_login.resizable(0,0)
v_login.config(bg='#E0E0E0')
logo_referencia =[]

ruta_actual = os.path.dirname(__file__)
ruta = os.path.join(ruta_actual, 'Imagenes', 'Logo.png')

img_pil = Image.open(ruta) 
logo_tk = ImageTk.PhotoImage(img_pil) 
v_login.iconphoto(True, logo_tk)
v_login.logo_ref = logo_tk

# Centrar el contenido
frame_central = tk.Frame(v_login, bg='#E0E0E0')
frame_central.pack(expand=True)

Deivy.Labels(frame_central,"Usuario:", 0, 0, 'w', 2, 1).crear_label()
entry_usuario = tk.Entry(frame_central, width=30, font=("sans-serif", 10),border=0)
entry_usuario.grid(row=1, column=0, sticky= 'we')

Deivy.Labels(frame_central, "Contraseña:", 2, 0, 'w', 2, 1).crear_label()
entry_clave = tk.Entry(frame_central, width=30, show='*', font=("sans-serif", 10),border=0)
entry_clave.grid(row=3, column=0, sticky= 'we')

ruta_actual = os.path.dirname(__file__)
carpeta = os.path.join(ruta_actual, 'Imagenes')
ruta = os.path.join(carpeta, 'Ok.png')
ruta_config = os.path.join(carpeta, 'Configuracion.png')

btn = Deivy.Boton(ruta, frame_central, validar_login, 0, 10)
boton = btn.crear_boton(30,30,4,0, '', '#E1E1E1')

btn_config = Deivy.Boton(ruta_config, frame_central, Database.abrir_configuracion, 0, 10).crear_boton(20,20,0,1, 'ne', '#E1E1E1')

entry_clave.bind('<Return>', lambda e: validar_login())

v_login.mainloop()



