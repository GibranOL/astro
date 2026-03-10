from datetime import datetime
from sqlmodel import Session, select
from typing import Dict, Any
import uuid

from app.models import TarotistQuestion, Subscription

def check_user_limits(session: Session, user_id: uuid.UUID) -> Dict[str, Any]:
    """
    Verifica si el usuario ha utilizado su pregunta gratuita del día.
    Los usuarios de pago (premium) no están sujetos a este límite.
    """
    
    # 1. Verificar si el usuario tiene una suscripción premium activa
    statement_sub = select(Subscription).where(
        Subscription.user_id == user_id,
        Subscription.plan == "premium",
        Subscription.is_active == True
    )
    active_subscription = session.exec(statement_sub).first()
    
    if active_subscription:
        return {
            "can_ask": True, 
            "questions_used_today": 0, 
            "is_premium": True
        }

    # 2. Si es usuario Free, contar cuántas preguntas ha hecho hoy
    today = datetime.utcnow().date()
    
    # SQLite/Postgres trick to cast datetime to date portably depends on the engine,
    # but since asked_at is a datetime, we can check a range or rely on Python mapping.
    # To keep portability simple across SQLAlchemy: we'll fetch today's records.
    # We query records from the start of the current UTC day.
    
    start_of_day = datetime(today.year, today.month, today.day)
    
    statement_questions = select(TarotistQuestion).where(
        TarotistQuestion.user_id == user_id,
        TarotistQuestion.asked_at >= start_of_day,
        TarotistQuestion.is_free == True
    )
    questions_today = session.exec(statement_questions).all()
    questions_count = len(questions_today)
    
    # Límite: 1 pregunta gratuita por día
    can_ask = questions_count < 1
    
    return {
        "can_ask": can_ask,
        "questions_used_today": questions_count,
        "is_premium": False
    }
