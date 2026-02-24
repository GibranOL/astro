import random
from typing import List

class AIService:
    """
    Servicio encargado de la Inteligencia Artificial Generativa.
    
    MODO ACTUAL: MOCK (Simulación)
    ------------------------------
    En este momento, este servicio devuelve datos simulados para permitir
    el desarrollo del frontend y la lógica de negocio sin necesitar una API Key real.
    
    Cuando tengamos la API Key, reemplazaremos los métodos simulados por llamadas
    reales a OpenAI o Gemini usando LangChain.
    """

    def __init__(self):
        # En el futuro, aquí inicializaremos el cliente de OpenAI/Gemini
        # self.llm = ChatOpenAI(api_key=...)
        pass

    def get_embedding(self, text: str) -> List[float]:
        """
        Simula la creación de un embedding vectorial.
        
        Args:
            text: El texto a convertir.
            
        Returns:
            Una lista de 1536 números flotantes (dimensión estándar de OpenAI).
        """
        # MOCK: Generamos un vector aleatorio de dimensión 1536
        # Esto sirve para probar que LanceDB guarda y recupera arrays correctamente.
        return [random.uniform(-1.0, 1.0) for _ in range(1536)]

    def generate_tarot_interpretation(self, 
                                      user_name: str, 
                                      sun_sign: str, 
                                      card_name: str, 
                                      question: str) -> str:
        """
        Simula la generación de una lectura de tarot personalizada.
        
        Args:
            user_name: Nombre del usuario.
            sun_sign: Signo zodiacal del usuario (calculado por AstrologyService).
            card_name: Carta que salió en la tirada.
            question: La pregunta o intención del usuario.
            
        Returns:
            Un texto con la interpretación mística.
        """
        # MOCK: Retornamos una respuesta plantilla que parece real.
        return f"""🔮 Lectura para {user_name} (Sol en {sun_sign}):

La carta **{card_name}** ha aparecido en respuesta a tu pregunta: '{question}'.

[SIMULACIÓN DE IA]: Esta carta sugiere un momento de transformación profunda. La energía de {sun_sign} potencia la influencia de {card_name}, indicando que es hora de confiar en tu intuición. Los astros y el arcano te invitan a avanzar con valentía."""

# Instancia global del servicio
ai_service = AIService()
