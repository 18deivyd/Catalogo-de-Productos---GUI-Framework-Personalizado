import mysql.connector
import Deivy
import tkinter as tk
from tkinter import messagebox
import os 
import json

CONFIG_FILE = "config_db.json"

def guardar_json(ent_host, ent_user, ent_passw, ent_db):
        datos = {
                "host": ent_host.get(),
                "user": ent_user.get(),
                "password": ent_passw.get(),
                "database": ent_db.get(),
        }
        with open(CONFIG_FILE, "w") as f:
                json.dump(datos, f, indent=4)
        print("Configuración guardada exitosamente.")
        
def conectar_db():
        try:
                if os.path.exists(CONFIG_FILE):
                        with open(CONFIG_FILE, 'r') as f:
                                config = json.load(f)
                                
                        conexion = mysql.connector.connect(
                                host=config.get('host'),
                                user=config.get('user'),
                                password=config.get('password'),
                                database=config.get('database'))
                        return conexion
                else:
                        return None
                
        except mysql.connector.Error as err:
                messagebox.showinfo('Error',f"Error de conexión: {err}")
                
        

def abrir_configuracion():
        configuracion_ventana = Deivy.Ventana(600, 300, 'Configuración SQL')
        v_configuracion = configuracion_ventana.construir()
        v_configuracion.config(bg= '#e1e1e1')
        v_configuracion.resizable(0,0)

        frame_centra = tk.Frame(v_configuracion,
                                bg= '#e1e1e1',
                                bd=1,
                                relief='solid')
        frame_centra.grid( row=1, column=0, padx=40)
        
        lbl_titulo = Deivy.Labels(v_configuracion, 'CONEXION A SERVIDOR', 0, 0, '',2).crear_label()
        
        lbl_txt = [('Host o Ip:',1,0),('Usuario:',2,0),('Clave:',3,0),('Bases de Datos:',4,0)]
        
        for nombre, fila, columna in lbl_txt:
                Deivy.Labels(frame_centra, nombre, fila, columna, 'e').crear_label()
        
        ent_host = Deivy.Entrys(frame_centra, 50, 'normal', 1, 1, 'w').crear_entry()
        ent_user = Deivy.Entrys(frame_centra, 50, 'normal', 2, 1, 'w').crear_entry()
        ent_passw = Deivy.Entrys(frame_centra, 50, 'normal', 3, 1, 'w', show='*').crear_entry()
        ent_db = Deivy.Entrys(frame_centra, 50, 'normal', 4, 1, 'w', show='*').crear_entry()
        
        if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                        datos_cargados = json.load(f)
                        ent_host.insert(0, datos_cargados.get("host", ""))
                        ent_user.insert(0, datos_cargados.get("user", ""))
                        ent_passw.insert(0, datos_cargados.get("password", ""))
                        ent_db.insert(0, datos_cargados.get("database", ""))
        
        path = os.path.dirname(__file__)
        ruta = os.path.join(path, 'Imagenes', 'Ok.png')                
        
        bn_guardar = Deivy.Boton(ruta,v_configuracion,lambda: [guardar_json(ent_host, ent_user, ent_passw, ent_db), v_configuracion.destroy()],30,30).crear_boton(30,30,2,0,'e','#e1e1e1')
        
        



