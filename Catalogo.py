import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import Deivy
import os
import Database

def abrir_ventana_catalogo():
        #Conexion base de dato
    conexion = Database.conectar_db()
    
    def guardar_producto():
        try:
            cursor = conexion.cursor()
            
            def limpiar_p(valor):
                return float(valor.replace('%', '').strip()) if valor else 0.0

            # 1. RECOLECCIÓN DE DATOS (Asegúrate de que el orden sea igual al INSERT)
            datos = (
                self_entries['Código de Barra'].get(),
                self_entries['Producto'].get(),
                self_entries['Departamento'].get(),
                self_entries['Línea'].get(),
                self_entries['Fabricante'].get(),
                self_entries['Marca'].get(),
                self_entries['Días de Garantía'].get() or 0,
                texto_1.get("1.0", tk.END).strip(),
                limpiar_p(crear_iva_compra.get()),
                limpiar_p(crear_iva_venta.get()),
                entry_15.get() or 0,
                entry_14.get() or 0,
                combobox_pc.get(),
                entry_18.get(),  # Proveedor 1
                entry_19.get(),  # Proveedor 2
                entry_20.get()   # Proveedor 3
            )

            # 2. CONSULTA SQL (He contado 16 columnas y 16 marcadores %s)
            # Asegúrate de que los nombres de las columnas coincidan con tu MariaDB
            consulta = """INSERT INTO producto (
                            codigo_barra, producto, departamento, linea, 
                            fabricante, marca, dias_de_garantia, caracteristica, 
                            iva_compra, iva_venta, existencia_minima, existencia_maxima, 
                            presentacion_compra, provedor_1, provedor_2, provedor_3
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(consulta, datos)
            conexion.commit()

            for entry in self_entries.values():
                # Limpiar los Entrys
                estado_original = entry.cget('state')
                entry.config(state='normal')
                entry.delete(0, 'end')
                entry.config(state=estado_original)
                
            texto_1.delete('1.0', 'end')
            
            crear_iva_compra.set('0%')
            crear_iva_venta.set('0%')
            crear_retención_iva.set('0%')
            combobox_pc.set('Unidad')
            
            entry_18.delete(0, 'end')
            entry_19.delete(0, 'end')
            entry_20.delete(0, 'end')
            entry_14.delete(0, 'end')
            entry_15.delete(0, 'end')
            
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            
        except Exception as e:
            conexion.rollback()
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
    
    def limpiar_formulario():
        for entry in self_entries.values():
                # Limpiar todos los Entrys 
            estado_original = entry.cget('state')
            entry.config(state='normal')
            entry.delete(0, 'end')
            entry.config(state=estado_original)
            
            # Limpiar el cuadro de texto de características
        texto_1.delete('1.0', 'end')
        
            # Resetear Comboboxes a sus valores iniciales
        crear_iva_compra.set('0%')
        crear_iva_venta.set('0%')
        crear_retención_iva.set('0%')
        combobox_pc.set('Unidad')
        
            # Limpiar proveedores
        entry_18.delete(0, 'end')
        entry_19.delete(0, 'end')
        entry_20.delete(0, 'end')
        
        entry_14.delete(0, 'end')
        entry_15.delete(0, 'end')
        
        messagebox.showinfo("Limpiar", "Formulario listo para nuevo registro")
        
        # Configuración de Ventana
    configurar_ventana = Deivy.Ventana(600, 500, 'Registro y Modificación de Catálogo de Productos')
    v_catalogo = configurar_ventana.construir()
    v_catalogo.resizable(0,0)
    v_catalogo.grab_set()
    v_catalogo.focus_set()
    v_catalogo.referencias = []


        # Frame Superior (Barra de herramientas)
    ventana_superior = tk.Frame(v_catalogo, 
                                bg='#0f9fcf', 
                                height=50)
    ventana_superior.pack(side='top', fill='x')
    ventana_superior.pack_propagate(False) # Importante para mantener los 50px

        #Contenedor de pestañas (Notebook)
    notebook = ttk.Notebook(v_catalogo)
    notebook.pack(expand=True, fill="both")

        #Crear los marcos (Frames)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

        #Añadir los marcos al notebook con un título
    notebook.add(tab1, text="Producto")
    notebook.add(tab2, text="Fiscal")
    notebook.add(tab3, text="Proveedor")

        # Pestaña Producto
    ventana_tab1 = tk.Frame(tab1,
                            bg='#E2E2E2')
    ventana_tab1.pack(fill='both', expand=True)

        # Configuración de Rejilla (Grid)
    ventana_superior.rowconfigure(0, weight=1)
    for i in range(14):
        ventana_superior.columnconfigure(i, weight=1)
        
    for i in range(10):
        ventana_tab1.rowconfigure(i, weight=1)
        
    ventana_tab1.columnconfigure(0, weight=1)
    ventana_tab1.columnconfigure(1, weight=1)


    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_imgs = os.path.join(base_path, 'Imagenes')
    
    print(f"Buscando imágenes en: {folder_imgs}")

    try:
        # Diccionario para iterar y no repetir código (opcional, pero más seguro)
        #iconos = [('Inicio.png', 0, None), ('Siguiente_izquierda.png', 1, None), ('Buscar.png', 2, None),('Siguiente_derecha.png', 3, None), ('Final.png', 4, None), ('Nuevo.png', 6, limpiar_formulario),('Guardar.png', 7, guardar_producto), ('Salir.png', 8, None), ('Imprimir.png', 10, None),('Recargar.png', 11, None), ('Licencia.png', 13, None), ('Exportar.png', 14, None)]
        
        iconos = [('Nuevo.png', 0, limpiar_formulario),('Guardar.png', 1, guardar_producto)]

        for nombre_arc, col, comando in iconos:
            ruta = os.path.join(folder_imgs, nombre_arc)
            # Pasamos v_catalogo para que la referencia se guarde ahí
            obj_btn = Deivy.Boton(ruta, ventana_superior, comando, 0, 0)
            btn = obj_btn.crear_boton(30, 30, 0, col)
            v_catalogo.referencias.append(obj_btn) # Mantener vivo el objeto
            
    except Exception as e:
        print(f"Error cargando iconos: {e}")


        # Creación de Labels y Entrys
    lbl_producto = [
        ('Código:', 0, 0,'disabled'), ('Código de Barra:', 1, 0, 'normal'), ('Producto:', 2, 0, 'normal'), ('Departamento:', 3, 0, 'normal'), ('Línea:', 4, 0,'normal'), ('Fabricante:', 5, 0, 'normal'), ('Marca:', 6, 0, 'normal'), ('Días de Garantía:', 7, 0, 'normal')
    ]

    self_entries = {}

    for texto, fila, columna, estado in lbl_producto:
        lbl = Deivy.Labels(ventana_tab1, texto, fila, columna, 'e').crear_label()
        ent_obj = Deivy.Entrys(ventana_tab1, 40, estado, fila, columna + 1, 'w', 1, 1)
        entry_widget = ent_obj.crear_entry()

        self_entries[texto.replace(':', '')] = entry_widget

        #Caracteristica
    label_caracteristica = Deivy.Labels(ventana_tab1, 'Característica:', 8, 0,'ne', None, 3)
    caracteristica = label_caracteristica.crear_label()

    texto_caracteristica = Deivy.Textos(ventana_tab1, 40, 5, 8, 1, 'w')
    texto_1 = texto_caracteristica.crear_text()

        #Pestaña Fiscal
    ventana_tab2 = tk.Frame(tab2,
                            bg='#E2E2E2')
    ventana_tab2.pack(fill='both', expand=True)

    for i in range(10):
        ventana_tab2.rowconfigure(i, weight=1)
        
    for i in range(4):
        ventana_tab2.columnconfigure(i, weight=1)
        
    opciones_iva = ['0%', '8%', '16%', '24%']
    
        #I.V.A Compra
    label_iva_compra = Deivy.Labels(ventana_tab2, 'IVA Compra:', 0, 0,'e')
    iva_compra = label_iva_compra.crear_label()

    combobox_iva_compra = Deivy.Combobox(ventana_tab2, opciones_iva, 0, 1, sticky='w')
    crear_iva_compra = combobox_iva_compra.crear_combobox()

        #I.V.A Venta
    label_iva_venta = Deivy.Labels(ventana_tab2, 'IVA Venta:', 0, 2,'e')
    iva_venta = label_iva_venta.crear_label()

    combobox_iva_venta = Deivy.Combobox(ventana_tab2, opciones_iva, 0, 3, sticky='w')
    crear_iva_venta = combobox_iva_venta.crear_combobox()

        #Otro
    label_otro = Deivy.Labels(ventana_tab2, 'Otro:', 1, 0,'e')
    otro = label_otro.crear_label()

    combobox_otro = Deivy.Combobox(ventana_tab2, opciones_iva, 1, 1, sticky='w')
    crear_otro = combobox_otro.crear_combobox()

        #Retención I.V.A:
    label_retención_iva = Deivy.Labels(ventana_tab2, 'Retención IVA:', 1, 2,'e')
    retención_iva = label_retención_iva.crear_label()

    combobox_retención_iva = Deivy.Combobox(ventana_tab2, ['0%', '75%', '100%'], 1, 3, sticky='w')
    crear_retención_iva = combobox_retención_iva.crear_combobox()

        #Otro
    label_otro_1 = Deivy.Labels(ventana_tab2, 'Otro:', 2, 0,'e')
    otro_1 = label_otro_1.crear_label()

    combobox_otro_1 = Deivy.Combobox(ventana_tab2, ['0%', '8%', '16%', '24%'], 2, 1, sticky='w')
    crear_otro_1 = combobox_otro_1.crear_combobox()

        #Prorrata
    label_prorrata = Deivy.Labels(ventana_tab2, 'Prorrata:', 2, 2,'e')
    prorrata = label_prorrata.crear_label()

    combobox_prorrata = Deivy.Combobox(ventana_tab2, ['No aplica', 'Aplica','Deducible'], 2, 3, sticky='w')
    crear_prorrata = combobox_prorrata.crear_combobox()

        #Grupo
    label_grupo = Deivy.Labels(ventana_tab2, 'Grupo:', 3, 0,'e')
    grupo = label_grupo.crear_label()

    combobox_grupo = Deivy.Combobox(ventana_tab2, ['Producto Terminado', 'Materia Prima','Consumible', 'Empaque', 'Herramientas', 'Producto en Proceso', 'Repuesto', 'Limpieza','Suministro'], 3, 1, sticky='w', width=18)
    crear_grupo = combobox_grupo.crear_combobox()

        #Retención I.S.L.R:
    label_islr = Deivy.Labels(ventana_tab2, 'Retención I.S.L.R:', 4, 0,'e', 1, None)
    islr = label_islr.crear_label()

    entry_islr = Deivy.Entrys(ventana_tab2, 15, 'normal', 4, 1, 'e')
    entry_8 = entry_islr.crear_entry()

    entry_islr_1 = Deivy.Entrys(ventana_tab2, 30, 'normal', 4, 2, 'w',columnspan=2)
    entry_9 = entry_islr_1.crear_entry()

    path_buscar_general = os.path.join(base_path, 'Imagenes', 'Buscar.png')
    boton_buscar_islr = Deivy.Boton(path_buscar_general, ventana_tab2, None, 0, 0)
    buscar_islr = boton_buscar_islr.crear_boton(30, 30, 4, 3, 'e','#E2E2E2')
    v_catalogo.referencias.append(boton_buscar_islr)

        #Pestaña Proveedor
    ventana_tab3 = tk.Frame(tab3, bg='#E2E2E2')
    ventana_tab3.pack(expand=True, fill='both')

    for i in range(10):
        ventana_tab3.rowconfigure(i, weight=1)
        
    for i in range(4):
        ventana_tab3.columnconfigure(i, weight=1)

    campos_prov = [
        ('Ultimo Costo:', 0, 0), ('Costo Anterior:', 0, 2),
        ('Fecha Compra:', 1, 0), ('Cantidad Actual:', 1, 2)
    ]
    for txt, f, c in campos_prov:
        lbl = Deivy.Labels(ventana_tab3, txt, f, c, 'e')
        label = lbl.crear_label()
        ent = Deivy.Entrys(ventana_tab3, 10, 'disabled', f, c+1, 'w')
        entry = ent.crear_entry()

        #Existencia min
    lbl_existencia_min = Deivy.Labels(ventana_tab3,'Existencia Minima:', 2, 0, 'e')
    existencia_min = lbl_existencia_min.crear_label() 

    entry_existencia_min = Deivy.Entrys(ventana_tab3, 4, 'normal', 2, 1, 'w')
    entry_15 = entry_existencia_min.crear_entry()

        #Existencia max
    lbl_existencia_max = Deivy.Labels(ventana_tab3,'Existencia Maxima:', 2, 2, 'e')
    existencia_max = lbl_existencia_max.crear_label() 

    entry_existencia_max = Deivy.Entrys(ventana_tab3, 4, 'normal', 2, 3, 'w')
    entry_14 = entry_existencia_max.crear_entry()

        #Presentacion de Compra
    lbl_presentacion_compra = Deivy.Labels(ventana_tab3,'Presentacion Compra:', 3, 0, 'e')
    presentacion_compra = lbl_presentacion_compra.crear_label() 

    combobox_presentacion_compra = Deivy.Combobox(ventana_tab3, ['Unidad', 'Par', 'Docena', 'Blíster', 'Caja', 'Six-pack', 'Mililitro', 'Centilitro', 'Litro', 'Metro cúbico', 'Galón', 'Gramo', 'Kilogramo', 'Tonelada', 'Centímetro cúbico', 'Metro cúbico', 'Balde', 'Carretilla', 'Palada', 'Bolsa/Saco'], 3, 1, 'w',20)

    combobox_pc = combobox_presentacion_compra.crear_combobox()
        
        #Presentacion de Venta
    lbl_presentacion_venta = Deivy.Labels(ventana_tab3,'Presentacion Venta:', 4, 0, 'e')
    presentacion_venta = lbl_presentacion_venta.crear_label() 

    combobox_presentacion_venta = Deivy.Combobox(ventana_tab3, ['Unidad', 'Par', 'Docena', 'Blíster', 'Caja', 'Six-pack', 'Mililitro', 'Centilitro', 'Litro', 'Metro cúbico', 'Galón', 'Gramo', 'Kilogramo', 'Tonelada', 'Centímetro cúbico', 'Metro cúbico', 'Balde', 'Carretilla', 'Palada', 'Bolsa/Saco'], 4, 1, 'w',20)

    combobox_pv = combobox_presentacion_venta.crear_combobox()

        #Proveedor_1
    lbl_proveedor = Deivy.Labels(ventana_tab3,'Proveedor #1:', 5, 0, 'e')
    proveedor = lbl_proveedor.crear_label() 

    entry_proveedor = Deivy.Entrys(ventana_tab3, 40, 'normal', 5, 1, 'w', None, 3)
    entry_18 = entry_proveedor.crear_entry()

        #Proveedor_2
    lbl_proveedor = Deivy.Labels(ventana_tab3,'Proveedor #2:', 6, 0, 'e')
    proveedor = lbl_proveedor.crear_label() 

    entry_proveedor1 = Deivy.Entrys(ventana_tab3, 40, 'normal', 6, 1, 'w', None, 3)
    entry_19 = entry_proveedor1.crear_entry()

        #Proveedor_3
    lbl_proveedor = Deivy.Labels(ventana_tab3,'Proveedor #3:', 7, 0, 'e')
    proveedor = lbl_proveedor.crear_label() 

    entry_proveedor2 = Deivy.Entrys(ventana_tab3, 40, 'normal', 7, 1, 'w', None, 3)
    entry_20 = entry_proveedor2.crear_entry()
    
    #v_catalogo.mainloop()
    
#abrir_ventana_catalogo()


  
