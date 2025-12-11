import mysql.connector
from Conexion.conexion import conexiondb

def apply_migrations():
    connection = conexiondb()
    if connection is None:
        print("Failed to connect to database")
        return

    try:
        cursor = connection.cursor()
        
        # 1. Add role column to clients if it doesn't exist
        try:
            cursor.execute("SELECT role FROM clientes LIMIT 1")
            print("Column 'role' already exists in 'clientes'.")
        except mysql.connector.Error:
            print("Adding 'role' column to 'clientes'...")
            cursor.execute("ALTER TABLE clientes ADD COLUMN role ENUM('admin', 'client') DEFAULT 'client'")
            print("Column 'role' added.")

        # 2. Create audit_logs table
        print("Creating 'audit_logs' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id_log INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(255) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES clientes(id_cliente)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        print("'audit_logs' table created (or already exists).")

        connection.commit()
        print("Migrations applied successfully.")

    except mysql.connector.Error as err:
        print(f"Error applying migrations: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    apply_migrations()
