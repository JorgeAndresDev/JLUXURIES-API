import mysql.connector
import os # <-- ¡Nuevo! Necesitas el módulo OS

def conexiondb():
    # 🎯 Usamos os.getenv() para leer los valores de Vercel
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT") # Usamos 3306 como fallback por defecto
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DATABASE = os.getenv("DB_DATABASE")

    # Si alguna variable crítica falta, lanzamos una excepción clara
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE]):
        print("ERROR: Faltan variables de entorno de la base de datos.")
        # Podrías lanzar un error más útil aquí si el contexto lo permite
        return None 
    
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=int(DB_PORT), # Aseguramos que el puerto sea un entero
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_DATABASE,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        # print("Conexión exitosa a la base de datos") # Puedes eliminar este print en producción
        return connection
    except mysql.connector.Error as error:
        # ⚠️ Si la conexión falla, se captura el error de Python y termina la función
        print(f"ERROR CRÍTICO: No se pudo conectar a la BD remota: {error}") 
        # Esta excepción es la que probablemente está causando el 500 inicial.
        return None
