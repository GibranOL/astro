from fastapi.testclient import TestClient
from app.main import app
from app.db.database import create_db_and_tables # Importamos el creador de tablas
import json
import os

# Instanciamos el cliente de pruebas
client = TestClient(app)

def run_test():
    """
    Ejecuta una petición simulada al endpoint /api/tarot/draw.
    """
    # 0. Asegurar que la base de datos existe para el test
    print("🛠 [TEST] Inicializando base de datos de prueba...")
    create_db_and_tables()

    print("🔮 [TEST] Enviando petición a CosmoTarot...")
    
    # Datos simulados del usuario
    payload = {
        "user_name": "Estudiante de Platzi",
        "birth_date": "1999-01-01T12:00:00",
        "question": "¿Tendré éxito con mi proyecto Showcase?"
    }

    # Enviamos la petición POST
    response = client.post("/api/tarot/draw", json=payload)

    if response.status_code == 200:
        print("✅ [OK] Respuesta recibida exitosamente:")
        data = response.json()
        
        # Formateamos la salida para que sea legible
        print(f"""
--- Resultado de la Tirada ---
👤 Usuario: {data['user_id']}
🃏 Carta: {data['card_drawn']}
🔄 Invertida: {'Sí' if data['is_reversed'] else 'No'}
📜 Interpretación:
{data['interpretation']}
------------------------------
""")
    else:
        print(f"❌ [ERROR] Falló la petición: {response.text}")

if __name__ == "__main__":
    run_test()
