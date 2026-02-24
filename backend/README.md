# CosmoTarot Backend 🌌🃏

Este es el backend de la aplicación **CosmoTarot**, desarrollada como proyecto showcase para el reto Developer Foundations de Platzi.

## Tecnologías Utilizadas
- **FastAPI**: Framework web moderno y de alto rendimiento.
- **pyswisseph**: Motor de cálculos astronómicos de alta precisión.
- **SQLAlchemy & SQLite**: Persistencia de datos ligera.
- **LangChain & LanceDB**: Motor de IA y RAG para interpretaciones místicas.

## Requisitos Previos
- Python 3.10 o superior.
- (Opcional) Efemérides de Swiss Ephemeris para mayor rango histórico.

## Configuración del Entorno

1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar entorno virtual:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del Servidor

Para levantar el servidor en modo desarrollo (con auto-reload):

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`. 
Puedes ver la documentación interactiva en `http://127.0.0.1:8000/docs`.

---
**Nota del Mentor:** Recuerda que la calidad de un ingeniero no solo está en el código que funciona, sino en el código que otros pueden entender y mantener. ¡Sigamos construyendo!
