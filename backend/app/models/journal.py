from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TarotJournal(SQLModel, table=True):
    """
    Modelo que representa una entrada en el diario de Tarot del usuario.
    Aquí combinamos el modelo de Base de Datos y el esquema de validación.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True) # Identificador del usuario (ej. UUID o email)
    card_drawn: str                  # Nombre de la carta obtenida
    is_reversed: bool = False       # ¿Salió la carta invertida?
    interpretation: str              # La interpretación generada por la IA
    user_notes: Optional[str] = None # Reflexiones personales del usuario
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Nota para el Junior: Al heredar de SQLModel y usar table=True, 
    # le decimos a Python que esta clase se convertirá en una tabla real en SQL.
