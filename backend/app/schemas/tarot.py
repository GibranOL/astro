from pydantic import BaseModel
from datetime import datetime

class TarotDrawRequest(BaseModel):
    """
    Esquema de datos para solicitar una tirada de cartas.
    Validamos que nos envíen el nombre, la fecha de nacimiento y la pregunta.
    """
    user_name: str
    birth_date: datetime
    question: str
