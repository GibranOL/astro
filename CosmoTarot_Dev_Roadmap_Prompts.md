# 🔮 CosmoTarot — Roadmap de Desarrollo & Prompts de Implementación

**Versión:** 1.0  
**Fecha:** Marzo 2026  
**Stack:** FastAPI · Supabase · Flutter · Google Gemini · LanceDB  

---

## 📌 Nota sobre Supabase: ¿Qué pasa si la app despega?

Supabase es PostgreSQL real, no un toy database. Escala muy bien:

| Etapa | Usuarios | Plan Supabase | Costo aprox. |
|---|---|---|---|
| MVP | 0 – 500 | Free | $0/mes |
| Crecimiento | 500 – 10,000 | Pro | $25/mes |
| Escalado | 10,000 – 100,000 | Pro + add-ons | $25–$200/mes |
| Startup real | 100,000+ | Team / Enterprise | Negociable |

Si en algún momento necesitas salir de Supabase, el escape es limpio: es PostgreSQL estándar. Puedes migrar a AWS RDS, Neon, o tu propio servidor sin cambiar una sola línea de código ORM. **No hay vendor lock-in real.**

---

## 🗺️ Mapa de Tareas (en orden de ejecución)

1. Migrar BD a PostgreSQL/Supabase + schema completo de usuario
2. Sistema de autenticación (Supabase Auth)
3. QA Strategy completo (tests + CI/CD + seguridad)
4. Refinamiento del RAG con LanceDB
5. Frontend Flutter (onboarding + lectura diaria)
6. Integración RevenueCat (monetización)

---

## 🧩 PROMPT 1 — Migración de Base de Datos a Supabase

```
Contexto del proyecto:
Tengo una aplicación llamada CosmoTarot. Es una app de tarot, numerología y astrología
potenciada con IA (Google Gemini). El backend está hecho en FastAPI (Python) con SQLModel
como ORM. Actualmente usa SQLite como base de datos y quiero migrarla a PostgreSQL
usando Supabase.

Tu tarea:
1. Actualiza la configuración de conexión en `backend/app/db/database.py` para conectarse
   a Supabase (PostgreSQL) usando la DATABASE_URL de Supabase. Usa variables de entorno
   con python-dotenv.

2. Crea o actualiza los modelos SQLModel para que incluyan las siguientes entidades:

   Tabla: users
   - id: UUID (primary key, generado automáticamente)
   - email: str (único, requerido)
   - full_name: str
   - birth_date: date (requerido — para calcular número de vida)
   - birth_time: time (opcional — para carta natal completa)
   - birth_city: str (opcional)
   - birth_country: str (opcional)
   - latitude: float (opcional, calculado desde ciudad)
   - longitude: float (opcional, calculado desde ciudad)
   - onboarding_answers: JSON (respuestas de las 3 preguntas de personalización)
   - preferred_language: str (default: "es")
   - timezone: str (default: "America/Mexico_City")
   - life_number: int (calculado, guardado para no recalcular)
   - created_at: datetime (auto)
   - updated_at: datetime (auto)

   Tabla: daily_readings
   - id: UUID
   - user_id: UUID (FK → users)
   - reading_date: date
   - cards_drawn: JSON (lista de 3 cartas con posición)
   - ai_interpretation: text
   - created_at: datetime

   Tabla: tarotist_questions
   - id: UUID
   - user_id: UUID (FK → users)
   - question: text
   - answer: text
   - asked_at: datetime
   - is_free: bool (True si es la pregunta gratuita del día)

   Tabla: subscriptions
   - id: UUID
   - user_id: UUID (FK → users)
   - plan: str (free | premium)
   - revenue_cat_id: str (para sincronizar con RevenueCat)
   - started_at: datetime
   - expires_at: datetime (nullable)
   - is_active: bool

3. Crea un archivo `backend/app/db/migrations/` con instrucciones de cómo aplicar
   las migraciones usando Alembic con Supabase.

4. Actualiza el `docker-compose.yml` para que acepte la variable DATABASE_URL
   como variable de entorno, con soporte para conectarse a Supabase en producción
   y a una imagen de PostgreSQL local para desarrollo/tests.

5. Crea un archivo `.env.example` con todas las variables de entorno necesarias
   (sin valores reales).

Restricciones:
- Usa SQLModel (no SQLAlchemy puro, aunque internamente lo usa)
- Mantén compatibilidad con los servicios existentes (tarot.py, astrology.py, ai.py)
- Todo el código debe tener type hints completos
- Añade docstrings en español
```

