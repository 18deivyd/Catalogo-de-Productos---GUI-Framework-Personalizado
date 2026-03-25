🖥️ Catálogo de Productos - GUI Framework Personalizado

Este repositorio contiene una aplicación de escritorio para la gestión de catálogos de productos, construida sobre un framework personalizado desarrollado en Python. El proyecto destaca por el uso de componentes reutilizables y una arquitectura limpia.

🌟 Lo más destacado: "El Core Deivy.py"

La pieza central de este proyecto es el módulo Deivy.py, una librería de abstracción para Tkinter. En lugar de escribir cientos de líneas repetitivas, he creado clases que encapsulan la lógica de creación de:

    Ventanas Autocentradas: Cálculo automático de la posición según la resolución de pantalla.

    Botones con Gestión de Imágenes: Manejo automático de redimensión con PIL (Pillow) y prevención de recolección de basura (Garbage Collection) para las referencias de imagen.

    Componentes UI Estandarizados: Clases para Labels, Entrys, Textos y Combobox con estilos predefinidos (bordes, colores de resaltado y fuentes).

🚀 Funcionalidades del Catálogo

La interfaz principal (Catalogo.py) implementa un sistema de pestañas organizadas:

    Pestaña Producto: Información técnica, marcas, fabricantes y garantías.

    Pestaña Fiscal: Configuración de impuestos (I.V.A), retenciones e I.S.L.R.

    Pestaña Proveedor: Gestión de costos, historial de compras, stock crítico (Max/Min) y trazabilidad de proveedores.

🛠️ Herramientas Utilizadas

    Python 3.x: Lenguaje base.

    Tkinter & TTK: Para la interfaz gráfica y el manejo de widgets avanzados como Notebook.

    Pillow (PIL): Procesamiento y renderizado de iconos en alta calidad.

    Layout Management: Uso intensivo de Grid y Pack para una distribución precisa de elementos.

📂 Estructura del Código
Plaintext

├── Catalogo.py       # Lógica principal de la interfaz y distribución
├── Deivy.py          # Framework/Librería de componentes personalizados (POO)
└── Imagenes/         # Assets visuales para la barra de herramientas

⚙️ Cómo ejecutar

    Asegúrate de tener instalada la librería Pillow:
    Bash

    pip install Pillow

    Ejecuta el archivo principal:
    Bash

    python Catalogo.py

Desarrollado por Deivy Delgado Enfocado en crear soluciones de software escalables y herramientas de productividad eficientes.
