# Importa la clase Flask y otras funciones necesarias del framework Flask.
# Flask: La clase principal para crear la aplicación web.
# render_template: Para cargar y renderizar archivos HTML (plantillas).
# request: Para acceder a los datos enviados en las peticiones HTTP (como formularios).
# redirect: Para redirigir al usuario a otra URL.
# url_for: Para generar URLs para funciones específicas de tu aplicación.
# flash: Para mostrar mensajes temporales al usuario (mensajes "flash").
from flask import Flask, render_template, request, redirect, url_for, flash

# Importa el módulo pyodbc para conectarse y trabajar con bases de datos ODBC, como SQL Server.
import pyodbc

# Importa el módulo 're' para trabajar con expresiones regulares, que se usan para validación de texto.
import re 

# Crea una instancia de la aplicación Flask.
# __name__ es un parámetro estándar que ayuda a Flask a localizar recursos como plantillas y archivos estáticos.
app = Flask(__name__)

# Configura una clave secreta para la aplicación Flask.
# Es crucial para la seguridad de la sesión de usuario y los mensajes flash.
# ¡IMPORTANTE!: En un entorno de producción, esta clave debe ser una cadena aleatoria y compleja,
# y no debe estar directamente en el código fuente (por ejemplo, cargarse desde una variable de entorno).
app.secret_key = 'tu_clave_secreta_super_segura_y_aleatoria_1234567890' 

# Inicializa variables globales para la conexión y el cursor de la base de datos a None.
# Se usarán para almacenar la conexión y el cursor una vez establecidos.
connection = None
cursor = None

# Define una función para establecer una conexión con la base de datos SQL Server.
def get_db_connection():
    # Declara que 'connection' y 'cursor' son variables globales,
    # lo que permite a la función modificarlas en el ámbito global.
    global connection, cursor 
    try:
        # Intenta establecer una conexión a la base de datos Northwind usando pyodbc.
        # Se especifica el controlador (DRIVER), el servidor (SERVER), la base de datos (DATABASE)
        # y que se usará una conexión de confianza (Trusted_Connection=yes).
        connection = pyodbc.connect(r'DRIVER={SQL Server}; SERVER=FRANCISCOBRAVO\SQLEXPRESS;DATABASE=Northwind; Trusted_Connection=yes;')
        # Crea un objeto cursor a partir de la conexión.
        # El cursor se usa para ejecutar comandos SQL.
        cursor = connection.cursor()
        # Retorna la conexión y el cursor si la conexión es exitosa.
        return connection, cursor
    except Exception as ex:
        # Si ocurre un error durante la conexión, imprime el mensaje de error en la consola.
        print(f"Error al conectar a la base de datos: {ex}")
        # Restablece las variables globales de conexión y cursor a None.
        connection = None
        cursor = None
        # Retorna None, None para indicar que la conexión falló.
        return None, None

# Define la ruta principal de la aplicación ('/').
# Cuando un usuario visita la raíz del sitio web, se ejecuta esta función.
@app.route('/')
def index():
    # Inicializa una lista vacía para almacenar los datos de los clientes.
    clientes = []
    # Intenta obtener una conexión y un cursor a la base de datos.
    conn, curr = get_db_connection() 
    
    # Verifica si la conexión y el cursor se obtuvieron exitosamente.
    if conn and curr: 
        try:
            # Ejecuta una consulta SQL para seleccionar todos los clientes activos (IsActive = 1).
            # Los resultados se ordenan por CustomerID de forma descendente.
            curr.execute("SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers WHERE IsActive = 1 ORDER BY CustomerID DESC")
            # Recupera todos los resultados de la consulta. Cada fila es una tupla.
            clientes_raw = curr.fetchall()

            # Itera sobre cada fila de resultados obtenida de la base de datos.
            for row in clientes_raw:
                # Crea un diccionario para cada cliente, mapeando los valores de la fila a nombres de claves legibles.
                clientes.append({
                    "id": row[0],
                    "nombre_compania": row[1],
                    "nombre_contacto": row[2],
                    "direccion": row[3],
                    "ciudad": row[4],
                    "codigo_postal": row[5],
                    "pais": row[6]
                })

        except Exception as ex:
            # Si ocurre un error durante la consulta, imprime el error en la consola.
            print(f"Error al consultar la base de datos: {ex}")
            # Vacía la lista de clientes para asegurar que no se muestren datos incompletos o erróneos.
            clientes = []
            # Muestra un mensaje flash de error al usuario.
            flash(f"Error al cargar clientes: {ex}", "error")
        finally:
            # Asegura que el cursor se cierre si existe.
            if curr: curr.close()
            # Asegura que la conexión se cierre si existe.
            if conn: conn.close()
    else:
        # Si la conexión a la base de datos no se pudo establecer, muestra un mensaje de error.
        flash("No se pudo establecer conexión a la base de datos. Verifique la configuración.", "error")

    # Renderiza la plantilla 'index.html' y le pasa la lista de clientes para que se muestren en la página.
    return render_template('index.html', clientes=clientes)

