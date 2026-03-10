# Migraciones con Alembic y Supabase

Este proyecto utiliza **Alembic** para gestionar las migraciones de la base de datos PostgreSQL alojada en Supabase (o de manera local vía Docker).

## Configuración Inicial (Solo la primera vez)

Si no cuentas con la estructura de Alembic en el proyecto, debes inicializarla en la raíz de `backend/`:

```bash
cd backend
alembic init alembic
```

Esto creará una carpeta `alembic` y un archivo `alembic.ini`.
Dentro de `alembic/env.py`, debes importar los modelos y el engine definido en `app/db/database.py` para enlazar el `target_metadata`:

```python
from app.db.database import engine
from app.models import User, DailyReading, TarotistQuestion, Subscription, TarotJournal
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata
```

Y en `alembic.ini`, asegura que la url se toma dinámicamente o usa el `DATABASE_URL` del entorno.

## Creando una Migración (Autogenerada)

Cada vez que alteres un modelo de `SQLModel` en `backend/app/models/`:

1. Asegúrate de tener la variable de entorno `DATABASE_URL` configurada con la conexión hacia tu base local o hacia Supabase.
2. Ejecuta el comando para que Alembic detecte los cambios:

```bash
alembic revision --autogenerate -m "Descripción de los cambios, ej: add user and subscription tables"
```

## Aplicar las Migraciones a Supabase (Upgrade)

Una vez generada la migración (revisa los ficheros en `alembic/versions`), aplica los cambios hacia la base de datos corriendo:

```bash
alembic upgrade head
```

Esto desplegará las tablas o actualizará las columnas directamente sobre la base de datos PostgreSQL.
