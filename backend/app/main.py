from fastapi import FastAPI
from typing import Dict
from app.db.database import create_db_and_tables
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.api.auth import limiter


from contextlib import asynccontextmanager

# El evento 'lifespan' reemplaza a los eventos de startup y shutdown.
# Aquí es el lugar perfecto para crear las tablas al iniciar.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de Startup
    create_db_and_tables()
    yield
    # Lógica de Shutdown (si la hubiera, iría aquí)

# Instanciamos la aplicación FastAPI
app = FastAPI(
    title="CosmoTarot API",
    description="Backend para la App de Cosmología y Tarot - Platzi Showcase",
    version="0.1.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Incluimos los routers de nuestra aplicación
from app.api import tarot, auth
app.include_router(auth.router)
app.include_router(tarot.router)

@app.get("/api/status", tags=["Health Check"])
async def get_status() -> Dict[str, str]:
    return {"status": "ok", "message": "CosmoTarot Backend is running smoothly"}
