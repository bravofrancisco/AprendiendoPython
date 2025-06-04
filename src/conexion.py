import pyodbc

# Inicializa connection y cursor a None
connection = None
cursor = None

try:
    # CADENA DE CONEXIÓN CORREGIDA: Usando la misma que ya te funcionó
    # Asegúrate de que esta línea esté idéntica a la que te funcionó para conectar
    connection = pyodbc.connect(r'DRIVER={SQL Server}; SERVER=FRANCISCOBRAVO\SQLEXPRESS;DATABASE=Northwind; Trusted_Connection=yes;')
    
    print("Conexión exitosa a la base de datos Northwind.")

    # Crear un objeto cursor a partir de la conexión
    cursor = connection.cursor()

    # --- PASO 1: Listar datos de una tabla (ej. Customers) ---
    print("\n--- Listando los primeros 10 clientes de la tabla 'Customers' ---")
    
    # Ejecutar una consulta SELECT
    # Puedes cambiar 'Customers' por el nombre de la tabla que quieras listar
    # LIMIT 10 (en otros SQL) o TOP 10 (en SQL Server) para no traer todos los datos
    # si la tabla es muy grande, lo que es una buena práctica.
    cursor.execute("SELECT  CustomerID, ContactName, Address, City, PostalCode, Country FROM Customers")
    
    # Recuperar todos los resultados
    # fetchall() obtiene todas las filas
    # fetchone() obtiene una fila
    # fetchmany(size) obtiene un número específico de filas
    rows = cursor.fetchall()

    # Mostrar las cabeceras de las columnas (opcional pero útil)
    # Las descripciones de las columnas están disponibles en cursor.description
    if cursor.description:
        column_names = [column[0] for column in cursor.description]
        print(f"Columnas: {', '.join(column_names)}")
        print("-" * 50) # Línea separadora

    # Iterar sobre los resultados e imprimirlos
    if rows:
        for row in rows:
            print(row) # Cada 'row' es una tupla con los valores de las columnas
    else:
        print("No se encontraron clientes.")

    # --- Opcional: Mostrar la versión del SQL Server como antes ---
    print("\n--- Verificando la versión del SQL Server ---")
    cursor.execute("SELECT @@VERSION");
    sql_version_row = cursor.fetchone()
    if sql_version_row:
        print (f"Versión de SQL Server: {sql_version_row[0]}")
    else:
        print("No se pudo obtener la versión de SQL Server.")


except Exception as ex:
    print(f"Ocurrió un error: {ex}")

finally:
    # Es una buena práctica cerrar la conexión y el cursor
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("\nConexión y cursor cerrados (si estaban abiertos).")