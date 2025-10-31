from fastapi import FastAPI
from Apps.Luxuries.router import router as luxuries_router
from Apps.Cart.router import router as Cart_router
from Apps.clients.router import router as client_router


app = FastAPI(title="API JLUXURIES🚀")


app.include_router(luxuries_router)
app.include_router(Cart_router)
app.include_router(client_router)
