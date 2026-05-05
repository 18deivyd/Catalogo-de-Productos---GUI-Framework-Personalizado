import tkinter as tk
from tkinter import ttk, messagebox
import Deivy
import Database
import os

def abrir_ventana_traslado(usuario_activo):
    conexion = Database.conectar_db()
    
    # El diccionario debe estar definido al inicio
    widgets_operacion = {}

    # --- FUNCIONES INTERNAS ---
    def busqueda():
        txt = entry_producto.get()
        for item in ventana_busqueda.get_children():
            ventana_busqueda.delete(item)
        try:
            cursor = conexion.cursor()
            consulta = '''SELECT p.Codigo, p.producto, COALESCE(SUM(k.entrada), 0) - COALESCE(SUM(k.salida), 0) AS cantidad 
            FROM producto as p LEFT JOIN kardex k ON p.Codigo = k.Codigo 
            WHERE p.producto LIKE %s OR p.Codigo LIKE %s GROUP BY p.Codigo, p.producto'''
            cursor.execute(consulta, (f'%{txt}%', f'%{txt}%'))
            for fila in cursor.fetchall():
                ventana_busqueda.insert('', 'end', values=fila)
        except Exception as e:
            print(f'Error en la busqueda: {e}')

    def agregar_a_lista():
        seleccion = ventana_busqueda.selection()
        if not seleccion:
            messagebox.showinfo('Informacion',"Seleccione un producto de la tabla inferior")
            return

        item_busqueda = ventana_busqueda.item(seleccion)
        codigo = item_busqueda['values'][0]
        nombre = item_busqueda['values'][1]

        # Ahora el diccionario ya tiene los widgets guardados
        origen = widgets_operacion['Origen'].get()
        destino = widgets_operacion['Destino'].get()
        cantidad = widgets_operacion['Cantidad'].get()
        estado = widgets_operacion['Estado'].get()
        u_seccion = widgets_operacion['Usuario_Seccion'].get()
        u_asignado = widgets_operacion['Usuario_Asignado'].get()
        obs_individual = widgets_operacion['Observacion'].get("1.0", "end-1c")
        
        if not cantidad or int(cantidad) <= 0:
            messagebox.showerror('Error',"Cantidad inválida")
            return

        ventana_producto.insert('', 'end', values=(
            codigo, nombre, origen, destino, cantidad, estado, u_asignado, u_seccion, obs_individual
        ))
        widgets_operacion['Cantidad'].delete(0, 'end')
        widgets_operacion['Observacion'].delete("1.0", "end")

    def guardar_todo_el_lote():
        filas = ventana_producto.get_children()
        if not filas:
            messagebox.showerror('Error',"No hay productos en la lista")
            return

        try:
            cursor = conexion.cursor()
            map_tipos = {1: '1- Carga', 2: '2- Descarga', 3: '3- Traslado'}
            tipo_seleccionado = variable_control.get()
            tipo_movimiento = map_tipos[tipo_seleccionado]
            
            concepto = widgets_operacion['Concepto'].get()
            user_logueado = widgets_operacion['Usuario_Seccion'].get()
            
            for fila_id in filas:
                datos = ventana_producto.item(fila_id)['values']
                cant = int(datos[4])
                u_asignado = datos[6]
                u_seccion  = datos[7]
                obs_item   = datos[8]
                
                entrada = cant if variable_control.get() == 1 else 0
                salida = cant if variable_control.get() == 2 else 0

                consulta = """INSERT INTO kardex (Codigo, fecha, tipo_movimiento, concepto, almacen, 
                              origen, destino, cantidad, entrada, salida, observacion, usuario_asignado, usuario_seccion)
                              VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                # datos[2] es origen, datos[3] es destino, datos[6] es usuario
                valores = (datos[0], tipo_movimiento, concepto, datos[2], datos[2], 
                           datos[3], cant, entrada, salida, obs_item, u_asignado, u_seccion)
                cursor.execute(consulta, valores)

            conexion.commit()
            messagebox.showinfo('Información',"Guardado exitoso")
            
            for i in ventana_producto.get_children(): 
                ventana_producto.delete(i)
            widgets_operacion['Observacion'].delete("1.0", "end")
            widgets_operacion['Concepto'].set('')
        except Exception as e:
            conexion.rollback()
            messagebox.showerror('Error',f"Error al guardar: {e}")
           
    def eliminar_item_lista():
        # 1. Obtener el item seleccionado
        seleccion = ventana_producto.selection()
        
        # 2. Validar que realmente haya algo seleccionado
        if not seleccion:
            messagebox.showerror('Error',"Por favor, seleccione una fila en la lista para eliminar.")
            return
            
        # 3. Eliminar la fila (o filas, si seleccionas varias)
        for fila in seleccion:
            ventana_producto.delete(fila)
            
        messagebox.showinfo('Informacion',"Producto eliminado de la lista temporal.")
        
        
        # --- DISEÑO DE INTERFAZ ---
    configuracion_ventana = Deivy.Ventana(940,800, 'Traslado, Carga y Descarga')
    v_traslado = configuracion_ventana.construir()
    v_traslado.resizable(0,0)
    v_traslado.config(bg='#E0E0E0')
    v_traslado.grab_set()
    v_traslado.focus_set()
    v_traslado.referencia =[]
    lista_referencias = []
    
    ventana_superior = tk.Frame(v_traslado, 
                                bg='#0f9fcf', 
                                height=30)
    ventana_superior.pack(side='top', fill='x')
    ventana_superior.pack_propagate(False)

        # Configuración de Rejilla (Grid)
    ventana_superior.rowconfigure(0, weight=1)

    for i in range(15):
        ventana_superior.columnconfigure(i, weight=1)

    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_imgs = os.path.join(base_path, 'Imagenes')

    try:
        #iconos = [('OK.png', 0, agregar_a_lista), ('Siguiente_izquierda.png', 1, None), ('Buscar.png', 2, busqueda),('Siguiente_derecha.png', 3, None), ('Final.png', 4, None), ('Nuevo.png', 6, None),('Guardar.png', 7, guardar_todo_el_lote), ('Salir.png', 8, eliminar_item_lista), ('Imprimir.png', 10, None),('Recargar.png', 11, None),]
        
        iconos = [('OK.png', 0, agregar_a_lista),('Buscar.png', 1, busqueda),('Guardar.png', 2, guardar_todo_el_lote), ('Salir.png', 3, eliminar_item_lista),]
        
        for nombre_arc, col, comando in iconos:
                ruta = os.path.join(folder_imgs, nombre_arc)
                # Pasamos v_catalogo para que la referencia se guarde ahí
                obj_btn = Deivy.Boton(ruta, ventana_superior, comando, 0, col)
                btn_widget = obj_btn.crear_boton(30, 30, 0, col)
                
                lista_referencias.append(obj_btn)
    except Exception as e:
        print(f'Error cargando iconos: {e}')
            
        # Frame operaciones
    datos_operaciones = tk.LabelFrame(v_traslado,
                                text="Datos de la Operación:",
                                bg='#E1E1E1',
                                height=200)
    datos_operaciones.pack(fill='x', padx=10, pady=10)

    tipos_operaciones = tk.LabelFrame(datos_operaciones,
                                    text='Tipos de Operaciones',
                                    bg= '#E1E1E1')
    tipos_operaciones.grid(row=0, column=0 , padx=20, pady=5)

    variable_control = tk.IntVar(value=1) 
    tipos = [('1- Carga', 1), ('2- Descarga', 2), ('3- Traslado', 3)]
    for i, (texto, valor) in enumerate(tipos):
        tk.Radiobutton(tipos_operaciones, text=texto, variable=variable_control, value=valor, bg='#E1E1E1').grid(row=0, column=i, padx=5)
        
        # Usuario LOGIN    
    tk.Label(datos_operaciones, text="Usuario:", bg='#E1E1E1').grid(row=0, column=3, sticky='e')
    ent_user = Deivy.Entrys(datos_operaciones, 30, 'normal', 0, 4, 'w').crear_entry()
    ent_user.insert(0, usuario_activo) # Insertamos el usuario que vino del login
    ent_user.config(state='readonly')  # Lo bloqueamos para que sea informativo
    widgets_operacion['Usuario_Seccion'] = ent_user

    nombres_c = ['Concepto', 'Origen', 'Destino']
    listas_c = [['Apertura','Avería','Cambio','Compra', 'Despacho','Devolución por Garantía','Error en Pedido','Faltante','Isntalación','Merma','Migración','Producto Defectuoso','Producto Terminado','Obsolescencia','Recepción','Reparación','Repuesto','Sobrante','Venta'], ['GrupoLosCar', 'Eleconstruc', 'Davan', 'Lompane', 'Lalobarda', 'Preventud Plus','Almacen'],['GrupoLosCar', 'Eleconstruc', 'Davan', 'Lompane', 'Lalobarda', 'Preventud Plus','Almacen']]
    
    for i, nombre in enumerate(nombres_c, start=1):
        # Primero creamos el Label
        tk.Label(datos_operaciones, text=f"{nombre}:", bg='#E1E1E1').grid(row=i, column=0, sticky='w', padx=20)
        # Creamos y guardamos el Combobox
        widgets_operacion[nombre] = Deivy.Combobox(datos_operaciones, listas_c[i-1], i, 0, 'e', 30).crear_combobox()

    # Estado
    tk.Label(datos_operaciones, text="Estado:", bg='#E1E1E1').grid(row=4, column=0, sticky='w', padx=20)
    widgets_operacion['Estado'] = Deivy.Combobox(datos_operaciones, ['Nuevo', 'Usado'], 4, 0, 'e', 30).crear_combobox()

    # Cantidad y Usuario
    tk.Label(datos_operaciones, text="Cantidad:", bg='#E1E1E1').grid(row=1, column=3, sticky='e')
    widgets_operacion['Cantidad'] = Deivy.Entrys(datos_operaciones, 5, 'normal', 1, 4, 'w').crear_entry()

    tk.Label(datos_operaciones, text="Asignado a:", bg='#E1E1E1').grid(row=2, column=3, sticky='e')
    widgets_operacion['Usuario_Asignado'] = Deivy.Entrys(datos_operaciones, 30, 'normal', 2, 4, 'w').crear_entry()

    # Observación
    tk.Label(datos_operaciones, text="Observación:", bg='#E1E1E1').grid(row=3, column=3, sticky='e')
    widgets_operacion['Observacion'] = Deivy.Textos(datos_operaciones, 60, 4, 3, 4, 'se', 2, 1).crear_text()
    
    

    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Treeview", background="white", fieldbackground="white", rowheight=25)
    style.map("Treeview", background=[('selected', '#347083')])
    style.configure("Treeview.Heading",
                    background="#E1E1E1",
                    foreground="black",
                    relief="flat")

    lista_producto = ['Codigo', 'Producto', 'Origen', 'Destino', 'Cantidad', 'Estado','Usuario']

    ventana_producto = ttk.Treeview(v_traslado, columns=lista_producto, show='headings', height=7)
    ventana_producto.pack(padx=10, pady=10, fill='x')

    ventana_producto.configure(style='Treeview')

    ventana_producto.heading('Codigo', text='Código', anchor='w')
    ventana_producto.heading('Producto', text='Producto', anchor='w')
    ventana_producto.heading('Origen', text='Origen', anchor='w')
    ventana_producto.heading('Destino', text='Destino', anchor='w')
    ventana_producto.heading('Cantidad', text='Cant.', anchor='w')
    ventana_producto.heading('Estado', text='Estado', anchor='w')
    ventana_producto.heading('Usuario', text='Usuario', anchor='w')

    ventana_producto.column('Codigo', width=70)
    ventana_producto.column('Producto', width=250)
    ventana_producto.column('Origen', width=150)
    ventana_producto.column('Destino', width=150)
    ventana_producto.column('Cantidad', width=70)
    ventana_producto.column('Estado', width=100)
    
    lista_busqueda = ['Codigo', 'Producto', 'Total']
    
    ventana_busqueda = ttk.Treeview(v_traslado, columns=lista_busqueda, show='headings', height=5)
    ventana_busqueda.pack(padx=10, pady=10, fill='x')
    ventana_busqueda.configure(style='Treeview')
    
    ventana_busqueda.heading('Codigo', text='Codigo', anchor='w')
    ventana_busqueda.column('Codigo', width=70)
    
    ventana_busqueda.heading('Producto', text='Producto', anchor='w')
    ventana_busqueda.column('Producto', width=250)
    
    ventana_busqueda.heading('Total', text='Total', anchor='w')
    ventana_busqueda.column('Total', width=100)

    frame_busqueda = tk.Frame(v_traslado,height=30, bg='#E1E1E1')
    frame_busqueda.pack(fill='x', padx=10, pady=10)

    lbl_producto = Deivy.Labels(frame_busqueda, 'Producto:', 0, 0, 'e').crear_label()
    entry_producto = Deivy.Entrys(frame_busqueda, 60,'normal', 0, 1, 'w').crear_entry()

    ruta = os.path.join(folder_imgs, 'Buscar.png')
    boton_producto = Deivy.Boton(ruta, frame_busqueda, busqueda, 0, 0).crear_boton(30, 30, 0, 2, 'e', '#E1E1E1')       
    
    # --- BINDINGS ---
    entry_producto.bind('<Return>', lambda e: busqueda())
    widgets_operacion['Cantidad'].bind('<Return>', lambda e: agregar_a_lista())
    
    ventana_producto.bind('<Delete>', lambda e: eliminar_item_lista())
        