---

## 🔐 PROMPT 2 — Sistema de Autenticación con Supabase Auth

```
Contexto del proyecto:
CosmoTarot es una app de tarot/numerología/IA con backend en FastAPI y Supabase como
base de datos. Voy a usar Supabase Auth para el manejo de autenticación.

Tu tarea:
1. Configura la integración de Supabase Auth en el backend FastAPI:
   - Instala y configura `supabase-py`
   - Crea un middleware o dependency en FastAPI que valide el JWT token de Supabase
     en cada request protegido (usando `get_current_user`)
   - El token viene en el header Authorization: Bearer <token>

2. Crea los siguientes endpoints en `backend/app/api/auth.py`:
   - POST /api/auth/register — recibe email + password + datos de perfil (nombre,
     fecha de nacimiento, etc.) Crea el usuario en Supabase Auth Y en nuestra tabla
     users de PostgreSQL en una transacción.
   - POST /api/auth/login — devuelve el JWT de Supabase
   - POST /api/auth/logout
   - GET /api/auth/me — devuelve el perfil completo del usuario autenticado
   - PUT /api/auth/profile — actualiza datos del perfil (onboarding_answers,
     birth_time, etc.)
   - POST /api/auth/refresh — refresca el token

3. Crea los schemas Pydantic en `backend/app/schemas/auth.py`:
   - UserRegisterRequest
   - UserLoginRequest
   - UserProfileResponse
   - OnboardingAnswers (con las 3 preguntas específicas de CosmoTarot:
     * pregunta_guia: Enum("amor", "trabajo", "vida_personal", "espiritual")
     * estilo_lectura: Enum("directa", "reflexiva", "poetica")
     * vision_destino: Enum("destino_fijo", "libre_albedrio", "equilibrio"))

4. Implementa la lógica de "pregunta gratuita diaria":
   - Crea una función en `backend/app/services/limits.py` que verifique si el usuario
     ya usó su pregunta gratuita del día (consulta tabla tarotist_questions).
   - Usuarios premium no tienen este límite.
   - Devuelve: { can_ask: bool, questions_used_today: int, is_premium: bool }

5. Protege todos los endpoints existentes de tarot con el middleware de auth.

Restricciones:
- Nunca guardes passwords en nuestra BD, solo en Supabase Auth
- Maneja errores de Supabase con respuestas HTTP apropiadas (401, 403, 409)
- Añade rate limiting básico en el endpoint de login (máx 5 intentos / 15 min)
- Todo con type hints y docstrings en español
```

---

## 🧪 PROMPT 3 — Estrategia QA Completa (Tests + CI/CD + Seguridad)

