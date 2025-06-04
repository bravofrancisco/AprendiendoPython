# ✨ Gestión de Clientes: Tu App Sencilla (Flask + SQL Server)

## 🚀 Descripción General

Esta es una aplicación web minimalista diseñada para la **administración eficiente de clientes**. Desarrollada con **Flask** en Python y utilizando **SQL Server** como base de datos, ofrece una solución ágil para gestionar tu información de clientes.

---

## 🌟 Funcionalidades Clave

* **Listado Intuitivo:** Visualiza de forma clara todos tus clientes activos.
* **Gestión Completa (CRUD):** Realiza operaciones de **C**reación, **L**ectura, **A**ctualización y **D**esactivación (Eliminación Lógica) de registros de clientes.
* **Eliminación Segura:** Los clientes son marcados como inactivos, preservando los datos para una posible recuperación futura.
* **Validación de Datos:** Asegura la consistencia y fiabilidad de la información ingresada.
* **Integración Robusta:** Conexión directa con tu instancia de SQL Server, compatible con la base de datos `Northwind`.

---

## 💻 Tecnologías Utilizadas

* **Backend:**
    * Python 3.x (con Flask y pyodbc)
    * SQL Server
* **Frontend:**
    * HTML, CSS, JavaScript
* **Control de Versiones:**
    * Git

---

## 🚀 Inicio Rápido

Para poner la aplicación en marcha, considera los siguientes puntos:

1.  **Requisitos:** Necesitarás Python 3.x instalado y una instancia de SQL Server con la base de datos `Northwind` (o una configurada a tu medida). Asegúrate de que SQL Server sea accesible desde tu entorno.
2.  **Preparación de la Base de Datos:** La tabla `Customers` debe contener una columna `IsActive` de tipo `BIT` con un valor predeterminado de `1`. Si ya tienes datos, verifica que estén marcados como activos en esta columna.
3.  **Configuración de la Aplicación:** Edita el archivo `app.py` para establecer la clave secreta de la aplicación y los detalles de conexión a tu servidor SQL.
4.  **Ejecución:** Una vez configurado, inicia la aplicación ejecutando el script principal desde tu terminal.

---

## 📂 Estructura del Proyecto

* `app.py`: Contiene la lógica central de la aplicación Flask.
* `templates/`: Directorio donde se almacenan los archivos HTML de la interfaz de usuario.

---

## 💡 Ideas para Futuras Mejoras

* Implementación de **paginación** para optimizar la visualización de grandes conjuntos de datos.
* Adición de **funcionalidad de búsqueda** para una recuperación de clientes más eficiente.
* Integración de un sistema de **autenticación de usuarios** para mayor seguridad y control de acceso.
* Refinamiento del **diseño visual** para una experiencia de usuario mejorada.

---