# Define una ruta para registrar nuevos clientes.
# Solo acepta peticiones POST, ya que se están enviando datos de un formulario.
@app.route('/registrar_cliente', methods=['POST'])
def registrar_cliente():
    # Intenta obtener una conexión y un cursor a la base de datos.
    conn, curr = get_db_connection() 

    # Verifica si la conexión y el cursor se obtuvieron exitosamente.
    if conn and curr:
        try:
            # Recupera los datos del formulario enviado. .strip() elimina espacios en blanco al inicio y final.
            company_name = request.form['company_name'].strip()
            contact_name = request.form.get('contact_name', '').strip() # .get() es más seguro si el campo podría no existir.
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            country = request.form.get('country', '').strip()

            # --- VALIDACIÓN DE CAMPOS OBLIGATORIOS ---
            # Verifica si el campo 'Nombre de Compañía' está vacío.
            if not company_name:
                # Muestra un mensaje flash de error.
                flash("El campo 'Nombre de Compañía' es obligatorio.", "error")
                # Redirige al usuario de vuelta a la página principal.
                return redirect(url_for('index'))
            # Repite la validación para 'Nombre de Contacto'.
            if not contact_name:
                flash("El campo 'Nombre de Contacto' es obligatorio.", "error")
                return redirect(url_for('index'))
            # Repite la validación para 'Dirección'.
            if not address:
                flash("El campo 'Dirección' es obligatorio.", "error")
                return redirect(url_for('index'))
            # Repite la validación para 'Ciudad'.
            if not city:
                flash("El campo 'Ciudad' es obligatorio.", "error")
                return redirect(url_for('index'))
            # Valida que 'Código Postal' contenga solo dígitos.
            if not postal_code.isdigit():
                flash("El campo 'Código Postal' debe contener solo números.", "error")
                return redirect(url_for('index'))
            # Repite la validación para 'País'.
            if not country:
                flash("El campo 'País' es obligatorio.", "error")
                return redirect(url_for('index'))
            # --- NUEVA VALIDACIÓN MEJORADA: PAÍS SOLO LETRAS Y ESPACIOS ---
            # Usa una expresión regular con re.fullmatch() para asegurar que la cadena 'country'
            # solo contenga letras (mayúsculas o minúsculas) y espacios.
            # r'^[a-zA-Z\s]+$': ^ inicio de cadena, [a-zA-Z\s] permite letras o espacios, + una o más veces, $ fin de cadena.
            if not re.fullmatch(r'^[a-zA-Z\s]+$', country):
                flash("El campo 'País' debe contener solo letras y espacios.", "error")
                return redirect(url_for('index'))
            # --- FIN DE NUEVA VALIDACIÓN ---
            
            # Define la consulta SQL para insertar un nuevo cliente en la tabla Customers.
            sql = """
            INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            # Ejecuta la consulta SQL, pasando los datos del formulario como parámetros.
            # Esto ayuda a prevenir ataques de inyección SQL.
            curr.execute(sql, 
                         company_name, 
                         contact_name, 
                         address, 
                         city, 
                         postal_code, 
                         country)
            
            # Confirma los cambios en la base de datos (hace que la inserción sea permanente).
            conn.commit()
            # Muestra un mensaje flash de éxito al usuario.
            flash(f"Cliente '{company_name}' registrado exitosamente!", "success")
            
        # Captura errores específicos de integridad de la base de datos (ej. clave duplicada).
        except pyodbc.IntegrityError as e: 
            flash(f"Error de registro: Ocurrió un problema de integridad de datos. Posiblemente un valor duplicado no permitido.", "error")
            print(f"Error de integridad (registro): {e}")
        # Captura cualquier otra excepción general que pueda ocurrir.
        except Exception as ex:
            flash(f"Ocurrió un error inesperado al registrar el cliente: {ex}", "error")
            print(f"Error general al registrar: {ex}")
        finally:
            # Asegura que el cursor se cierre, si está abierto.
            if curr: curr.close()
            # Asegura que la conexión se cierre, si está abierta.
            if conn: conn.close()

    else:
        # Si la conexión a la base de datos no se pudo establecer, muestra un mensaje de error.
        flash("No se pudo establecer conexión a la base de datos para registrar.", "error")

    # Redirige al usuario a la página principal después de intentar registrar el cliente.
    return redirect(url_for('index')) 

# Define una ruta para eliminar clientes.
# Solo acepta peticiones POST, ya que se está realizando una acción de modificación de datos.
@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    # Obtiene el CustomerID del formulario.
    customer_id = request.form.get('customer_id')
    # Si no se proporciona un CustomerID, muestra un error y redirige.
    if not customer_id:
        flash("ID de cliente no proporcionado para la eliminación.", "error")
        return redirect(url_for('index'))

    # Intenta obtener una conexión y un cursor a la base de datos.
    conn, curr = get_db_connection()

    # Verifica si la conexión y el cursor se obtuvieron exitosamente.
    if conn and curr:
        try:
            # Define la consulta SQL para realizar una eliminación "lógica".
            # Esto significa que el registro no se borra de la tabla, solo se marca como inactivo (IsActive = 0).
            sql = "UPDATE Customers SET IsActive = 0 WHERE CustomerID = ?"
            # Ejecuta la consulta SQL con el CustomerID.
            curr.execute(sql, customer_id)
            # Confirma los cambios en la base de datos.
            conn.commit()
            # Muestra un mensaje flash de éxito.
            flash(f"Cliente (ID: {customer_id}) eliminado lógicamente.", "success")
        except Exception as ex:
            # Si ocurre un error, muestra un mensaje de error y lo imprime en consola.
            flash(f"Error al eliminar lógicamente el cliente: {ex}", "error")
            print(f"Error al eliminar lógicamente: {ex}")
        finally:
            # Asegura el cierre del cursor y la conexión.
            if curr: curr.close()
            if conn: conn.close()
    else:
        # Si no hay conexión a la base de datos, muestra un error.
        flash("No se pudo establecer conexión a la base de datos para la eliminación.", "error")

    # Redirige a la página principal.
    return redirect(url_for('index'))

# --- NUEVAS RUTAS PARA LA FUNCIONALIDAD DE EDITAR ---

# Define una ruta para mostrar el formulario de edición de un cliente.
# <int:customer_id> indica que esta parte de la URL es un número entero que será pasado como argumento.
@app.route('/editar_cliente/<int:customer_id>')
def editar_cliente_form(customer_id):
    # Inicializa la variable cliente a None.
    cliente = None
    # Intenta obtener una conexión y un cursor a la base de datos.
    conn, curr = get_db_connection()

    # Verifica si la conexión y el cursor se obtuvieron exitosamente.
    if conn and curr:
        try:
            # Busca el cliente por su CustomerID, asegurándose de que esté activo (IsActive = 1).
            curr.execute("SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers WHERE CustomerID = ? AND IsActive = 1", customer_id)
            # Recupera solo una fila de resultados (ya que CustomerID es único).
            row = curr.fetchone() 

            # Si se encuentra una fila, crea un diccionario con los datos del cliente.
            if row:
                cliente = {
                    "id": row[0],
                    "nombre_compania": row[1],
                    "nombre_contacto": row[2],
                    "direccion": row[3],
                    "ciudad": row[4],
                    "codigo_postal": row[5],
                    "pais": row[6]
                }
            else:
                # Si el cliente no se encuentra, muestra un mensaje de error.
                flash(f"Cliente con ID {customer_id} no encontrado o no activo.", "error")
        except Exception as ex:
            # Si ocurre un error durante la carga de datos, muestra un mensaje de error.
            flash(f"Error al cargar datos del cliente para editar: {ex}", "error")
            print(f"Error al buscar cliente para edición: {ex}")
        finally:
            # Asegura el cierre del cursor y la conexión.
            if curr: curr.close()
            if conn: conn.close()
    else:
        # Si no hay conexión a la base de datos, muestra un error.
        flash("No se pudo establecer conexión a la base de datos para cargar datos de edición.", "error")
    
    # Renderiza la plantilla 'editar_cliente.html' y le pasa los datos del cliente encontrado.
    return render_template('editar_cliente.html', cliente=cliente)

# Define una ruta para procesar las actualizaciones de clientes.
# Solo acepta peticiones POST, ya que se están enviando datos de un formulario de edición.
@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    # Inicializa 'customer_id' a None. Esto asegura que la variable siempre esté definida,
    # incluso si ocurre un error antes de que se le asigne un valor desde 'request.form'.
    customer_id = None 
    # Intenta obtener una conexión y un cursor a la base de datos.
    conn, curr = get_db_connection()

    # Verifica si la conexión y el cursor se obtuvieron exitosamente.
    if conn and curr:
        try:
            # Obtiene el ID del cliente del campo oculto del formulario.
            customer_id = request.form['customer_id'].strip()

            # Valida que el CustomerID haya sido proporcionado.
            if not customer_id:
                flash("ID de cliente no proporcionado para la actualización.", "error")
                # Redirige a la página principal si el ID falta.
                return redirect(url_for('index'))

            # Recupera los datos actualizados de los demás campos del formulario.
            company_name = request.form['company_name'].strip()
            contact_name = request.form.get('contact_name', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            country = request.form.get('country', '').strip()

            # --- VALIDACIÓN DE CAMPOS (similar a registrar, pero al fallar, redirige al formulario de edición) ---
            # Valida que el campo 'Nombre de Compañía' no esté vacío.
            if not company_name:
                flash("El campo 'Nombre de Compañía' es obligatorio.", "error")
                # Redirige de vuelta al formulario de edición si la validación falla.
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # Valida que el campo 'Nombre de Contacto' no esté vacío.
            if not contact_name:
                flash("El campo 'Nombre de Contacto' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # Valida que el campo 'Dirección' no esté vacío.
            if not address:
                flash("El campo 'Dirección' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # Valida que el campo 'Ciudad' no esté vacío.
            if not city:
                flash("El campo 'Ciudad' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # Valida que el campo 'Código Postal' solo contenga dígitos.
            if not postal_code.isdigit():
                flash("El campo 'Código Postal' debe contener solo números.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # Valida que el campo 'País' no esté vacío.
            if not country:
                flash("El campo 'País' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # --- NUEVA VALIDACIÓN MEJORADA: PAÍS SOLO LETRAS Y ESPACIOS ---
            # Usa una expresión regular con re.fullmatch() para asegurar que 'country'
            # solo contenga letras (mayúsculas o minúsculas) y espacios.
            if not re.fullmatch(r'^[a-zA-Z\s]+$', country):
                flash("El campo 'País' debe contener solo letras y espacios.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # --- FIN DE NUEVA VALIDACIÓN ---

            # Define la consulta SQL para actualizar los datos de un cliente existente.
            sql = """
            UPDATE Customers
            SET CustomerName = ?, ContactName = ?, Address = ?, City = ?, PostalCode = ?, Country = ?
            WHERE CustomerID = ? AND IsActive = 1
            """
            # Ejecuta la consulta SQL con los nuevos datos y el CustomerID para identificar el registro.
            curr.execute(sql, 
                         company_name, 
                         contact_name, 
                         address, 
                         city, 
                         postal_code, 
                         country,
                         customer_id)
            
            # Confirma los cambios en la base de datos.
            conn.commit()
            # Muestra un mensaje flash de éxito.
            flash(f"Cliente '{company_name}' (ID: {customer_id}) actualizado exitosamente!", "success")
            
        except Exception as ex:
            # Si ocurre un error inesperado durante la actualización, muestra un mensaje de error.
            flash(f"Ocurrió un error inesperado al actualizar el cliente: {ex}", "error")
            print(f"Error al actualizar cliente: {ex}")
            # Si 'customer_id' tiene un valor (es decir, se logró obtener del formulario),
            # redirige de vuelta al formulario de edición con el ID del cliente para que el usuario pueda corregir.
            if customer_id:
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
        finally:
            # Asegura el cierre del cursor y la conexión.
            if curr: curr.close()
            if conn: conn.close()

    else:
        # Si no se pudo establecer la conexión a la base de datos, muestra un error.
        flash("No se pudo establecer conexión a la base de datos para actualizar.", "error")

    # Redirige a la página principal después de intentar la actualización.
    return redirect(url_for('index'))

# Bloque estándar de Python para ejecutar el servidor Flask.
# Solo se ejecuta si el script se corre directamente (no si se importa como módulo).
if __name__ == '__main__':
    # Inicia el servidor Flask en modo de depuración (debug=True).
    # Esto permite recarga automática del código y muestra mensajes de error detallados en el navegador.
    # ¡IMPORTANTE!: No usar debug=True en producción por razones de seguridad y rendimiento.
    app.run(debug=True)