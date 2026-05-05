# 📦 InventoryMaster GUI - Catalogo de Productos

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-green.svg)

**InventoryMaster** es una aplicación de escritorio profesional desarrollada en Python para la gestión de inventarios. El sistema permite administrar un catálogo de productos, visualizar movimientos de Kardex y consultar información detallada de marcas y usuarios mediante una conexión robusta a una base de datos MySQL.

---

## ✨ Características Principales

*   **Interfaz Dinámica**: Uso de `ttk.Treeview` para mostrar el inventario con actualización en tiempo real.
*   **Consultas Relacionales**: Extracción de datos específicos (marcas, observaciones) vinculados a cada producto.
*   **Optimización de Consultas**: Implementación de cursores con búfer (`buffered=True`) para evitar bloqueos de resultados no leídos.
*   **Gestión de Eventos**: Uso de `<<TreeviewSelect>>` para mostrar detalles automáticos al hacer clic en un registro.
*   **Diseño Modular**: Organización estética mediante Frames para separar la búsqueda, la tabla y los formularios de edición.

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje:** [Python 3.14+](https://www.python.org/)
*   **Interfaz Gráfica:** Tkinter / TTK
*   **Conector de BD:** `mysql-connector-python`
*   **Base de Datos:** MySQL (compatible con Laragon y MySQL Workbench)

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/18deivyd/Catalogo-de-Productos---GUI-Framework-Personalizado.git](https://github.com/18deivyd/Catalogo-de-Productos---GUI-Framework-Personalizado.git)
cd Catalogo-de-Productos---GUI-Framework-Personalizado

Desarrollado por: Deivy Delgado
Proyecto enfocado en la arquitectura de software y gestión de bases de datos relacionales.
