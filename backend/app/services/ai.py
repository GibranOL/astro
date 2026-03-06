import os
import random
from typing import List, Optional

# Intentamos importar dotenv de forma segura
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Intentamos importar las librerías de LangChain
try:
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class AIService:
    """
    Servicio de IA con manejo robusto de modelos para evitar el error 404.
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # Usamos nombres directos que son más estables
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL", "embedding-001")
        
        self.llm: Optional[ChatGoogleGenerativeAI] = None
        self.embeddings: Optional[GoogleGenerativeAIEmbeddings] = None
        
        if LANGCHAIN_AVAILABLE and self.api_key and "tu_google" not in self.api_key:
            try:
                # Inicialización del modelo de chat
                self.llm = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    temperature=0.8,
                    google_api_key=self.api_key
                )
                
                # Inicialización de embeddings (usamos model o task_type dependiendo del modelo)
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    model=f"models/{self.embedding_model_name}",
                    google_api_key=self.api_key
                )
                print(f"✅ Gemini Service inicializado (Model: {self.model_name})")
            except Exception as e:
                print(f"❌ Error al inicializar Gemini: {str(e)}")

    def get_embedding(self, text: str) -> List[float]:
        """
        Crea un embedding vectorial real con manejo de error 404.
        """
        if self.embeddings is not None:
            try:
                return self.embeddings.embed_query(text)
            except Exception as e:
                # Si falla el 404, mostramos el error específico pero seguimos con el mock
                if "404" in str(e):
                    print(f"⚠️ El modelo de embeddings {self.embedding_model_name} no se encontró.")
                else:
                    print(f"⚠️ Error en embedding real: {str(e)}")
        
        return [random.uniform(-1.0, 1.0) for _ in range(768)]

    def generate_tarot_interpretation(self, 
                                      user_name: str, 
                                      sun_sign: str, 
                                      card_name: str, 
                                      question: str) -> str:
        """
        Genera una lectura de tarot con manejo de error 404.
        """
        if self.llm is None:
            return f"🔮 [MOCK] Lectura para {user_name} (Sol en {sun_sign}): La carta {card_name} indica transformación."

        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Eres un experto Maestro de Tarot y Astrólogo místico. Tu tono es sabio, empático y profundo.
            Utilizas el conocimiento de los astros y los arcanos para guiar a las personas.
            Siempre te refieres al usuario por su nombre y mencionas su signo solar.
            Tus respuestas deben ser visualmente ricas, usando negritas para conceptos clave y emojis místicos.
            No des consejos médicos o legales drásticos, enfócate en el crecimiento espiritual y personal.
            """),
            ("user", """
            Hola maestro. Mi nombre es {user_name} y mi signo solar es {sun_sign}.
            He sacado la carta del Tarot: {card_name}.
            Mi pregunta o inquietud es la siguiente: "{question}"
            
            Por favor, interpreta este mensaje de los arcanos para mí en español.
            """)
        ])

        try:
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({
                "user_name": user_name,
                "sun_sign": sun_sign,
                "card_name": card_name,
                "question": question
            })
        except Exception as e:
            if "404" in str(e):
                return f"❌ Error 404: El modelo '{self.model_name}' no se encontró. Verifica el nombre en el archivo .env."
            return f"❌ Error al conectar con los astros (Gemini): {str(e)}"

# Instancia global del servicio
ai_service = AIService()