```
Contexto del proyecto:
CosmoTarot es mi proyecto showcase para demostrar habilidades de QA. El backend está
en FastAPI (Python) con Supabase/PostgreSQL. Necesito una estrategia de testing robusta
que cubra unit tests, integration tests, contract tests, seguridad y un pipeline CI/CD.
Este proyecto será parte de mi portafolio profesional como QA Engineer.

Tu tarea tiene 4 partes:

--- PARTE A: Tests Unitarios ---
Crea tests unitarios en `backend/tests/unit/` para cada servicio:

1. `test_tarot_service.py` — prueba el motor de tiradas:
   - que una tirada devuelva exactamente 3 cartas
   - que no se repitan cartas en la misma tirada
   - que cada carta tenga los campos: name, arcana, position, meaning
   - que el número de vida se calcule correctamente para distintas fechas

2. `test_astrology_service.py` — prueba el servicio de astrología:
   - cálculo correcto del signo solar por fecha
   - cálculo del número de vida (prueba con al menos 5 casos conocidos)
   - manejo de fechas inválidas

3. `test_ai_service.py` — prueba el servicio de IA (con mocks):
   - que el fallback funciona cuando Gemini falla (simula error 429, 500, timeout)
   - que la respuesta de Gemini se parsea correctamente
   - que el prompt se construye con el contexto del usuario (onboarding_answers)

4. `test_limits_service.py` — prueba los límites de uso:
   - usuario free que ya usó su pregunta no puede hacer otra
   - usuario premium siempre puede preguntar
   - el contador se resetea a medianoche

--- PARTE B: Tests de Integración ---
Crea tests de integración en `backend/tests/integration/` usando `pytest` con
`httpx.AsyncClient` y una base de datos PostgreSQL de test (usa pytest-postgresql
o una DB de test en Supabase).

1. `test_auth_endpoints.py`:
   - flujo completo: register → login → get /me → update profile
   - intentos de login con credenciales incorrectas (debe dar 401)
   - registro con email duplicado (debe dar 409)
   - acceso a endpoint protegido sin token (debe dar 401)

2. `test_tarot_endpoints.py`:
   - GET /api/tarot/daily — usuario autenticado recibe su lectura diaria
   - GET /api/tarot/daily — llamado dos veces el mismo día, devuelve la misma lectura
   - POST /api/tarot/ask — usuario free puede hacer 1 pregunta por día
   - POST /api/tarot/ask — usuario free que ya preguntó recibe error 429

3. `test_subscription_flow.py`:
   - usuario free tiene acceso limitado
   - simula webhook de RevenueCat que activa premium
   - usuario premium tiene acceso ilimitado

--- PARTE C: Tests de Contrato (Gemini API) ---
Crea en `backend/tests/contract/test_gemini_contract.py`:
- Usa `pytest-mock` para mockear la API de Gemini
- Verifica que nuestro código maneja correctamente:
  * Respuesta exitosa con el formato esperado
  * Error 429 (rate limit) — debe usar fallback
  * Error 503 (servicio no disponible) — debe usar fallback
  * Timeout — debe usar fallback
  * Respuesta con contenido vacío
  * Respuesta con contenido que no es JSON válido (cuando esperamos JSON)
- Cada test debe ser independiente (no depender de estado compartido)

--- PARTE D: CI/CD con GitHub Actions ---
Crea `.github/workflows/qa-pipeline.yml` que:
1. Se ejecute en cada Push a cualquier rama y en cada Pull Request a `main`
2. Pasos del pipeline:
   - Setup Python 3.11
   - Instalar dependencias (`pip install -r requirements-dev.txt`)
   - Linting: `ruff check .` y `black --check .`
   - Type checking: `mypy backend/app/`
   - Unit tests: `pytest tests/unit/ -v --cov=app --cov-report=xml`
   - Integration tests: `pytest tests/integration/ -v` (con PostgreSQL service)
   - Contract tests: `pytest tests/contract/ -v`
   - Security scan: `bandit -r backend/app/ -ll`
   - Upload coverage report a Codecov
3. Si cualquier paso falla, el pipeline falla y bloquea el merge.
4. En merge a `main`: también corre `safety check` para vulnerabilidades en dependencias.

--- PARTE E: Seguridad ---
Adicionalmente, implementa estas medidas de seguridad y crea tests para cada una:

1. `backend/app/security/`:
   - `input_sanitizer.py`: sanitiza inputs del usuario antes de enviarlos a Gemini
     (previene prompt injection). Test: envía prompts maliciosos y verifica que se limpian.
   - `rate_limiter.py`: implementa rate limiting por usuario y por IP usando Redis
     (o en memoria para MVP). Test: verifica que se bloquea después del límite.

2. En los tests de integración, agrega casos de seguridad:
   - SQL injection attempts en campos de texto
   - XSS en campos de nombre y preguntas
   - JWT manipulado / expirado / de otro usuario
   - Intentar acceder a lecturas de otro usuario (debe dar 403)

Restricciones:
- Usa `pytest` y `pytest-asyncio` para tests async
- Coverage mínimo objetivo: 80%
- Cada test debe tener un docstring que explique QUÉ prueba y POR QUÉ
- Crea también `QA_STRATEGY.md` en la raíz del proyecto documentando toda la estrategia
  (pirámide de tests, herramientas, cómo correr cada tipo de test, métricas de calidad)
- El QA_STRATEGY.md debe ser tan bueno que pueda usarse como pieza de portafolio
```

