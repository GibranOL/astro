import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TarotistQuestion(SQLModel, table=True):
    """
    Modelo que representa una pregunta hecha por el usuario al tarotista IA.
    """
    __tablename__ = "tarotist_questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    question: str
    answer: str
    asked_at: datetime = Field(default_factory=datetime.utcnow)
    is_free: bool = Field(default=False, description="True si es la pregunta gratuita del día")
