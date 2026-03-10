from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import random

# Importamos nuestros servicios y modelos
from app.db.database import get_session
from app.models.journal import TarotJournal
from app.models.user import User
from app.schemas.tarot import TarotDrawRequest
from app.services.astrology import astrology_service
from app.services.ai import ai_service
from app.services.auth import get_current_user

# Creamos un router específico para las rutas de Tarot
router = APIRouter(
    prefix="/api/tarot",
    tags=["Tarot"]
)

# Lista simplificada de Arcanos Mayores para nuestro Mock
MAJOR_ARCANA = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]

@router.post("/draw", response_model=TarotJournal)
def draw_card(
    request: TarotDrawRequest, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Realiza una tirada de cartas para el usuario.
    Combina la astrología (signo solar) con la lectura del Tarot.
    """
    
    # 1. Calcular el Signo Solar del usuario
    try:
        astro_data = astrology_service.get_sun_position(request.birth_date)
        sun_sign = astro_data["sign"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el cálculo astrológico: {str(e)}")

    # 2. Simular sacar una carta (Lógica de Negocio)
    # En el futuro, esto podría ser más complejo (barajar, cortar, etc.)
    card_name = random.choice(MAJOR_ARCANA)
    is_reversed = random.choice([True, False]) # 50% de probabilidad de salir invertida

    # 3. Generar Interpretación con IA (Mock por ahora)
    interpretation_text = ai_service.generate_tarot_interpretation(
        user_name=request.user_name,
        sun_sign=sun_sign,
        card_name=f"{card_name}",
        question=request.question
    )

    if is_reversed:
        interpretation_text = f"[INVERTIDA] {interpretation_text}"

    # 4. Guardar en el Diario de Tarot (Base de Datos)
    journal_entry = TarotJournal(
        user_id=str(current_user.id), # UUID to string if TarotJournal model expects string/int
        card_drawn=card_name,
        is_reversed=is_reversed,
        interpretation=interpretation_text,
        user_notes=request.question # Guardamos la pregunta como nota inicial
    )
    
    # Transacción SQL: Añadir, Confirmar, Refrescar
    session.add(journal_entry)
    session.commit()
    session.refresh(journal_entry) # Obtenemos el ID autogenerado por la DB

    return journal_entry
