import tkinter as tk
from tkinter import ttk
import Deivy as D3

# Configuración de Ventana
configurar_ventana = D3.Ventana(500, 500)
mi_ventana = configurar_ventana.construir()
mi_ventana.title("Catálogo de Productos")
mi_ventana.resizable(0,0)

# Frame Superior (Barra de herramientas)
ventana_superior = tk.Frame(mi_ventana, 
                            bg='#B9FBC0', 
                            height=50)
ventana_superior.pack(side='top', fill='x')
ventana_superior.pack_propagate(False) # Importante para mantener los 50px

#Crear el contenedor de pestañas (Notebook)
notebook = ttk.Notebook(mi_ventana)
notebook.pack(expand=True, fill="both")

#Crear los marcos (Frames) para cada pestaña
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

#Añadir los marcos al notebook con un título
notebook.add(tab1, text="Producto")
notebook.add(tab2, text="Fiscal")
notebook.add(tab3, text="Proveedor")

# Frame Inferior
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

# Creación de Botones
try:
    obj_inicio = D3.Boton('Imagenes/Inicio', ventana_superior, None, 0, 0)
    inicio = obj_inicio.crear_boton(30, 30, 0, 0)
    
    obj_siguiente_izquierda = D3.Boton('Imagenes/Siguiente_izquierda', ventana_superior, None, 0, 0)
    siguiente_izquierda = obj_siguiente_izquierda.crear_boton(30, 30, 0, 1)
    
    obj_buscar = D3.Boton('Imagenes/Buscar', ventana_superior, None, 0, 0)
    buscar = obj_buscar.crear_boton(30,30, 0, 2)
    
    obj_siguiente_derecha = D3.Boton('Imagenes/Siguiente_derecha', ventana_superior, None, 0, 0)
    siguiente_derecha = obj_siguiente_derecha.crear_boton(30, 30, 0, 3)
    
    obj_final = D3.Boton('Imagenes/Final', ventana_superior, None, 0, 0)
    final = obj_final.crear_boton(30, 30, 0, 4)
    
    espacio_5 = tk.Label(ventana_superior,text='12', bg='#B9FBC0', foreground='#B9FBC0')
    espacio_5.grid(row=0, column=5, padx=0, pady=0, sticky='nsew')
    
    obj_nuevo = D3.Boton('Imagenes/Nuevo', ventana_superior, None, 0, 0)
    nuevo = obj_nuevo.crear_boton(30, 30, 0, 6)
    
    obj_guardar = D3.Boton('Imagenes/Guardar', ventana_superior, None, 0, 0)
    guardar = obj_guardar.crear_boton(30, 30, 0, 7)
    
    obj_salir = D3.Boton('Imagenes/Salir', ventana_superior,None, 0, 0)
    salir = obj_salir.crear_boton(30, 30, 0, 8)
    
    espacio_9 = tk.Label(ventana_superior,text='12', bg='#B9FBC0', foreground='#B9FBC0')
    espacio_9.grid(row=0, column=9, padx=0, pady=0, sticky='nsew')
    
    obj_imprimir = D3.Boton('Imagenes/Imprimir', ventana_superior, None, 0, 0)
    imprimir = obj_imprimir.crear_boton(30, 30, 0, 10)

    obj_recargar = D3.Boton('Imagenes/Recargar', ventana_superior, None, 0, 0)
    recargar = obj_recargar.crear_boton(30, 30, 0, 11)
    
    espacio_12 = tk.Label(ventana_superior,text='123456789101112', bg='#B9FBC0', foreground='#B9FBC0')
    espacio_12.grid(row=0, column=12, padx=0, pady=0, sticky='nsew')
    
    obj_licencia = D3.Boton('Imagenes/Licencia', ventana_superior, None, 0, 0)
    licencia = obj_licencia.crear_boton(30, 30, 0, 13)
    
    obj_exportar = D3.Boton('Imagenes/Exportar', ventana_superior, None, 0, 0)
    exportar = obj_exportar.crear_boton(30, 30, 0, 14)
    
except Exception as e:
    print(f"Error en Catalogo.py: {e}")
    
# 5. Creación de Labels

    #Codigo
label_cod = D3.Labels(ventana_tab1, 'Código:', 0, 0,'e')
codigo = label_cod.crear_label()

entry_cod = D3.Entrys(ventana_tab1, 40, 'disabled',0, 1, 'w', None, None)
entry_1 = entry_cod.crear_entry()

    #Codigo de barra
label_cod_barra = D3.Labels(ventana_tab1, 'Código de Barra:', 1, 0,'e')
codigo_barra = label_cod_barra.crear_label()

