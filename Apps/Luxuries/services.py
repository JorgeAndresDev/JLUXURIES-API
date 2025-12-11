from fastapi import HTTPException
from Apps.Luxuries.schemas import LuxuryItem, LuxuryItemCreate, LuxuryItemUpdate
from Conexion.conexion import conexiondb


def get_luxuries_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idProducts, ProductsName, moto, categoria, Quantity, color, Description, Price, image_url FROM products")
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

def get_item_service(idProducts: int):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                sql = """
                SELECT idProducts, ProductsName, moto, categoria, Quantity, 
                       color, Description, Price, image_url 
                FROM products 
                WHERE idProducts = %s
                """
                cursor.execute(sql, (idProducts,))
                item = cursor.fetchone()
                return item
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
                sql = """
                INSERT INTO products 
                (ProductsName, moto, categoria, Quantity, Price, color, Description, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    luxury.ProductsName,
                    luxury.moto,
                    luxury.categoria,
                    luxury.Quantity,
                    luxury.Price,
                    luxury.color,
                    luxury.Description,
                    luxury.image_url
                )
                cursor.execute(sql, values)
                connection.commit()
                return cursor.lastrowid
    finally:
        if connection:
            connection.close()


def update_luxury_service(idProducts: int, luxury: LuxuryItemUpdate):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()

        # Convertir el modelo a dict y filtrar solo los campos no nulos
        data = {field: value for field, value in luxury.dict().items() if value is not None}

        if not data:
            return {"mensaje": "No hay campos para actualizar"}

        # Construir el SQL dinámicamente
        set_clause = ", ".join([f"{field} = %s" for field in data.keys()])
        values = list(data.values()) + [idProducts]

        sql = f"UPDATE products SET {set_clause} WHERE idProducts = %s"

        cursor.execute(sql, values)
        conexion.commit()

        if cursor.rowcount == 0:
            return {"mensaje": "No se encontró el producto o no hubo cambios"}

        return {"mensaje": "Item actualizado correctamente"}

    except Exception as e:
        print(f"Error en update_luxury_service: {e}")
        return {"mensaje": f"Error al actualizar: {str(e)}"}

    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

    
def delete_luxury_service(idProducts: int):
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
