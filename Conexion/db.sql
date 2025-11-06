CREATE DATABASE IF NOT EXISTS jluxuries
CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE jluxuries;

DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  telefono VARCHAR(20),
  direccion VARCHAR(255),
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cliente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS products;

CREATE TABLE products (
  idProducts INT NOT NULL AUTO_INCREMENT,
  ProductsName VARCHAR(100) NOT NULL,
  Description TEXT,
  Quantity INT NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  color VARCHAR(50),
  image_url VARCHAR(255),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idProducts)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS carrito;

CREATE TABLE carrito (
  id_carrito INT NOT NULL AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  precio_unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
  estado ENUM('activo','comprado','cancelado') DEFAULT 'activo',
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_carrito),
  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
  FOREIGN KEY (id_producto) REFERENCES products(idProducts) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO clientes (nombre, email, password, telefono, direccion)
VALUES 
('Jorge Gómez', 'jorge@example.com', '123456', '3000000000', 'Sincelejo, Sucre');

INSERT INTO products (ProductsName, Description, Quantity, Price, color, image_url)
VALUES 
('Filtro de alto flujo UNI', 'Filtro de aire de alto rendimiento para motocicletas', 10, 85000, 'Rojo', 'https://example.com/filtro-uni.jpg'),
('Manubrio de lujo', 'Manubrio metálico con acabados premium', 15, 25000, 'Negro', 'https://example.com/manubrio.jpg');

INSERT INTO carrito (id_cliente, id_producto, cantidad, precio_unitario)
VALUES 
(1, 1, 2, 85000),
(1, 2, 1, 25000);

emailfecha_creacionidProducts