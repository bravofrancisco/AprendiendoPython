🚀 Aplicación de Gestión de Clientes (Flask + SQL Server)
📄 Descripción
Esta es una aplicación web sencilla para gestionar clientes. Fue construida con Flask (un framework de Python) y utiliza SQL Server como su base de datos. Te permite añadir, ver, editar y "eliminar" clientes, marcándolos como inactivos en lugar de borrarlos por completo.

✨ Características Principales
Listado de Clientes: Mira todos tus clientes activos de un vistazo.
Registrar Clientes: Añade nuevos clientes fácilmente a tu base de datos.
Editar Clientes: Actualiza la información de cualquier cliente existente.
Eliminación Lógica: Los clientes no se borran permanentemente; solo se marcan como inactivos, por si necesitas recuperarlos después.
Validaciones Básicas: La aplicación verifica que la información que ingresas sea correcta.
Conexión a SQL Server: Se conecta a tu base de datos Northwind (o la que configures).
💻 Tecnologías Utilizadas
Python 3.x: Lenguaje de programación principal.
Flask: Microframework web para Python.
SQL Server: Sistema de gestión de bases de datos relacionales.
HTML, CSS, JavaScript: Para la estructura y la interactividad de la interfaz de usuario en el navegador.
Git: Sistema de control de versiones para gestionar el código fuente.
pyodbc: Librería de Python para conectar con SQL Server.
🛠️ Cómo Ponerla en Marcha
Para que la aplicación funcione, necesitarás tener:

Python 3.x instalado.
Una instancia de SQL Server con la base de datos Northwind disponible.
Tu sistema de SQL Server debe permitir la conexión desde la aplicación.
Antes de ejecutar:

Asegúrate de que la tabla Customers en tu base de datos tenga una columna llamada IsActive de tipo booleano (BIT). Esta columna debe tener un valor predeterminado de 1. Si ya tienes clientes, verifica que estén marcados como activos en esta columna.
Deberás configurar la clave secreta de la aplicación y los detalles de conexión a tu SQL Server dentro del código de la aplicación.
Una vez que tengas todo eso listo, puedes ejecutar el archivo principal de la aplicación.

📂 Estructura Básica del Proyecto
app.py: Contiene toda la lógica principal de la aplicación Flask.
templates/: Aquí encontrarás los archivos HTML que definen la interfaz de usuario.
🚀 Ideas para el Futuro
Aquí hay algunas formas en que esta aplicación podría crecer:

Paginación: Mejorar la visualización para cuando tengas muchos clientes.
Búsqueda: Añadir una función de búsqueda para encontrar clientes más rápido.
Autenticación de Usuarios: Controlar quién puede acceder a la aplicación.
Mejoras Visuales: Darle un aspecto más moderno y fácil de usar.