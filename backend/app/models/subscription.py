import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Subscription(SQLModel, table=True):
    """
    Modelo que representa la suscripción (Free o Premium) de un usuario.
    """
    __tablename__ = "subscriptions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    plan: str = Field(description="'free' o 'premium'")
    revenue_cat_id: Optional[str] = Field(default=None, description="Para sincronizar con RevenueCat")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = Field(default=True)
