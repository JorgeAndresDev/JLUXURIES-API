from fastapi import HTTPException
from Apps.clients.schemas import client
from Conexion.conexion import conexiondb

def register_client_service(cliente: client):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO clientes (nombre) VALUES (%s)"
                values = (cliente.nombre,)
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
                    "SELECT id_cliente, nombre FROM clientes WHERE id_cliente = %s",
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
                cursor.execute("SELECT id_cliente, nombre FROM clientes")
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

def update_client_service (Cliente: client):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE clientes SET nombre = %s WHERE id_cliente = %s",
            (Cliente.nombre, Cliente.id_cliente)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Datos de cliente actualizados correctamente"}
    except Exception as e:
        print(f"Error en update_client_service: {e}")
        return {"mensaje": "Datos de cliente actualizados correctamente"}

def delete_client_service(id_cliente: int):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(query, (id_cliente,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Cleinte eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
