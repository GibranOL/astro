from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time
from enum import Enum
import uuid

class PreguntaGuia(str, Enum):
    amor = "amor"
    trabajo = "trabajo"
    vida_personal = "vida_personal"
    espiritual = "espiritual"

class EstiloLectura(str, Enum):
    directa = "directa"
    reflexiva = "reflexiva"
    poetica = "poetica"

class VisionDestino(str, Enum):
    destino_fijo = "destino_fijo"
    libre_albedrio = "libre_albedrio"
    equilibrio = "equilibrio"

class OnboardingAnswers(BaseModel):
    pregunta_guia: PreguntaGuia
    estilo_lectura: EstiloLectura
    vision_destino: VisionDestino

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    birth_date: date
    birth_time: Optional[time] = None
    birth_city: Optional[str] = None
    birth_country: Optional[str] = None
    onboarding_answers: OnboardingAnswers

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    birth_date: date
    birth_time: Optional[time] = None
    birth_city: Optional[str] = None
    birth_country: Optional[str] = None
    onboarding_answers: dict
    preferred_language: str
    timezone: str
    life_number: Optional[int] = None

    class Config:
        from_attributes = True

class UserProfileUpdateRequest(BaseModel):
    onboarding_answers: Optional[OnboardingAnswers] = None
    birth_time: Optional[time] = None
    birth_city: Optional[str] = None
    birth_country: Optional[str] = None
    preferred_language: Optional[str] = None
    timezone: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str
