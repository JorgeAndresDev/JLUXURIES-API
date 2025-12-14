from fastapi import FastAPI
from Apps.Luxuries.router import router as luxuries_router
from Apps.Cart.router import router as Cart_router
from Apps.clients.router import router as client_router
from Apps.auth.router import router as Auth_router
from Apps.common.router import router as audit_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API JLUXURIES🚀")

# 🎯 Paso 1: Definir los orígenes permitidos explícitamente
# Incluye el dominio de tu frontend y los dominios locales de desarrollo
origins = [
    "https://jluxuries-front.vercel.app",  # <--- Dominio de Producción
    "http://localhost:5173",               # Ejemplo si usas Vite en local
    "http://localhost:3000",               # Ejemplo si usas React/Next.js en local
    "http://127.0.0.1:8000",
]

app.include_router(luxuries_router)
app.include_router(Cart_router)
app.include_router(client_router)
app.include_router(Auth_router)
app.include_router(audit_router)


# 🎯 Paso 2: Usar la lista de orígenes en el middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # <-- ¡CAMBIADO de ["*"] a la lista 'origins'!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
