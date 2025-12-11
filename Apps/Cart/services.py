from fastapi import HTTPException
from Apps.Cart.schemas import CartItemCreate, CartItemUpdate
from Conexion.conexion import conexiondb


def register_cart_service(carrito: CartItemCreate):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO carrito (id_cliente, id_producto, cantidad, precio_unitario, estado) VALUES (%s, %s, %s, %s, %s)"
                values = (carrito.id_cliente, carrito.id_producto, carrito.cantidad, carrito.precio_unitario, carrito.estado)
                cursor.execute(sql, values)
                connection.commit()
                return cursor.lastrowid
    finally:
        if connection:
            connection.close()

def get_cart_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_carrito, id_cliente, id_producto, cantidad, precio_unitario, subtotal, estado FROM carrito")
                cart = cursor.fetchall()
                return cart
        else: 
            return None
    except Exception as e:         
        print(f"Error en la función get_cart_service: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()

def get_cart_by_client_service(id_cliente: int):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                sql = """
                SELECT c.id_carrito, c.id_cliente, c.id_producto, c.cantidad, 
                       c.precio_unitario, c.subtotal, c.estado,
                       p.ProductsName, p.image_url
                FROM carrito c
                INNER JOIN products p ON c.id_producto = p.idProducts
                WHERE c.id_cliente = %s AND c.estado = 'activo'
                """
                cursor.execute(sql, (id_cliente,))
                cart_items = cursor.fetchall()
                return cart_items
        else:
            return None
    except Exception as e:
        print(f"Error en get_cart_by_client_service: {e}")
        return None
    finally:
        if connection:
            connection.close()

def update_cart_service(Cart: CartItemUpdate):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE carrito SET cantidad = %s, precio_unitario = %s, estado = %s WHERE id_carrito = %s",
            (Cart.cantidad, Cart.precio_unitario, Cart.estado, Cart.id_carrito)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Carrito actualizado correctamente"}
    except Exception as e:
        print(f"Error en update_cart_service: {e}")
        return {"mensaje": f"Error al actualizar: {str(e)}"}
    
def delete_cart_service(id_carrito: int):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        query = "DELETE FROM carrito WHERE id_carrito = %s"
        cursor.execute(query, (id_carrito,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Item del carrito eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
