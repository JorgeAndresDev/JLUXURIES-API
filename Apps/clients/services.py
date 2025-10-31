from Apps.clients.schemas import clientCreate
from Conexion.conexion import conexiondb

def register_client_service(cliente: clientCreate):
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