---

## 🤖 PROMPT 4 — Refinamiento del RAG con LanceDB

```
Contexto del proyecto:
CosmoTarot usa RAG (Retrieval Augmented Generation) para que el tarotista IA tenga
conocimiento profundo sobre tarot, numerología y astrología, además del contexto
personal del usuario. El backend es FastAPI y ya existe un archivo `vector_store.py`
con una integración inicial con LanceDB.

Tu tarea:
1. Revisa y completa `backend/app/services/vector_store.py`:
   - Inicializa LanceDB con persistencia en disco (directorio configurable por .env)
   - Crea las siguientes colecciones (tablas en LanceDB):
     * `tarot_knowledge`: significados de las 78 cartas (upright + reversed),
       arquetipos, simbolismo, combinaciones comunes
     * `numerology_knowledge`: significados de números de vida 1-9, números maestros
       11, 22, 33, años personales, meses personales
     * `astrology_knowledge`: significados de signos, planetas, casas, aspectos
     * `user_context`: fragmentos del historial de conversación del usuario
       (para memoria a largo plazo del tarotista)

2. Crea un script `backend/scripts/seed_knowledge.py` que:
   - Carga el conocimiento base desde archivos JSON en `backend/data/knowledge/`
   - Genera embeddings usando la API de Google (text-embedding-004) o sentence-transformers
     como fallback gratuito
   - Inserta todos los documentos en LanceDB
   - Muestra progreso y maneja errores de rate limit con retry exponencial

3. Crea los archivos de conocimiento base en `backend/data/knowledge/`:
   - `tarot_cards.json`: las 78 cartas del Tarot Rider-Waite con:
     * name, arcana (major/minor), suit, number
     * meaning_upright, meaning_reversed
     * keywords (lista), archetype, element
     * description_es (descripción poética en español)
   - `life_numbers.json`: números de vida 1-9 + 11, 22, 33 con:
     * number, name, description, strengths, challenges, famous_people, keywords

4. Actualiza `backend/app/services/ai.py` para usar RAG:
   - Antes de llamar a Gemini, busca en LanceDB los documentos más relevantes
     usando la pregunta del usuario como query
   - Incluye también el contexto personal del usuario (onboarding_answers, historial)
   - Construye el prompt final: [system_prompt] + [rag_context] + [user_context] + [question]
   - El system_prompt debe adaptar la personalidad del tarotista según onboarding_answers

5. Crea tests en `backend/tests/unit/test_vector_store.py`:
   - Que la búsqueda semántica devuelva resultados relevantes
   - Que el contexto del usuario se recupera correctamente
   - Que el RAG mejora la calidad del prompt (verifica que el prompt contiene
     el contexto relevante)

Restricciones:
- El RAG debe funcionar completamente offline para tests (usa embeddings pre-calculados)
- Maneja el caso donde LanceDB no está inicializado (fallback a prompt sin contexto)
- Documenta el schema de cada colección en un `README_KNOWLEDGE.md`
```

---

## 📱 PROMPT 5 — Frontend Flutter: Onboarding + Lectura Diaria

