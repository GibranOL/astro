from fastapi import FastAPI
from typing import Dict
from app.db.database import create_db_and_tables
from app.api import tarot

# Instanciamos la aplicación FastAPI
app = FastAPI(
    title="CosmoTarot API",
    description="Backend para la App de Cosmología y Tarot - Platzi Showcase",
    version="0.1.0"
)

# El evento 'startup' se ejecuta una sola vez cuando el servidor inicia.
# Aquí es el lugar perfecto para crear las tablas si no existen.
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluimos los routers de nuestra aplicación
app.include_router(tarot.router)

@app.get("/api/status", tags=["Health Check"])
async def get_status() -> Dict[str, str]:
    return {"status": "ok", "message": "CosmoTarot Backend is running smoothly"}
