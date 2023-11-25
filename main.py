from fastapi import FastAPI
from auth_routes import auth_router
from medicines_routes import medicines_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(medicines_router)