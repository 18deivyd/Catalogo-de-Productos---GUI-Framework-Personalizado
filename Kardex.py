import tkinter as tk
from tkinter import ttk, messagebox
import Deivy
import mysql.connector
import Database
import qrcode
from PIL import ImageTk, Image 


def abrir_ventana_kardex(codigo_producto):
    conexion = Database.conectar_db()
    
    print(f"Abriendo Kardex para el producto: {codigo_producto}")
             
        #---Creacion de ventana---     
    configuracion_ventana = Deivy.Ventana(1280,600,'Kardex')
    v_kardex = configuracion_ventana.construir()
    v_kardex.resizable(0,0)
    v_kardex.config(bg= '#E1E1E1')
    v_kardex.grab_set()
    v_kardex.focus_set()
        
        #---Treeview---
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


    lista_busqueda=('Codigo','Producto','Total')
    treeview_superior = ttk.Treeview(v_kardex, columns=lista_busqueda, show='headings', height=1)
    treeview_superior.pack(padx=10, pady=10, fill='x')
    treeview_superior.configure(style='Treeview')

    treeview_superior.heading('Codigo', text='Codigo', anchor='w')
    treeview_superior.heading('Producto', text='Producto', anchor='w')
    treeview_superior.heading('Total', text='Total', anchor='w')

    treeview_superior.column('Codigo', width=20, anchor='w')
    treeview_superior.column('Producto', width=480, anchor='w')
    treeview_superior.column('Total', width=220, anchor='w')
    
    referencia_busqueda = {}
    
    lista_historial = ('Fecha', 'Almacen', 'Referencia', 'Tipo de Movimiento', 'Concepto', 'Cantidad')
    treeview_kardex = ttk.Treeview(v_kardex, columns=lista_historial, show='headings', height=10)
    treeview_kardex.pack(padx=10, pady=10, fill='x')
    treeview_kardex.configure(style='Treeview')
    
    treeview_kardex.heading('Fecha', text='Fecha', anchor='w')
    treeview_kardex.heading('Almacen', text='Almacen', anchor='w')
    treeview_kardex.heading('Referencia', text='Referencia', anchor='w')
    treeview_kardex.heading('Tipo de Movimiento', text='Tipo de Movimiento', anchor='w')
    treeview_kardex.heading('Concepto', text='Concepto', anchor='w')
    treeview_kardex.heading('Cantidad', text='Cantidad', anchor='w')

    frame_detalles = tk.Frame(v_kardex, bg='#E2E2E2', border=1, relief='solid')
    frame_detalles.pack(padx=10,expand=True, side='left', fill='x')

    lista_lbl = [('Usuario:',0,0), ('Origen:',1,0), ('Responsable:', 2, 0), ('Cant Asignada:', 0, 2), ('Observación:', 1, 2)]
    
    for nombre, fila, columna in lista_lbl:
        lbl = Deivy.Labels(frame_detalles, nombre, fila, columna, 'e')
        lbl.crear_label()

    ent_usuario = Deivy.Entrys(frame_detalles, 30, 'disabled', 0, 1, 'w').crear_entry()
    
    ent_origen = Deivy.Entrys(frame_detalles, 30, 'disabled', 1, 1, 'w').crear_entry()
    
    ent_responsable = Deivy.Entrys(frame_detalles, 30, 'disabled', 2, 1, 'w').crear_entry()
    
    ent_cantidad = Deivy.Entrys(frame_detalles, 15, 'disabled', 0, 3, 'w').crear_entry()
    
    texto_observaccion = Deivy.Textos(frame_detalles, 60, 4, 1, 3,'w',2,estado='disabled')
    txt_observacion = texto_observaccion.crear_text()
    
    lbl_qr = tk.Label(v_kardex, bg='white', bd=1, relief='sunken')
    lbl_qr.pack(side='right', padx=10, expand=True)
    
    def actualizar_qr_en_pantalla(datos_producto):
        """Genera el QR basado en la info real de la selección"""
        # Formateamos el texto del QR según tu solicitud
        contenido = (
            f"Producto: {datos_producto.get('producto', 'N/A')}\n"
            f"Fecha: {datos_producto.get('fecha', 'N/A')}\n"
            f"Marca: {datos_producto.get('marca', 'N/A')}\n"
            f"Responsable: {datos_producto.get('usuario_asignado', 'N/A')}\n"
            f"Destino: {datos_producto.get('destino', 'N/A')}\n"
            f"Observacion: {datos_producto.get('observacion', 'N/A')}"
        )
        
        qr = qrcode.QRCode(box_size=3, border=2)
        qr.add_data(contenido)
        qr.make(fit=True)
        
        img_qr = qr.make_image(fill_color="black", back_color="white")
        foto = ImageTk.PhotoImage(img_qr)
        
        lbl_qr.config(image=foto)
        lbl_qr.image_ref = foto
        
    def mostrar_producto():
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # 1. Datos para el QR y Encabezado
            consulta_prod = "SELECT producto, linea, marca, caracteristica FROM producto WHERE Codigo = %s"
            cursor.execute(consulta_prod, (codigo_producto,))
            info_p = cursor.fetchone()
            
            if info_p:
                print(f"Datos encontrados: {info_p}")
                
                # Actualizar QR con datos reales (ajusta las llaves según tus columnas)
                datos_qr = {
                    'producto': info_p['producto'],
                    'linea': info_p['linea'],
                    'marca': info_p['marca'],
                    'detalle': info_p['caracteristica']
                }
                actualizar_qr_en_pantalla(datos_qr)
            else:
                messagebox.showinfo('Información',f"No se encontró el producto con código: {codigo_producto}")

            # 2. Saldo Total
            consulta_saldo = """
                SELECT p.producto, 
                (COALESCE(SUM(k.entrada), 0) - COALESCE(SUM(k.salida), 0)) AS cantidad
                FROM producto AS p 
                LEFT JOIN kardex AS k ON k.Codigo=p.Codigo 
                WHERE p.Codigo = %s GROUP BY p.producto, p.Codigo"""
            cursor.execute(consulta_saldo, (codigo_producto,))
            res_head = cursor.fetchone()
            
            if res_head:
                treeview_superior.delete(*treeview_superior.get_children())
                treeview_superior.insert('', 'end', values=(codigo_producto, res_head['producto'], res_head['cantidad']))

            # 3. Historial
            query_historial = """
                SELECT k.fecha, k.destino, k.id_movimiento, k.tipo_movimiento, 
                       k.concepto, k.cantidad
                FROM kardex k WHERE k.Codigo = %s ORDER BY k.fecha DESC"""
            cursor.execute(query_historial, (codigo_producto,))
            
            treeview_kardex.delete(*treeview_kardex.get_children())
            for fila in cursor.fetchall():
                treeview_kardex.insert('', 'end', values=(
                    fila['fecha'], fila['destino'], fila['id_movimiento'], 
                    fila['tipo_movimiento'], fila['concepto'], fila['cantidad']
                ))
                
            cursor.execute(consulta_prod, (codigo_producto,))
            info_p = cursor.fetchone()
            print(f"DEBUG - Datos del producto: {info_p}")
        finally:
            cursor.close()
    
    def al_seleccionar_movimiento(event):
        seleccion = treeview_kardex.selection()
        if not seleccion: return
        
        # Obtenemos los valores visibles en el treeview_kardex
        valores_fila = treeview_kardex.item(seleccion)['values']
        id_mov = valores_fila[2] # El ID del movimiento
        
        cursor = conexion.cursor(dictionary=True)
        # Traemos todos los datos necesarios para los Entrys y para el QR
        cursor.execute("""
            SELECT k.fecha, k.destino, k.id_movimiento, k.tipo_movimiento, 
                   k.concepto, k.usuario_seccion, k.origen, 
                   k.usuario_asignado, k.cantidad, k.observacion, p.producto, p.marca
            FROM kardex k
            INNER JOIN producto p ON k.Codigo = p.Codigo
            WHERE k.id_movimiento = %s""", (id_mov,))
        res = cursor.fetchone()
        
        if res:
            # --- Actualización de Entrys (Tu lógica actual) ---
            for widget, valor in [(ent_usuario, res['usuario_seccion']), 
                                (ent_origen, res['origen']), 
                                (ent_responsable, res['usuario_asignado']),
                                (ent_cantidad, res['cantidad'])]:
                widget.config(state='normal')
                widget.delete(0, 'end')
                widget.insert(0, str(valor) if valor else "")
                widget.config(state='readonly')
            
            txt_observacion.config(state='normal')
            txt_observacion.delete('1.0', 'end')
            txt_observacion.insert('1.0', res['observacion'] if res['observacion'] else "")
            txt_observacion.config(state='disabled')

            # --- NUEVO: Actualización dinámica del QR ---
            # Preparamos el diccionario con los campos exactos que pediste
            datos_para_qr = {
                'producto': res['producto'],
                'fecha': res['fecha'],
                'marca': res['marca'],
                'usuario_asignado': res['usuario_asignado'],
                'destino': res['destino'],
                'observacion': res['observacion']
            }
            actualizar_qr_en_pantalla(datos_para_qr)
            
        cursor.close()

    treeview_kardex.bind('<<TreeviewSelect>>', al_seleccionar_movimiento)

    # --- PROTOCOLO DE CIERRE SEGURO ---
    def cerrar_kardex():
        if conexion.is_connected():
            conexion.close()
            print("Conexión de Kardex cerrada.")
        v_kardex.destroy()

    v_kardex.protocol("WM_DELETE_WINDOW", cerrar_kardex)

    mostrar_producto()
    #v_kardex.mainloop()
    
#abrir_ventana_kardex()