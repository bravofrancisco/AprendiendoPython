from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import re # ¡IMPORTA EL MÓDULO 're'!

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura_y_aleatoria_1234567890' 

connection = None
cursor = None

def get_db_connection():
    global connection, cursor 
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server}; SERVER=FRANCISCOBRAVO\SQLEXPRESS;DATABASE=Northwind; Trusted_Connection=yes;')
        cursor = connection.cursor()
        return connection, cursor
    except Exception as ex:
        print(f"Error al conectar a la base de datos: {ex}")
        connection = None
        cursor = None
        return None, None

@app.route('/')
def index():
    clientes = []
    conn, curr = get_db_connection() 
    
    if conn and curr:
        try:
            curr.execute("SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers WHERE IsActive = 1 ORDER BY CustomerID DESC")
            clientes_raw = curr.fetchall()

            for row in clientes_raw:
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
            print(f"Error al consultar la base de datos: {ex}")
            clientes = []
            flash(f"Error al cargar clientes: {ex}", "error")
        finally:
            if curr: curr.close()
            if conn: conn.close()
    else:
        flash("No se pudo establecer conexión a la base de datos. Verifique la configuración.", "error")

    return render_template('index.html', clientes=clientes)


@app.route('/registrar_cliente', methods=['POST'])
def registrar_cliente():
    conn, curr = get_db_connection() 

    if conn and curr:
        try:
            company_name = request.form['company_name'].strip()
            contact_name = request.form.get('contact_name', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            country = request.form.get('country', '').strip()

            # --- VALIDACIÓN DE CAMPOS OBLIGATORIOS ---
            if not company_name:
                flash("El campo 'Nombre de Compañía' es obligatorio.", "error")
                return redirect(url_for('index'))
            if not contact_name:
                flash("El campo 'Nombre de Contacto' es obligatorio.", "error")
                return redirect(url_for('index'))
            if not address:
                flash("El campo 'Dirección' es obligatorio.", "error")
                return redirect(url_for('index'))
            if not city:
                flash("El campo 'Ciudad' es obligatorio.", "error")
                return redirect(url_for('index'))
            if not postal_code.isdigit():
                flash("El campo 'Código Postal' debe contener solo números.", "error")
                return redirect(url_for('index'))
            if not country:
                flash("El campo 'País' es obligatorio.", "error")
                return redirect(url_for('index'))
            # --- NUEVA VALIDACIÓN MEJORADA: PAÍS SOLO LETRAS Y ESPACIOS ---
            # Usa una expresión regular para asegurar que solo contenga letras (a-z, A-Z) y espacios
            if not re.fullmatch(r'^[a-zA-Z\s]+$', country):
                flash("El campo 'País' debe contener solo letras y espacios.", "error")
                return redirect(url_for('index'))
            # --- FIN DE NUEVA VALIDACIÓN ---
            
            sql = """
            INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            curr.execute(sql, 
                         company_name, 
                         contact_name, 
                         address, 
                         city, 
                         postal_code, 
                         country)
            
            conn.commit()
            flash(f"Cliente '{company_name}' registrado exitosamente!", "success")
            
        except pyodbc.IntegrityError as e: 
            flash(f"Error de registro: Ocurrió un problema de integridad de datos. Posiblemente un valor duplicado no permitido.", "error")
            print(f"Error de integridad (registro): {e}")
        except Exception as ex:
            flash(f"Ocurrió un error inesperado al registrar el cliente: {ex}", "error")
            print(f"Error general al registrar: {ex}")
        finally:
            if curr: curr.close()
            if conn: conn.close()

    else:
        flash("No se pudo establecer conexión a la base de datos para registrar.", "error")

    return redirect(url_for('index')) 

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    customer_id = request.form.get('customer_id')
    if not customer_id:
        flash("ID de cliente no proporcionado para la eliminación.", "error")
        return redirect(url_for('index'))

    conn, curr = get_db_connection()

    if conn and curr:
        try:
            sql = "UPDATE Customers SET IsActive = 0 WHERE CustomerID = ?"
            curr.execute(sql, customer_id)
            conn.commit()
            flash(f"Cliente (ID: {customer_id}) eliminado lógicamente.", "success")
        except Exception as ex:
            flash(f"Error al eliminar lógicamente el cliente: {ex}", "error")
            print(f"Error al eliminar lógicamente: {ex}")
        finally:
            if curr: curr.close()
            if conn: conn.close()
    else:
        flash("No se pudo establecer conexión a la base de datos para la eliminación.", "error")

    return redirect(url_for('index'))

@app.route('/editar_cliente/<int:customer_id>')
def editar_cliente_form(customer_id):
    cliente = None
    conn, curr = get_db_connection()

    if conn and curr:
        try:
            curr.execute("SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers WHERE CustomerID = ? AND IsActive = 1", customer_id)
            row = curr.fetchone()

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
                flash(f"Cliente con ID {customer_id} no encontrado o no activo.", "error")
        except Exception as ex:
            flash(f"Error al cargar datos del cliente para editar: {ex}", "error")
            print(f"Error al buscar cliente para edición: {ex}")
        finally:
            if curr: curr.close()
            if conn: conn.close()
    else:
        flash("No se pudo establecer conexión a la base de datos para cargar datos de edición.", "error")
    
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    customer_id = None 
    conn, curr = get_db_connection()

    if conn and curr:
        try:
            customer_id = request.form['customer_id'].strip()

            if not customer_id:
                flash("ID de cliente no proporcionado para la actualización.", "error")
                return redirect(url_for('index'))

            company_name = request.form['company_name'].strip()
            contact_name = request.form.get('contact_name', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            postal_code = request.form.get('postal_code', '').strip()
            country = request.form.get('country', '').strip()

            # --- VALIDACIÓN DE CAMPOS (similar a registrar, pero al fallar, redirige al formulario de edición) ---
            if not company_name:
                flash("El campo 'Nombre de Compañía' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            if not contact_name:
                flash("El campo 'Nombre de Contacto' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            if not address:
                flash("El campo 'Dirección' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            if not city:
                flash("El campo 'Ciudad' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            if not postal_code.isdigit():
                flash("El campo 'Código Postal' debe contener solo números.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            if not country:
                flash("El campo 'País' es obligatorio.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # --- NUEVA VALIDACIÓN MEJORADA: PAÍS SOLO LETRAS Y ESPACIOS ---
            if not re.fullmatch(r'^[a-zA-Z\s]+$', country):
                flash("El campo 'País' debe contener solo letras y espacios.", "error")
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
            # --- FIN DE NUEVA VALIDACIÓN ---

            sql = """
            UPDATE Customers
            SET CustomerName = ?, ContactName = ?, Address = ?, City = ?, PostalCode = ?, Country = ?
            WHERE CustomerID = ? AND IsActive = 1
            """
            curr.execute(sql, 
                         company_name, 
                         contact_name, 
                         address, 
                         city, 
                         postal_code, 
                         country,
                         customer_id)
            
            conn.commit()
            flash(f"Cliente '{company_name}' (ID: {customer_id}) actualizado exitosamente!", "success")
            
        except Exception as ex:
            flash(f"Ocurrió un error inesperado al actualizar el cliente: {ex}", "error")
            print(f"Error al actualizar cliente: {ex}")
            if customer_id:
                return redirect(url_for('editar_cliente_form', customer_id=customer_id))
        finally:
            if curr: curr.close()
            if conn: conn.close()

    else:
        flash("No se pudo establecer conexión a la base de datos para actualizar.", "error")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)