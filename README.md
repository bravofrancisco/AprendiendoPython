🚀 Aplicación de Gestión de Clientes (Flask + SQL Server)
📄 Descripción General
Esta aplicación web facilita la gestión de clientes con operaciones CRUD (Crear, Leer, Actualizar, Eliminar). Desarrollada con Flask (Python) y SQL Server, ofrece una interfaz intuitiva para manejar tus datos de clientes de manera eficiente.

✨ Características Destacadas
Visibilidad Clara: Lista de clientes activos para una visión rápida.
Gestión Completa: Añade, edita y consulta la información de tus clientes.
Eliminación Segura: Los clientes se "desactivan" en lugar de borrarse permanentemente, permitiendo una recuperación futura.
Datos Confiables: Validaciones básicas en el formulario aseguran la integridad de la información.
Integración Sólida: Conexión directa a SQL Server, utilizando la base de datos Northwind (o la que especifiques).

💻 Tecnologías Clave
Backend:
Python 3.x: El núcleo de la aplicación.
Flask: Microframework web para la lógica del servidor.
SQL Server: Sistema de base de datos relacional.
pyodbc: Conector Python para SQL Server.
Frontend:
HTML, CSS, JavaScript: Para la interfaz de usuario en el navegador.
Control de Versiones:
Git: Para la gestión del código fuente.

🛠️ Cómo Iniciar
Para poner esta aplicación en funcionamiento, asegúrate de tener:

Python 3.x instalado.
Una instancia de SQL Server con la base de datos Northwind disponible y accesible para la aplicación.
Pasos Previos Necesarios:

Tu tabla Customers en SQL Server debe incluir una columna IsActive (tipo BIT) con un valor predeterminado de 1. Si ya tienes clientes, asegúrate de que estén marcados como activos en esta columna.
Dentro del código de la aplicación, configura la clave secreta de Flask y los detalles de conexión a tu SQL Server.
Una vez configurado, ejecuta el archivo principal de la aplicación para iniciar el servidor web.

📂 Organización del Proyecto
app.py: Contiene toda la lógica principal de la aplicación Flask.
templates/: Almacena los archivos HTML que construyen la interfaz de usuario.

🚀 Ideas para Mejoras Futuras
Optimización de Vistas: Implementar paginación para manejar grandes volúmenes de datos.
Funcionalidad de Búsqueda: Añadir filtros para encontrar clientes rápidamente.
Seguridad Mejorada: Integrar un sistema de autenticación de usuarios.
Experiencia de Usuario: Mejorar el diseño visual para una interfaz más pulida.