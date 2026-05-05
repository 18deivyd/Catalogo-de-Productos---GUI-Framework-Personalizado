import tkinter as tk
from tkinter import messagebox, ttk
import Deivy
import mysql.connector
import os
import Database

def abrir_ventana_usuario():
    conexion = Database.conectar_db() 
    
    def busqueda_usuario():
        busqueda= entry_busqueda.get()
        cursor = conexion.cursor()
        cursor.execute('Select id_usuario, usuario_seccion, nombre, activo FROM usuario WHERE usuario_seccion LIKE %s OR nombre LIKE %s', ('%' + busqueda + '%', '%' + busqueda + '%'))
        usuarios = cursor.fetchall()
        
        treeview_usuario.delete(*treeview_usuario.get_children())
        
        for usuario in usuarios:
            treeview_usuario.insert('','end', values=usuario) 
    
    configurar_ventana = Deivy.Ventana(1050, 320, 'Usuario')
    v_usuario = configurar_ventana.construir()
    v_usuario.resizable(0,0)
    v_usuario.config(bg = '#E1E1E1')
    v_usuario.grab_set()
    v_usuario.focus_set()
    
    style = ttk.Style()
    style.theme_use("clam") 

    style.configure("Treeview", 
                background="#ffffff",
                foreground="black",
                rowheight=25,
                fieldbackground="#ffffff",
                borderwidth=1,
                lightcolor="gray", 
                bordercolor="#D3D3D3")

    style.map("Treeview", 
          background=[('selected', '#347083')])

    style.configure("Treeview.Heading",
                background="#E1E1E1",
                foreground="black",
                relief="flat")
    
    lista_usuario = ('Codigo','Usuario','Nombre','Activo')
    treeview_usuario = ttk.Treeview(v_usuario, height=5, show='headings', columns=lista_usuario)
    treeview_usuario.pack(padx=10, pady=10, fill='x')
    
    treeview_usuario.config(style='Treeview')
    
    treeview_usuario.heading('Codigo', text='Codigo', anchor='w')
    treeview_usuario.heading('Usuario', text='Usuario', anchor='w')
    treeview_usuario.heading('Nombre', text='Nombre', anchor='w')
    treeview_usuario.heading('Activo', text='Activo', anchor='w')
    
    
    frame_busquedad = tk.Frame(v_usuario, bg='#e1e1e1')
    frame_busquedad.pack(fill='x', padx=10, pady=10)
    
    lbl_busqueda = Deivy.Labels(frame_busquedad, 'Busquedad:', 0, 0, 'e').crear_label()
    entry_busqueda = Deivy.Entrys(frame_busquedad, 50, 'normal', 0, 1, 'w').crear_entry()
    
    path = os.path.dirname(__file__)
    ruta_busqueda = os.path.join(path, 'Imagenes', 'Buscar.png')
    
    bnt_busqueda = Deivy.Boton(ruta_busqueda, frame_busquedad, busqueda_usuario, 10, 0).crear_boton(30, 30, 0, 2, 'w', '#e1e1e1')
    
    frame_usuario = tk.Frame(v_usuario, bg='#e1e1e1')
    frame_usuario.pack(fill='x', padx=10, pady=10)
    
    lbl_usuario = [('Usuario:', 0, 0), ('Nombre:', 0, 2), ('Clave:', 0, 4), ('Activo:', 0, 6)]
    
    for texto, fila, columna in lbl_usuario:
        Deivy.Labels(frame_usuario, texto, fila, columna, 'e').crear_label()
    
    ent_usuario = Deivy.Entrys(frame_usuario, 25, 'normal', 0, 1, 'w').crear_entry()
    ent_nombre = Deivy.Entrys(frame_usuario, 25, 'normal', 0, 3, 'w').crear_entry()
    ent_clave = Deivy.Entrys(frame_usuario, 25, 'normal', 0, 5, 'w').crear_entry()
    ent_activo = Deivy.Combobox(frame_usuario, (1, 0 ), 0, 7, 'w').crear_combobox()
    
    path = os.path.dirname(__file__)
    ruta_guardar = os.path.join(path, 'Imagenes', 'Ok.png')
    ruta_borrar = os.path.join(path, 'Imagenes', 'Salir.png')
    guardar_referencia = []
    borrar_referencia = [] 
    
    def mostrar_usuarios():
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, usuario_seccion, nombre, activo, clave FROM usuario")
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            treeview_usuario.insert('', 'end', values=usuario)
            
    mostrar_usuarios()

    
    def guardar_usuario():
        usuario = ent_usuario.get()
        nombre = ent_nombre.get()
        clave = ent_clave.get()
        activo = ent_activo.get()
        
        if not usuario or not nombre or not clave or not activo:
            messagebox.showerror('Error', 'Todos los campos son obligatorios')
            return
    
        try:
            cursor = conexion.cursor()
            cursor.execute('SELECT nombre FROM usuario WHERE usuario_seccion = %s', (usuario,))
            resultado = cursor.fetchone()
            
            if resultado:
                cursor.execute('UPDATE usuario SET usuario_seccion = %s, nombre = %s, clave = %s, activo = %s WHERE usuario_seccion = %s', (usuario, nombre, clave, activo, usuario))
                
                messagebox.showinfo('Modiificado', 'El usuario ha sido modificado correctamente')
            else:
                cursor.execute('INSERT INTO usuario (usuario_seccion, nombre, clave, activo) VALUES (%s, %s, %s, %s)', (usuario, nombre, clave, activo))
                
                messagebox.showinfo('Guardado', 'El usuario ha sido guardado correctamente')
                
                busqueda_usuario() # Refresca el Treeview
                for entry in [ent_usuario, ent_nombre, ent_clave, ent_activo]:
                    entry.delete(0, tk.END)

            conexion.commit()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar el usuario: {e}')
        finally:
            cursor.close()

    def eliminar_usuario():
        seleccion = treeview_usuario.focus()
        
        if seleccion:
            valores = treeview_usuario.item(seleccion, 'values')
            usuario_id = valores[0]
            
            confirmacion = messagebox.askyesno('Confirmar eliminación', '¿Estás seguro de que deseas eliminar este usuario?')
            
            if confirmacion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute('DELETE FROM usuario WHERE id_usuario = %s', (usuario_id,))
                    conexion.commit()
                    treeview_usuario.delete(seleccion)
                    messagebox.showinfo('Eliminado', 'El usuario ha sido eliminado correctamente')
                except Exception as e:
                    messagebox.showerror('Error', f'Error al eliminar el usuario: {e}')
            
    btn_guardar = Deivy.Boton(ruta_guardar, frame_busquedad, guardar_usuario, 10, 0).crear_boton(30, 30, 0, 3, 'w', '#e1e1e1')
    btn_borrar = Deivy.Boton(ruta_borrar, frame_busquedad, eliminar_usuario, 10, 1).crear_boton(30, 30, 0, 4, 'e', '#e1e1e1')
    
    guardar_referencia.append(btn_guardar)
    borrar_referencia.append(btn_borrar)   
    
    def seleccionar_usuario(event):
        seleccion = treeview_usuario.focus()
        
        if seleccion:
            valores = treeview_usuario.item(seleccion, 'values')
            ent_usuario.delete(0, tk.END)
            ent_clave.delete(0, tk.END)
            ent_nombre.delete(0, tk.END)
            ent_activo.delete(0, tk.END)
            
            ent_usuario.insert(0, valores[1])
            ent_nombre.insert(0, valores[2])
            ent_clave.insert(0, valores[4])
            ent_activo.insert(0, valores[3])

    treeview_usuario.bind('<ButtonRelease-1>', seleccionar_usuario)
    
    