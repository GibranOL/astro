from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
import os

# Definimos el nombre del archivo de la base de datos
sqlite_file_name = "database.db"
# La URL de conexión. Para SQLite es simplemente el prefijo + el nombre del archivo.
sqlite_url = f"sqlite:///{sqlite_file_name}"

# El "engine" es el objeto que realmente se comunica con el archivo .db
# 'check_same_thread=False' es necesario para que FastAPI (que es asíncrono) 
# pueda usar SQLite (que es síncrono por defecto) sin problemas.
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

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