entry_cod_barra = D3.Entrys(ventana_tab1, 40, 'normal',1, 1, 'w', None, None)
entry_2 = entry_cod_barra.crear_entry()

    #Producto
label_producto = D3.Labels(ventana_tab1, 'Producto:', 2, 0,'e')
producto = label_producto.crear_label()

entry_producto = D3.Entrys(ventana_tab1, 40, 'normal', 2, 1, 'w', None, None)
entry_3 = entry_producto.crear_entry()

    #Departamento
label_departamento = D3.Labels(ventana_tab1, 'Departamento:', 3, 0,'e')
departamento = label_departamento.crear_label()

entry_departamento = D3.Entrys(ventana_tab1, 40, 'normal', 3, 1, 'w', None, None)
entry_4 = entry_departamento.crear_entry()

    #Linea
label_linea = D3.Labels(ventana_tab1, 'Línea:', 4, 0,'e')
linea = label_linea.crear_label()

entry_linea = D3.Entrys(ventana_tab1, 40, 'normal', 4, 1, 'w', None, None)
entry_5 = entry_linea.crear_entry()

    #Fabricante
label_fabricante = D3.Labels(ventana_tab1, 'Fabricante:', 5, 0,'e')
fabricante = label_fabricante.crear_label()

entry_fabricante = D3.Entrys(ventana_tab1, 40, 'normal', 5, 1, 'w', None, None)
entry_6 = entry_fabricante.crear_entry()

    #Marca
label_marca = D3.Labels(ventana_tab1, 'Marca:', 6, 0,'e')
marca = label_marca.crear_label()

entry_marca = D3.Entrys(ventana_tab1, 40, 'normal', 6, 1, 'w', None, None)
entry_7 = entry_marca.crear_entry()

    #Dia de garantias para el cliente
label_dias_garantia = D3.Labels(ventana_tab1, 'Días de Garantía:', 7, 0,'e')
dias_garantia = label_dias_garantia.crear_label()

entry_dias_garantia = D3.Entrys(ventana_tab1, 40, 'normal', 7, 1, 'w', None, None)
entry_dias_garantia_1 = entry_dias_garantia.crear_entry()

    #Caracteristica
label_caracteristica = D3.Labels(ventana_tab1, 'Característica:', 8, 0,'ne', None, 3)
caracteristica = label_caracteristica.crear_label()

texto_caracteristica = D3.Textos(ventana_tab1, 40, 5, 8, 1, 'w')
texto_1 = texto_caracteristica.crear_text()

#Frame Fiscal
ventana_tab2 = tk.Frame(tab2,
                        bg='#E2E2E2')
ventana_tab2.pack(fill='both', expand=True)

for i in range(10):
    ventana_tab2.rowconfigure(i, weight=1)
    
for i in range(4):
    ventana_tab2.columnconfigure(i, weight=1)
    
    #I.V.A
label_iva = D3.Labels(ventana_tab2, 'I.V.A', 0, 0,'e')
iva = label_iva.crear_label()

combobox_iva = D3.Combobox(ventana_tab2, ['0%', '8%', '16%', '24%'], 0, 1, sticky='w')
crear_iva = combobox_iva.crear_combobox()

    #Prorrata
label_prorrata = D3.Labels(ventana_tab2, 'Prorrata', 0, 2,'e')
prorrata = label_prorrata.crear_label()

combobox_prorrata = D3.Combobox(ventana_tab2, ['No aplica', 'Aplica','Deducible'], 0, 3, sticky='w')
crear_prorrata = combobox_prorrata.crear_combobox()

    #Otro
label_otro = D3.Labels(ventana_tab2, 'Otro', 1, 0,'e')
otro = label_otro.crear_label()

combobox_otro = D3.Combobox(ventana_tab2, ['0%', '8%', '16%', '24%'], 1, 1, sticky='w')
crear_otro = combobox_otro.crear_combobox()

    #Retención I.V.A:
label_retención_iva = D3.Labels(ventana_tab2, 'Retención I.V.A:', 1, 2,'e')
retención_iva = label_retención_iva.crear_label()

combobox_retención_iva = D3.Combobox(ventana_tab2, ['0%', '75%', '100%'], 1, 3, sticky='w')
crear_retención_iva = combobox_retención_iva.crear_combobox()

    #Otro
label_otro_1 = D3.Labels(ventana_tab2, 'Otro', 2, 0,'e')
otro_1 = label_otro_1.crear_label()

