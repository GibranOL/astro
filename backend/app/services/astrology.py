# import swisseph as swe  <-- Comentado temporalmente
from datetime import datetime
from typing import Dict, Any

class AstrologyService:
    """
    Servicio encargado de los cálculos astronómicos y efemérides.
    
    MODO ACTUAL: SIMULACIÓN DE ALTA DISPONIBILIDAD
    ----------------------------------------------
    Debido a que el entorno actual ejecuta Python 3.14 (Beta), la librería científica
    'pyswisseph' (escrita en C) no puede compilarse aún.
    
    Hemos implementado un algoritmo simplificado para calcular el signo solar
    basado en las fechas aproximadas del zodiaco. Esto permite que el backend funcione
    perfectamente para propósitos de demostración y desarrollo del frontend.
    """

    def __init__(self):
        pass

    def get_sun_position(self, birth_date: datetime) -> Dict[str, Any]:
        """
        Calcula el signo zodiacal aproximado basado en el día y mes.
        """
        day = birth_date.day
        month = birth_date.month
        
        # Lógica simplificada de fechas de corte para los signos
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            sign = "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            sign = "Tauro"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            sign = "Géminis"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            sign = "Cáncer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            sign = "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            sign = "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            sign = "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            sign = "Escorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            sign = "Sagitario"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            sign = "Capricornio"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            sign = "Acuario"
        else:
            sign = "Piscis"

        return {
            "longitude": 0.0, # Valor dummy
            "sign": sign,
            "degree_in_sign": 0.0,
            "julian_day": 0.0,
            "planet": "Sun (Simulated)"
        }

# Instancia única para ser usada en los controladores (Singleton Pattern)
astrology_service = AstrologyService()
