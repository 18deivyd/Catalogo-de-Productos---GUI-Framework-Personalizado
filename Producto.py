import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import Deivy
import os 
import Database
import Kardex

def abrir_ventana_producto():
    conexion = Database.conectar_db()
    
        #Ventana Principal
    configuracion_ventana = Deivy.Ventana(1280,650, 'Producto')
    v_producto = configuracion_ventana.construir()
    v_producto.resizable(0,0)
    v_producto.config(background='#E2E2E2')
    v_producto.grab_set()
    v_producto.referencias = []

    
    #--Funcion Buscar--
    def buscar_producto():
        termino = txt_buscar.get() # Obtenemos el texto del Entry
        
        # Limpiar tabla para mostrar resultados
        for item in ventana_producto.get_children():
            ventana_producto.delete(item)
            
        try:
            cursor = conexion.cursor()
            # Consulta con filtros para nombre o código
            query = """
                SELECT p.Codigo, p.producto, 
                COALESCE(SUM(k.entrada), 0) - COALESCE(SUM(k.salida), 0) AS cantidad
                FROM producto p
                LEFT JOIN kardex k ON p.Codigo = k.Codigo
                WHERE p.producto LIKE %s OR p.Codigo LIKE %s
                GROUP BY p.Codigo, p.producto
                ORDER BY p.producto
            """
            cursor.execute(query, (f'%{termino}%', f'%{termino}%'))
            
            for fila in cursor.fetchall():
                ventana_producto.insert('', 'end', values=fila)
                
            actualizar_suma_total()
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            
    def actualizar_suma_total():
        total = 0
        
        for item in ventana_producto.get_children():
            # El valor de cantidad está en el índice 2 (Codigo=0, Producto=1, Cantidad=2)
            valores = ventana_producto.item(item)['values']
            if valores:
                try:
                    total += float(valores[2])
                except (ValueError, IndexError):
                    continue
    
        lbl_total_general.config(text=f"Total Inventario: {total:,.0f}")

    
        #Botones superior
    ventana_superior = tk.Frame(v_producto,
                                background= '#0f9fcf',
                                height=50)
    ventana_superior.pack(side='top', fill='x')
    ventana_superior.pack_propagate(False)

    ventana_superior.rowconfigure(0, weight=1)

    for i in range(14):
        ventana_superior.columnconfigure(i, weight=1)
        
    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_imgs = os.path.join(base_path, 'Imagenes')
    
    def ejecutar_kardex_con_seleccion():
        seleccion = ventana_producto.selection()
        if seleccion:
            valores = ventana_producto.item(seleccion)['values']
            codigo_seleccionado = valores[0]
            Kardex.abrir_ventana_kardex(codigo_seleccionado)
        else:
            messagebox.showinfo('Informacion',"Por favor, selecciona un producto primero")

    try:
        iconos = [
                ('Kardex.png', 0, ejecutar_kardex_con_seleccion),('Buscar.png', 1, buscar_producto),
        ]
        for nombre, columna, comando in iconos:
            ruta = os.path.join(folder_imgs, nombre)
            obj_boton = Deivy.Boton(ruta, ventana_superior, comando, 0, 0)
            boton = obj_boton.crear_boton(30, 30, 0, columna)
            v_producto.referencias.append(obj_boton)
    except Exception as e:
        messagebox.showerror('Error',f'Error cargando iconos: {e}')
        
        # Treeview Producto
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

        # Tabla de Productos
    lista_producto = ('Codigo', 'Producto', 'Cantidad')
    ventana_producto = ttk.Treeview(v_producto, columns=lista_producto, show='headings', height=7)
    ventana_producto.pack(padx=10, pady=10, fill='x')
    
    ventana_producto.configure(style="Treeview")
    
    ventana_producto.heading('Codigo', text='Codigo', anchor='w')
    ventana_producto.heading('Producto', text='Producto', anchor='w')
    ventana_producto.heading('Cantidad', text='Cantidad', anchor='w')
    
    ventana_producto.column('Codigo', width=20, anchor='w')
    ventana_producto.column('Producto', width=480, anchor='w')
    ventana_producto.column('Cantidad', width=200, anchor='w')

    referencias_caracteristicas = {}
    
              
    
    # Labels codigo y nombre del producto    
    frame_nombres = tk.Frame(v_producto, bg='#E2E2E2')
    frame_nombres.pack(pady=10)
    
    nombre_codigo = ttk.Label(frame_nombres, 
                                text='0',
                                font=("sans-serif", 12, "bold"), background='#E2E2E2')
    nombre_codigo.pack(side='left')
    nombre_espacio = ttk.Label(frame_nombres, 
                                text='-',
                                font=("sans-serif", 12, "bold"), background='#E2E2E2')
    nombre_espacio.pack(side='left')
    nombre_producto = ttk.Label(frame_nombres, 
                                text='Ningun Producto Selecionado',
                                font=("sans-serif", 12, "bold"), background='#E2E2E2')
    nombre_producto.pack(side='left')
        
        # Tabla de Almacen
    lista_Almacen = ('Codigo', 'Almacen', 'Cantidad')
    
    ventana_almacen = ttk.Treeview(v_producto, columns=lista_Almacen, show='headings', height=4)
    ventana_almacen.pack(padx=10, pady=10, fill='x')
    
    ventana_almacen.config(style='Treeview')
    
    ventana_almacen.heading('Codigo', text='Codigo', anchor='w')
    ventana_almacen.heading('Almacen', text='Almacen', anchor='w')
    ventana_almacen.heading('Cantidad', text='Cantidad', anchor='w')
    
    ventana_almacen.column('Codigo', width=20, anchor='w')
    ventana_almacen.column('Almacen', width=480, anchor='w')
    ventana_almacen.column('Cantidad', width=200, anchor='w')
    
        # --- LABEL PARA LA SUMA TOTAL ---
    lbl_total_general = tk.Label(v_producto, 
                                text="Total Inventario: 0", 
                                font=("sans-serif", 11, "bold"), 
                                bg='#E0E0E0', 
                                anchor='e')
    lbl_total_general.pack(fill='x', padx=10)
         
    # Caracteristica Producto
    frame_caracteristica = tk.Frame(v_producto,
                                    background= '#E0E0E0',
                                    height=200)
    frame_caracteristica.pack(fill='x', padx=10, pady=10)
    
    for i in range(6):
        frame_caracteristica.columnconfigure(i, weight=1)
        
    frame_caracteristica.rowconfigure(0, weight=1)
    frame_caracteristica.rowconfigure(1, weight=1)
    
    referencias_caracteristicas = {}
    
    labels = [('Departamento:',30,0,0,'e'), ('Línea:', 30, 0, 4, 'e'), ('Marca:',30, 1, 0,'e'), ('Caracteristica:', 100, 1, 4,'e')]
    
    for datos in labels:
        texto, ancho, fila, column, orientacion = datos
        
        lbl = Deivy.Labels(frame_caracteristica, texto, fila, column, orientacion)
        lbl.crear_label()
        
        entry = Deivy.Entrys(frame_caracteristica,ancho, 'disabled', fila, column + 1,'w')
        obj_entry = entry.crear_entry()
        
        nombre_llave = texto.replace(':', '').strip()
        referencias_caracteristicas[nombre_llave] = obj_entry
        
        
    def al_seleccionar_producto(event):
        seleccion = ventana_producto.selection()
        if not seleccion:
            return
            
        # Obtener el Código del producto seleccionado
        item = ventana_producto.item(seleccion)
        codigo_p = item['values'][0]
        
        try:
            cursor = conexion.cursor()
            
            # 1. BUSCAR DATOS TÉCNICOS EN TABLA PRODUCTO
            query_detalles = "SELECT departamento, linea, marca, caracteristica, producto FROM producto WHERE Codigo = %s"
            cursor.execute(query_detalles, (codigo_p,))
            res = cursor.fetchone()
            
            if res:
                # Actualizar los Labels de la cabecera
                nombre_codigo.config(text=str(codigo_p))
                nombre_producto.config(text=res[4])
                
                # Mapeo de datos para los Entrys de características
                # El orden en res es: 0:Dep, 1:Linea, 2:Marca, 3:Caracteristica
                datos_mapeo = {
                    'Departamento': res[0],
                    'Línea': res[1],
                    'Marca': res[2],
                    'Caracteristica': res[3]
                }
                
                # Llenar los campos usando el diccionario de referencias
                for nombre_campo, valor in datos_mapeo.items():
                    if nombre_campo in referencias_caracteristicas:
                        entry_widget = referencias_caracteristicas[nombre_campo]
                        entry_widget.config(state='normal') # Habilitar para escribir
                        entry_widget.delete(0, 'end')
                        entry_widget.insert(0, str(valor) if valor else "")
                        entry_widget.config(state='readonly') # Volver a proteger

            # 2. ACTUALIZAR VENTANA_ALMACEN (CONSULTA A KARDEX)
            # Limpiar tabla de almacén
            for i in ventana_almacen.get_children():
                ventana_almacen.delete(i)
                
            query_kardex = """
                SELECT 
                    Codigo,
                    ubicacion,
                    SUM(ingresos) - SUM(egresos) AS cantidad
                FROM (
                    SELECT 
                        Codigo, 
                        destino AS ubicacion, 
                        SUM(cantidad) AS ingresos, 
                        0 AS egresos
                    FROM kardex
                    WHERE tipo_movimiento IN ('1- Carga', '3- Traslado')
                    GROUP BY Codigo, destino

                    UNION ALL

                    SELECT 
                        Codigo, 
                        origen AS ubicacion, 
                        0 AS ingresos, 
                        SUM(cantidad) AS egresos
                    FROM kardex
                    WHERE tipo_movimiento IN ('2- Descarga', '3- Traslado')
                    GROUP BY Codigo, origen
                ) AS movimientos_consolidados
                WHERE Codigo = %s 
                GROUP BY Codigo, ubicacion;
            """
            cursor.execute(query_kardex, (codigo_p,))
            
            for fila_k in cursor.fetchall():
                ventana_almacen.insert('', 'end', values=fila_k)
                
        except Exception as e:
            print(f"Error al sincronizar selección: {e}")
    
    ventana_producto.bind('<<TreeviewSelect>>', al_seleccionar_producto)
        
        # --- FRAME DE BÚSQUEDA ---
    frame_buscar = tk.Frame(v_producto,
                            background= '#E0E0E0',
                            height=50)
    frame_buscar.pack(fill='x', padx=10, pady=10)
    
    frame_buscar.rowconfigure(0, weight=1)
    
    for i in range(4):
        frame_buscar.columnconfigure(i, weight=1)
        
    lbl_buscar = Deivy.Labels(frame_buscar, 'Busqueda:', 0, 0, 'e')
    lbl_buscar.crear_label()
        
    entry_busqueda_obj = Deivy.Entrys(frame_buscar, 100, 'normal', 0, 1, 'w')
    txt_buscar = entry_busqueda_obj.crear_entry()     

    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_imgs = os.path.join(base_path, 'Imagenes')
    ruta = os.path.join(folder_imgs, 'Buscar.png')
    
    boton_buscar = Deivy.Boton(ruta, frame_buscar, buscar_producto, 0, 0)
    btn_buscar = boton_buscar.crear_boton(30, 30, 0, 2, 'w', '#E0E0E0') 
    v_producto.referencias.append(boton_buscar)
    
    txt_buscar.bind('<Return>', lambda e: buscar_producto())

        # Carga inicial de todos los productos
    buscar_producto()

    
    
