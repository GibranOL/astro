from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

# Cargar variables de entorno (por defecto busca en el directorio actual o padres)
load_dotenv()

# Obtener la URL de la base de datos de las variables de entorno
# Hacemos fallback a SQLite si no existe, para evitar romper tests inmediatos 
# si alguien olvida configurar el .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Configurar el engine. Para Postgres en Supabase, la configuración recomendada a veces
# requiere pool_pre_ping=True para manejar conexiones caídas.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args, 
    echo=False, # Pon en True para ver los logs SQL en la consola
    pool_pre_ping=True if not DATABASE_URL.startswith("sqlite") else False
)

def create_db_and_tables():
    """
    Función para inicializar la base de datos y crear todas las tablas
    definidas en nuestros modelos.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Generador de sesiones para FastAPI. 
    Esto nos permite usar la base de datos en nuestras rutas de forma limpia.
    El 'yield' asegura que la conexión se cierre automáticamente después de usarse.
    """
    with Session(engine) as session:
        yield session