```
Contexto del proyecto:
CosmoTarot es una app de tarot/numerología/IA. El backend está listo en FastAPI.
Ahora necesito construir el frontend en Flutter. La app debe ser muy visual,
con animaciones fluidas y una estética mística/esotérica (colores oscuros, dorados,
púrpuras, fuente serif elegante).

Tu tarea — construye estas pantallas en Flutter:

--- PANTALLA 1: Splash Screen ---
- Fondo negro profundo con animación de partículas/estrellas (usa el paquete `particles_flutter`)
- Logo de CosmoTarot aparece con fade-in
- Transición automática a Onboarding (primera vez) o Home (ya registrado)

--- PANTALLA 2: Onboarding / Registro ---
Flujo de 5 pasos (usa `PageView` con animación de transición):

Paso 1 — Bienvenida:
- Texto: "Bienvenido/a al cosmos" con animación typewriter
- Botón "Comenzar mi viaje"

Paso 2 — Datos personales:
- Campo: Nombre completo
- Campo: Email
- Campo: Contraseña
- DatePicker estilizado para fecha de nacimiento (debe verse místico, no el picker default)

Paso 3 — Datos astrológicos (opcionales):
- Campo: Hora de nacimiento (TimePicker)
- Campo: Ciudad de nacimiento (con autocomplete)
- Texto explicativo: "Esto nos permite crear tu carta natal completa"

Paso 4 — Las 3 preguntas de personalización:
Cada pregunta en su propia card animada que hace flip al seleccionar:
- "¿Qué área de tu vida busca guía?" → opciones: Amor, Trabajo, Vida personal, Espiritual
- "¿Cómo prefieres que te hable tu tarotista?" → opciones: Directa, Reflexiva, Poética
- "¿Cómo ves el destino?" → opciones: Todo está escrito, Tú decides, Es un equilibrio

Paso 5 — Tu número de vida:
- Animación que "calcula" el número (efecto de números rodando)
- Muestra el número grande con su nombre y descripción corta
- Botón "Comenzar"

--- PANTALLA 3: Home / Lectura Diaria ---
- Header con: saludo personalizado ("Buenos días, [nombre]") + icono de perfil
- Sección principal: "Tu lectura de hoy"
  * 3 cartas boca abajo con animación de volteo al tocar (una por una)
  * Cada carta muestra su imagen + nombre + significado breve
  * Botón "Ver interpretación completa" que abre bottom sheet con texto de la IA
- Sección secundaria: "Tu número de vida" — card compacta
- Sección: "Pregunta a tu tarotista" — chat input con límite diario visible
  * Muestra: "Te queda 1 pregunta gratuita hoy" o "Preguntas ilimitadas ✨" (premium)

--- COMPONENTES REUTILIZABLES ---
Crea en `lib/widgets/`:
- `TarotCardWidget`: carta con flip animation, frente y reverso
- `MysticButton`: botón con estilo dorado/oscuro y glow effect
- `CosmicBackground`: fondo animado reutilizable
- `LifeNumberBadge`: badge con el número de vida del usuario

--- ARQUITECTURA ---
- Usa Riverpod para state management
- Usa `go_router` para navegación
- Crea `lib/services/api_service.dart` con todos los calls al backend FastAPI
- Guarda el JWT en `flutter_secure_storage`
- Maneja estados: loading, error, success en cada pantalla

--- TEMA VISUAL ---
Paleta de colores:
- Background: #0A0A1A (negro azulado profundo)
- Primary: #C9A84C (dorado místico)
- Secondary: #7B2FBE (púrpura)
- Accent: #E8D5B7 (crema/pergamino)
- Text: #F0E6D3 (blanco cálido)
Fuentes: Cinzel (serif, títulos) + Lato (sans-serif, cuerpo)

Restricciones:
- Flutter 3.x con null safety
- Diseño responsive para iOS y Android
- Todos los textos en español
- Animaciones deben ser fluidas (60fps), usa AnimatedBuilder o Lottie para efectos complejos
- Añade comentarios en el código explicando las animaciones
```

---

## 💳 PROMPT 6 — Integración RevenueCat (Monetización)

