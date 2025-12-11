from fastapi import FastAPI
from Apps.Luxuries.router import router as luxuries_router
from Apps.Cart.router import router as Cart_router
from Apps.clients.router import router as client_router
from Apps.auth.router import router as Auth_router
from Apps.common.router import router as audit_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API JLUXURIES🚀")


app.include_router(luxuries_router)
app.include_router(Cart_router)
app.include_router(client_router)
app.include_router(Auth_router)
app.include_router(audit_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner luego la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
