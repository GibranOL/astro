from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from datetime import datetime

from app.db.database import get_session
from app.models import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserProfileResponse,
    UserProfileUpdateRequest,
    RefreshTokenRequest,
)
from app.services.auth import supabase_client, get_current_user

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
def register_user(payload: UserRegisterRequest, session: Session = Depends(get_session)):
    """
    Registra un usuario en Supabase Auth y luego inserta el perfil en PostgreSQL.
    """
    if not supabase_client:
        raise HTTPException(500, "Supabase config missing.")

    # 1. Crear en Supabase Auth
    try:
        auth_response = supabase_client.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
    except Exception as e:
        raise HTTPException(400, f"Registration failed: {str(e)}")

    if not auth_response.user:
        raise HTTPException(400, "User could not be created in Supabase.")

    supabase_uid = auth_response.user.id

    # 2. Verificar duplicados locales
    existing = session.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(409, "User email already registered in DB.")

    # 3. Crear Perfil en la Base de Datos
    new_user = User(
        id=supabase_uid,
        email=payload.email,
        full_name=payload.full_name,
        birth_date=payload.birth_date,
        birth_time=payload.birth_time,
        birth_city=payload.birth_city,
        birth_country=payload.birth_country,
        onboarding_answers=payload.onboarding_answers.dict() if payload.onboarding_answers else {},
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "User successfully registered.", "user_id": new_user.id}

@router.post("/login")
@limiter.limit("5/15minute")
def login_user(request: Request, payload: UserLoginRequest):
    """
    Inicia sesión y devuelve el token JWT de Supabase.
    Limitado a 5 intentos cada 15 min.
    """
    if not supabase_client:
        raise HTTPException(500, "Supabase config missing.")

    try:
        auth_response = supabase_client.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
    except Exception as e:
        raise HTTPException(401, "Invalid email or password")
    
    return {
        "access_token": auth_response.session.access_token,
        "token_type": "bearer",
        "refresh_token": auth_response.session.refresh_token,
        "expires_in": auth_response.session.expires_in
    }

@router.post("/logout")
def logout_user(current_user: User = Depends(get_current_user)):
    """
    Cierra la sesión destruyendo el token válido de Supabase del lado del servidor.
    En la mayoría de aplicaciones Stateless (JWT), basta con descartar el token 
    en el Flutter frontend, pero supabase-py puede invalidar la sesión actual.
    """
    supabase_client.auth.sign_out()
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve el perfil del usuario autenticado mapeando el JWT contra 
    la base de datos PostgreSQL.
    """
    return current_user

@router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    payload: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Actualiza datos del perfil (onboarding answers, etc.)
    """
    update_data = payload.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        if key == "onboarding_answers" and value:
            # Pydantic a dict si es diccionario subyacente
            current_user.onboarding_answers = value
        else:
            setattr(current_user, key, value)
            
    current_user.updated_at = datetime.utcnow()
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return current_user

@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest):
    """
    Refresca el token JWT usando el refresh token de Supabase.
    """
    if not supabase_client:
        raise HTTPException(500, "Supabase config missing.")

    try:
        res = supabase_client.auth.refresh_session(payload.refresh_token)
    except Exception as e:
        raise HTTPException(401, "Invalid or expired refresh token")

    if not res.session:
        raise HTTPException(401, "Could not refresh session")

    return {
        "access_token": res.session.access_token,
        "token_type": "bearer",
        "refresh_token": res.session.refresh_token,
        "expires_in": res.session.expires_in
    }
