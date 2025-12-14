import mysql.connector
import os 
# Asegúrate de importar 'os'

def conexiondb():
    # 1. Obtener todas las variables de entorno
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT_STR = os.getenv("DB_PORT") # Lo obtenemos como string
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DATABASE = os.getenv("DB_DATABASE")

    # 2. Validación de variables (CRÍTICO)
    # Incluimos DB_PORT_STR en la validación
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT_STR]):
        # Lanzar una excepción (ValueError) es mejor que solo imprimir y devolver None,
        # ya que causará un Traceback en Vercel, dándote más información.
        # Si usas un raise, no debes devolver None, ya que el flujo se detiene aquí.
        raise ValueError("ERROR FATAL: Faltan una o más variables de entorno de la base de datos (DB_HOST, DB_PORT, etc.). Verifica la configuración de Vercel.")

    try:
        # Convertir el puerto a entero (lo cual valida que sea un número)
        DB_PORT_INT = int(DB_PORT_STR)
    except ValueError:
        raise ValueError(f"ERROR FATAL: DB_PORT ('{DB_PORT_STR}') no es un número entero válido.")

    # 3. Intento de Conexión
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT_INT, # Usamos el puerto ya convertido a entero
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_DATABASE,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        return connection
        
    except mysql.connector.Error as error:
        # Si falla por credenciales o red, este error se propaga.
        # En Vercel, si esto ocurre al iniciar la app, causará el 500.
        print(f"ERROR CRÍTICO: Falló la conexión a la BD remota. Detalle: {error}")
        # Es mejor relanzar la excepción para que Vercel la capture
        raise ConnectionError(f"No se pudo establecer conexión con la BD remota: {error}") from error
