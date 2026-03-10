import os
from supabase import create_client, Client
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import uuid

from app.db.database import get_session
from app.models import User

# Asegurar que las variables de entorno existen
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Inicializar cliente de Supabase (solo si las credenciales existen)
if SUPABASE_URL and SUPABASE_KEY:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase_client = None

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency para proteger endpoints. Valida el JWT Bearer token contra Supabase Auth.
    Retorna el modelo de Usuario desde nuestra DB (PostgreSQL).
    """
    if not supabase_client:
        raise HTTPException(
            status_code=500, detail="Supabase Client not configured in environment variables."
        )

    token = credentials.credentials
    try:
        # Recuperar el usuario usando el endpoint auth de Supabase y el token actual
        # getUser es asíncrono en supabase-js pero síncrono en supabase-py para auth.get_user
        res = supabase_client.auth.get_user(token)
        supabase_user = res.user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid auth token or token expired")

    if not supabase_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Extraer el UUID real de la capa de Auth de Supabase
    auth_uid = supabase_user.id
    
    # Buscar al usuario en la tabla `users` (nuestra BD local / supabase postgres)
    user_db = session.get(User, uuid.UUID(auth_uid))
    
    if not user_db:
        raise HTTPException(status_code=403, detail="User exists in Auth but not mapped in DB.")

    return user_db
