from typing import List, Optional, Any
# import lancedb <-- Comentado temporalmente
from pydantic import BaseModel
import os

class TarotCardDocument(BaseModel):
    id: str 
    name: str
    content: str
    vector: Optional[List[float]] = None

class VectorStoreService:
    """
    Servicio MOCK de LanceDB para compatibilidad con Python 3.14.
    """
    
    def __init__(self, db_path: str = "data/lancedb"):
        self.db = None # Mock
        self.table_name = "tarot_knowledge"

    def create_table(self, data: List[TarotCardDocument]):
        print(f"[MOCK VectorStore] Creando tabla simulada con {len(data)} documentos.")
            
    def search_similar(self, query_vector: List[float], limit: int = 3) -> List[TarotCardDocument]:
        print("[MOCK VectorStore] Buscando vectores similares...")
        return []

vector_store = VectorStoreService()
