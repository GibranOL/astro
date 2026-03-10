import uuid
from sqlmodel import SQLModel, Field, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class DailyReading(SQLModel, table=True):
    """
    Modelo que representa la lectura diaria de tarot de un usuario.
    """
    __tablename__ = "daily_readings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    reading_date: date
    
    # Lista de cartas obtenidas (con sus posiciones, etc.)
    cards_drawn: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    
    ai_interpretation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
