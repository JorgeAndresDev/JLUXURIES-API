from Conexion.conexion import conexiondb
from typing import List, Optional


def get_all_logs_service(limit: int = 100) -> List[dict]:
    """
    Obtiene todos los logs de auditoría con información del usuario.
    
    Args:
        limit: Número máximo de logs a retornar (default: 100)
        
    Returns:
        Lista de diccionarios con logs y datos del usuario
    """
    connection = conexiondb()
    if not connection:
        return []
    
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    a.id_log,
                    a.user_id,
                    c.nombre as user_name,
                    c.email as user_email,
                    a.action,
                    a.details,
                    a.ip_address,
                    a.timestamp
                FROM audit_logs a
                INNER JOIN clientes c ON a.user_id = c.id_cliente
                ORDER BY a.timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            logs = cursor.fetchall()
            return logs if logs else []
    except Exception as e:
        print(f"Error en get_all_logs_service: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_logs_by_user_service(user_id: int, limit: int = 50) -> List[dict]:
    """
    Obtiene los logs de auditoría de un usuario específico.
    
    Args:
        user_id: ID del usuario
        limit: Número máximo de logs a retornar (default: 50)
        
    Returns:
        Lista de diccionarios con logs del usuario
    """
    connection = conexiondb()
    if not connection:
        return []
    
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    a.id_log,
                    a.user_id,
                    c.nombre as user_name,
                    c.email as user_email,
                    a.action,
                    a.details,
                    a.ip_address,
                    a.timestamp
                FROM audit_logs a
                INNER JOIN clientes c ON a.user_id = c.id_cliente
                WHERE a.user_id = %s
                ORDER BY a.timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (user_id, limit))
            logs = cursor.fetchall()
            return logs if logs else []
    except Exception as e:
        print(f"Error en get_logs_by_user_service: {e}")
        return []
    finally:
        if connection:
            connection.close()
