import sys
import os
from dotenv import load_dotenv

# Añadimos el directorio raíz al path para poder importar los servicios del backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.ai import ai_service

def test_gemini_integration():
    """
    Script de prueba para validar la integración con Google Gemini.
    """
    print("\n🌟 --- INICIANDO PRUEBA DE INTEGRACIÓN CON GEMINI --- 🌟")

    # 1. Verificar si la API Key está configurada
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "tu_google_api_key_aqui":
        print("\n❌ ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
        print("Por favor, ve a backend/.env y pega tu clave de Google AI Studio.")
        return

    print(f"✅ API Key detectada: {api_key[:10]}... (protegida)")

    # 2. Probar la generación de Embeddings
    print("\n📡 Probando generación de Embeddings (Vectores)...")
    try:
        texto_prueba = "La Luna representa la intuición y el subconsciente."
        vector = ai_service.get_embedding(texto_prueba)
        print(f"✅ Embeddings generados con éxito!")
        print(f"   Dimensión del vector: {len(vector)} (Esperado: 768)")
    except Exception as e:
        print(f"❌ Error al generar embeddings: {e}")

    # 3. Probar la interpretación del Tarot (Generación de Texto)
    print("\n🔮 Solicitando lectura de Tarot a los astros (Gemini)...")
    
    # Datos de ejemplo para la prueba
    datos_prueba = {
        "user_name": "Gibrán",
        "sun_sign": "Escorpio",
        "card_name": "La Rueda de la Fortuna",
        "question": "¿Qué cambios vienen para mi carrera profesional este mes?"
    }

    try:
        respuesta = ai_service.generate_tarot_interpretation(**datos_prueba)
        print("\n✨ RESPUESTA DE GEMINI:")
        print("-" * 50)
        print(respuesta)
        print("-" * 50)
        print("\n✅ Prueba finalizada con éxito.")
    except Exception as e:
        print(f"❌ Error al generar interpretación: {e}")

if __name__ == "__main__":
    # Cargamos el .env explícitamente desde la carpeta backend
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    test_gemini_integration()