```
Contexto del proyecto:
CosmoTarot necesita monetización via suscripción. Vamos a usar RevenueCat para manejar
las suscripciones en iOS y Android desde un único lugar.

Planes de suscripción:
- Free: 1 pregunta/día al tarotista, lectura diaria de 3 cartas, número de vida
- Premium ($4.44/mes o $44.44/año): preguntas ilimitadas, lecturas ilimitadas,
  carta natal completa, historial, compatibilidad

Tu tarea tiene dos partes:

--- PARTE BACKEND ---
1. Crea `backend/app/api/webhooks.py`:
   - POST /webhooks/revenuecat — recibe eventos de RevenueCat
   - Verifica la firma del webhook (header X-RevenueCat-Signature)
   - Maneja los eventos:
     * INITIAL_PURCHASE → activa premium en tabla subscriptions
     * RENEWAL → renueva la fecha de expiración
     * CANCELLATION → marca is_active=False al vencer
     * EXPIRATION → desactiva premium
   - Responde 200 rápido y procesa en background (usa BackgroundTasks de FastAPI)

2. Actualiza `backend/app/services/limits.py`:
   - check_user_limits(user_id) → verifica plan activo consultando tabla subscriptions
   - Cachea el resultado por 5 minutos para no consultar la BD en cada request

3. Tests para el webhook:
   - Simula cada tipo de evento con firma válida → verifica que el estado cambia
   - Simula evento con firma inválida → debe dar 401
   - Simula CANCELLATION → usuario pierde acceso premium al día siguiente

--- PARTE FLUTTER ---
4. Crea `lib/services/subscription_service.dart`:
   - Inicializa RevenueCat SDK con la API key
   - getOfferings() → obtiene los planes disponibles
   - purchasePackage(package) → inicia el flujo de compra
   - restorePurchases() → restaura compras anteriores
   - getCurrentEntitlements() → verifica si el usuario es premium

5. Crea `lib/screens/paywall_screen.dart`:
   - Pantalla de paywall mística y atractiva
   - Muestra comparativa Free vs Premium
   - Precio $4.44/mes o $44.44/año (destaca el ahorro anual)
   - Los precios con "4" son intencionales (numerología del número 4: estabilidad, fundamento)
   - Botón de compra con animación
   - Texto: "Cancela cuando quieras"
   - Opción "Restaurar compras"

6. Integra el paywall en el flujo:
   - Cuando usuario free intenta hacer la 2da pregunta del día → muestra paywall
   - Botón "Desbloquear premium" en el Home
   - Manejo de estados: purchasing, success, error, cancelled

Restricciones:
- Usa el paquete oficial `purchases_flutter`
- Maneja todos los errores de compra con mensajes amigables en español
- El backend nunca confía en el cliente para verificar premium: siempre verifica via webhook
- Añade tests de integración para los flujos de compra y cancelación (con mocks de RevenueCat)
```

---

## 📋 QA_STRATEGY.md — Plantilla Base

```markdown
# CosmoTarot — QA Strategy

## Pirámide de Testing

           /\
          /  \  E2E (10%)
         /----\
        /      \  Integration (30%)
       /--------\
      /          \  Unit Tests (60%)
     /------------\

## Herramientas

| Tipo | Herramienta |
|------|-------------|
| Unit & Integration | pytest + pytest-asyncio |
| Mocking | pytest-mock + responses |
| Coverage | pytest-cov + Codecov |
| Linting | ruff + black |
| Type checking | mypy |
| Security | bandit + safety |
| CI/CD | GitHub Actions |
| API Testing | httpx (async) |

## Cómo correr los tests

# Todos los tests
pytest --cov=app --cov-report=html

# Solo unitarios
pytest tests/unit/ -v

# Solo integración (requiere PostgreSQL)
pytest tests/integration/ -v

# Con reporte de cobertura
pytest --cov=app --cov-report=term-missing

## Métricas de calidad objetivo

- Coverage: ≥ 80%
- 0 vulnerabilidades críticas (bandit)
- 0 errores de tipo (mypy)
- Tiempo de pipeline: < 5 minutos
```

---

*Documento generado para CosmoTarot — Todos los prompts están listos para usar en cualquier asistente de código (Claude, Cursor, GitHub Copilot). Úsalos en orden para garantizar que cada capa del proyecto esté bien construida antes de la siguiente.*
