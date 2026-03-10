import uuid
from sqlmodel import SQLModel, Field, JSON
from typing import Optional, Dict, Any
from datetime import datetime, date, time
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class User(SQLModel, table=True):
    """
    Modelo que representa a un usuario en la plataforma CosmoTarot.
    """
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    full_name: str
    birth_date: date
    birth_time: Optional[time] = None
    birth_city: Optional[str] = None
    birth_country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Usamos sa_column para definir el tipo JSON correctamente en PostgreSQL/SQLite
    onboarding_answers: Optional[Dict[str, Any]] = Field(default={}, sa_column=Column(JSON))
    
    preferred_language: str = Field(default="es")
    timezone: str = Field(default="America/Mexico_City")
    life_number: Optional[int] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
