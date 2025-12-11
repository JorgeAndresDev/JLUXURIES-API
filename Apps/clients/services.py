from fastapi import HTTPException
from Apps.clients.schemas import client, ClientUpdate
from Conexion.conexion import conexiondb
from Apps.auth.auth import hash_password

def register_client_service(cliente: client):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                hashed_pwd = hash_password(cliente.password)
                sql = "INSERT INTO clientes (nombre, email, password, telefono, direccion) VALUES (%s, %s, %s, %s, %s)"
                values = (cliente.nombre, cliente.email, hashed_pwd, cliente.telefono, cliente.direccion)
                cursor.execute(sql, values)
                connection.commit()
                return cursor.lastrowid  # id autogenerado
    finally:
        if connection:
            connection.close()

def get_client_service(id_cliente: int):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT id_cliente, nombre, email, telefono, direccion, role FROM clientes WHERE id_cliente = %s",
                    (id_cliente,)
                )
                client = cursor.fetchone()  # Trae solo un registro
                return client
        else:
            return None
    except Exception as e:
        print(f"Error en la función get_client_service: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_all_cliente_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_cliente, nombre, email, telefono, direccion, role FROM clientes")
                cart = cursor.fetchall()
                return cart
        else: 
            return None
    except Exception as e:         
        print(f"Error en la función get_all_cliente_service: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()

def update_client_service (Cliente: ClientUpdate):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        # Note: Password update usually requires special handling (hashing), skipping for now or should we include it?
        # Assuming basic update for profile info.
        cursor.execute(
            "UPDATE clientes SET nombre = %s, email = %s, telefono = %s, direccion = %s, role = %s WHERE id_cliente = %s",
            (Cliente.nombre, Cliente.email, Cliente.telefono, Cliente.direccion, Cliente.role, Cliente.id_cliente)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Datos de cliente actualizados correctamente"}
    except Exception as e:
        print(f"Error en update_client_service: {e}")
        return {"mensaje": f"Error al actualizar: {str(e)}"}

def delete_client_service(id_cliente: int):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(query, (id_cliente,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Cliente eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
