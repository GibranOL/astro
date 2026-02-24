# CosmoTarot - Platzi Developer Foundations Showcase 🌌🃏

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![DB](https://img.shields.io/badge/DB-SQLite%20%7C%20LanceDB-blue)

**CosmoTarot** es una aplicación mística que combina la precisión de la **Astrología** con la sabiduría intuitiva del **Tarot**, potenciada por **Inteligencia Artificial Generativa**.

Este proyecto es parte del reto **Developer Foundations de Platzi**, demostrando la capacidad de integrar tecnologías modernas en una experiencia de usuario única.

## 🚀 Arquitectura del Proyecto

El proyecto sigue una arquitectura **Monorepo**:

- **`/backend`**: API RESTful construida con **FastAPI** (Python).
  - **Astrología:** Motor de cálculo de efemérides (Swiss Ephemeris / pyswisseph).
  - **Tarot:** Sistema de tiradas y significados arquetípicos.
  - **IA (RAG):** Motor de interpretación de lecturas personalizado (LangChain + LanceDB).
  - **Base de Datos:** SQLite con SQLModel para persistencia ligera.

- **`/frontend`** *(En desarrollo)*: Aplicación móvil multiplataforma construida con **Flutter**.

## 🛠️ Cómo Iniciar (Backend)

### Opción A: Docker (Recomendada)
Si tienes Docker instalado, puedes levantar todo el entorno con un solo comando:

```bash
docker-compose up --build
```
El servidor estará disponible en `http://localhost:8000`.

### Opción B: Local (Python)

1. Navega a la carpeta del backend:
   ```bash
   cd backend
   ```
2. Crea un entorno virtual e instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Tests
Para verificar que el sistema funciona correctamente, puedes ejecutar el script de prueba manual:

```bash
python backend/tests/manual_test.py
```

## 📝 Roadmap
- [x] Configuración inicial del Backend (FastAPI).
- [x] Integración de base de datos (SQLite + SQLModel).
- [x] Motor de Astrología y Tarot (Mock funcional).
- [ ] Desarrollo del Frontend en Flutter.
- [ ] Integración real con OpenAI/Gemini API.
- [ ] Despliegue en la nube (Render/Railway).

---
Hecho con ❤️ y ☕ por [GibranOL](https://github.com/GibranOL).
