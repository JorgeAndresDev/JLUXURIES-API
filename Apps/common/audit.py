from Conexion.conexion import conexiondb

def log_action(user_id: int, action: str, details: str = None, ip_address: str = None):
    """
    Registra una acción en la tabla audit_logs.
    """
    connection = conexiondb()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO audit_logs (user_id, action, details, ip_address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, action, details, ip_address))
            connection.commit()
            print(f"Audit Log: {action} by User {user_id}")
        except Exception as e:
            print(f"Error logging action: {e}")
        finally:
            cursor.close()
            connection.close()
