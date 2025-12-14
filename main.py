# =========================================================
# 1. IMPORTACIONES Y CONFIGURACIÓN INICIAL
# =========================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv # Lo usaríamos solo si queremos cargar el .env localmente

# Importaciones de los módulos (routers) de tu aplicación
from Apps.Luxuries.router import router as luxuries_router
from Apps.Cart.router import router as Cart_router
from Apps.clients.router import router as client_router
from Apps.auth.router import router as Auth_router
from Apps.common.router import router as audit_router

# Opcional: Cargar .env solo si estás ejecutando localmente
# En Vercel, las variables se inyectan automáticamente.
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Variables de entorno locales cargadas desde .env.")
except ImportError:
    # Si python-dotenv no está instalado o en Vercel, simplemente continuamos.
    pass


# =========================================================
# 2. INICIALIZACIÓN DE FASTAPI
# =========================================================

app = FastAPI(
    title="API JLUXURIES🚀",
    description="API de servicios para la gestión de productos y clientes de JLUXURIES.",
    version="1.0.0"
)


# =========================================================
# 3. CONFIGURACIÓN CORS (Cross-Origin Resource Sharing)
# =========================================================

# Definir los orígenes permitidos explícitamente
origins = [
    "https://jluxuries-front.vercel.app",  # Dominio de Producción del Frontend
    "http://localhost:5173",               # Ambiente de desarrollo 1 (ej. Vite)
    "http://localhost:3000",               # Ambiente de desarrollo 2 (ej. Next/React)
    "http://127.0.0.1:8000",               # Ambiente de desarrollo de la API
]

# Añadir el Middleware CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      # Permite el uso de cookies y headers de autorización
    allow_methods=["*"],         # Permite todos los métodos HTTP
    allow_headers=["*"],         # Permite todos los headers (incluyendo Authorization)
)


# =========================================================
# 4. INCLUSIÓN DE ROUTERS
# =========================================================

app.include_router(luxuries_router)
app.include_router(Cart_router)
app.include_router(client_router)
app.include_router(Auth_router)
app.include_router(audit_router)


# =========================================================
# 5. RUTA RAIZ (Health Check - Opcional)
# =========================================================

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "JLUXURIES API is running successfully!"}

# Puedes añadir un endpoint para verificar la conexión a la BD (temporalmente)
# @app.get("/db-status", tags=["Health"])
# def check_db_connection():
#     from Conexion.conexion import conexiondb
#     connection = conexiondb()
#     if connection:
#         connection.close()
#         return {"status": "Database connection OK"}
#     else:
#         raise HTTPException(status_code=500, detail="Database connection FAILED")

# Si usas Gunicorn o Uvicorn para ejecutar en local o en un servidor tradicional,
# la línea final de ejecución iría aquí:
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
