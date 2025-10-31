from fastapi import HTTPException
from Apps.Cart.schemas import CartItemCreate, CartItemGet, CartItemUpdate
from Conexion.conexion import conexiondb


def register_cart_service(carrito: CartItemCreate):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO carrito (id_carrito, id_cliente, id_producto, cantidad, subtotal, estado) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (carrito.id_carrito , carrito.id_cliente ,
                           carrito.id_producto , carrito.cantidad, 
                           carrito.subtotal , carrito. estado )
                cursor.execute(sql, values)
                connection.commit()
                return cursor.lastrowid  # id autogenerado
    finally:
        if connection:
            connection.close()

def get_cart_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_carrito, id_cliente, id_producto, cantidad, subtotal, estado FROM carrito")
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

def update_cart_service (Cart: CartItemUpdate):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE carrito SET id_producto = %s, cantidad = %s, subtotal = %s, estado = %s WHERE id_carrito = %s",
            (Cart.id_producto, Cart.cantidad, Cart.subtotal, Cart.estado, Cart.id_carrito)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Carrito actualizado correctamente"}
    except Exception as e:
        print(f"Error en update_cart_service: {e}")
        return {"mensaje": "Carrito actualizado correctamente"}

def delete_cart_service(id_carrito: int):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        query = "DELETE FROM carrito WHERE id_carrito = %s"
        cursor.execute(query, (id_carrito,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Carrito eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