combobox_otro_1 = D3.Combobox(ventana_tab2, ['0%', '8%', '16%', '24%'], 2, 1, 'w')
crear_otro_1 = combobox_otro_1.crear_combobox()

    #Retención I.S.L.R:
label_islr = D3.Labels(ventana_tab2, 'Retención I.S.L.R:', 3, 0,'w', 2, None)
islr = label_islr.crear_label()

entry_islr = D3.Entrys(ventana_tab2, 6, 'normal', 3, 1, 'e')
entry_8 = entry_islr.crear_entry()

entry_islr_1 = D3.Entrys(ventana_tab2, 35, 'normal', 3, 2, 'w',None, 2)
entry_9 = entry_islr_1.crear_entry()

boton_buscar_islr = D3.Boton('Imagenes/Buscar', ventana_tab2,None,0,0)
buscar_islr = boton_buscar_islr.crear_boton(30,30,3,3, 'e','#E2E2E2')

#Frame Proveedor
ventana_tab3 = tk.Frame(tab3, bg='#E2E2E2')
ventana_tab3.pack(expand=True, fill='both')

for i in range(10):
    ventana_tab3.rowconfigure(i, weight=1)
    
for i in range(4):
    ventana_tab3.columnconfigure(i, weight=1)

    #Ultimo costo
lbl_ultimo_costo = D3.Labels(ventana_tab3,'Ultimo Costo:', 0, 0, 'e')
ultimo_costo = lbl_ultimo_costo.crear_label() 

entry_ultimo_costo = D3.Entrys(ventana_tab3, 6, 'disable', 0, 1, 'w')
entry_10 = entry_ultimo_costo.crear_entry()

    #Costo Anterior
lbl_costo_anterior = D3.Labels(ventana_tab3,'Costo Anterior:', 0, 2, 'e')
costo_anterior = lbl_costo_anterior.crear_label() 

entry_costo_anterior = D3.Entrys(ventana_tab3, 4, 'disable', 0, 3, 'w')
entry_11 = entry_costo_anterior.crear_entry()

    #Fecha de Compra
lbl_fecha_compra = D3.Labels(ventana_tab3,'Fecha de Compra:', 1, 0, 'e')
fecha_compra = lbl_fecha_compra.crear_label() 

entry_fecha_compra = D3.Entrys(ventana_tab3, 12, 'disable', 1, 1, 'w')
entry_12 = entry_fecha_compra.crear_entry()

    #Stock
lbl_stock = D3.Labels(ventana_tab3,'Cantidad Actual:', 1, 2, 'e')
stock = lbl_stock.crear_label() 

entry_stock = D3.Entrys(ventana_tab3, 4, 'disable', 1, 3, 'w')
entry_13 = entry_stock.crear_entry()

    #Existencia max
lbl_existencia_max = D3.Labels(ventana_tab3,'Existencia Maxima:', 2, 0, 'e')
existencia_max = lbl_existencia_max.crear_label() 

entry_existencia_max = D3.Entrys(ventana_tab3, 4, 'normal', 2, 1, 'w')
entry_14 = entry_existencia_max.crear_entry()

    #Existencia min
lbl_existencia_min = D3.Labels(ventana_tab3,'Existencia Minima:', 2, 2, 'e')
existencia_min = lbl_existencia_min.crear_label() 

entry_existencia_min = D3.Entrys(ventana_tab3, 4, 'normal', 2, 3, 'w')
entry_15 = entry_existencia_min.crear_entry()

    #Proveedor
lbl_proveedor = D3.Labels(ventana_tab3,'Proveedor #1:', 3, 0, 'e')
proveedor = lbl_proveedor.crear_label() 

entry_proveedor = D3.Entrys(ventana_tab3, 40, 'normal', 3, 1, 'we', None, 3)
entry_16 = entry_proveedor.crear_entry()

    #Proveedor
lbl_proveedor = D3.Labels(ventana_tab3,'Proveedor #2:', 4, 0, 'we')
proveedor = lbl_proveedor.crear_label() 

entry_proveedor1 = D3.Entrys(ventana_tab3, 40, 'normal', 4, 1, 'we', None, 3)
entry_17 = entry_proveedor1.crear_entry()

    #Proveedor
lbl_proveedor = D3.Labels(ventana_tab3,'Proveedor #3:', 5, 0, 'we')
proveedor = lbl_proveedor.crear_label() 

entry_proveedor2 = D3.Entrys(ventana_tab3, 40, 'normal', 5, 1, 'we', None, 3)
entry_18 = entry_proveedor2.crear_entry()




mi_ventana.mainloop()