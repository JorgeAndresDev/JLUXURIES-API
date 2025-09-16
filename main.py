from fastapi import FastAPI
from Apps.Luxuries.router import router as luxuries_router


app = FastAPI(title="API JLUXURIES🚀")


app.include_router(luxuries_router)