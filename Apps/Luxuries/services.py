from fastapi import HTTPException
from Apps.Luxuries.schemas import LuxuryItem, LuxuryItemCreate, LuxuryItemUpdate
from Conexion.conexion import conexiondb


def get_luxuries_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idProducts, ProductsName, Quantity, Price FROM products")
                jluxuries = cursor.fetchall()
                return jluxuries
        else: 
            return None
    except Exception as e:         
        print(f"Error en la función get_luxuries_service: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()

def get_item_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idProducts, ProductsName, Quantity, Price, Color FROM products")
                items = cursor.fetchall()  # Trae todos los registros
                return items
        else:
            return None
    except Exception as e:
        print(f"Error en la función get_item_service: {e}")
        return None
    finally:
        if connection:
            connection.close()


def register_luxury_service(luxury: LuxuryItemCreate):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO products (ProductsName, Quantity, Price, color) VALUES (%s, %s, %s, %s)"
                values = (luxury.ProductsName, luxury.Quantity, luxury.Price, luxury.color)
                cursor.execute(sql, values)
                connection.commit()
                return cursor.lastrowid  # id autogenerado
    finally:
        if connection:
            connection.close()

def update_luxury_service (luxury: LuxuryItemUpdate):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE products SET ProductsName = %s, Quantity = %s, Price = %s, color = %s WHERE idProducts = %s",
            (luxury.ProductsName, luxury.Quantity, luxury.Price, luxury.color, luxury.idProducts)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Item actualizado correctamente"}
    except Exception as e:
        print(f"Error en update_luxury_service: {e}")
        return {"mensaje": "Item actualizado correctamente"}
    
def delete_luxury_service(idProducts: LuxuryItem):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        query = "DELETE FROM products WHERE idProducts = %s"
        cursor.execute(query, (idProducts,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Item eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

