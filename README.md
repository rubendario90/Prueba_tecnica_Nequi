# Prueba Técnica Nequi 🚀

Bienvenido a **Prueba Técnica Nequi**, una API robusta y escalable para el procesamiento de mensajes de chat construida con FastAPI. Este proyecto demuestra habilidades avanzadas en desarrollo backend, manejo de datos, arquitectura limpia y buenas prácticas de programación.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso de la API](#-uso-de-la-api)
- [Documentación de la API](#-documentación-de-la-api)
- [Autenticación](#-autenticación)
- [Testing](#-testing)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración Avanzada](#-configuración-avanzada)

## ✨ Características Principales

- **🔄 Procesamiento de mensajes en tiempo real** - Recepción, validación y procesamiento de mensajes de chat
- **🛡️ Validación robusta** - Validación de formato y filtrado de contenido inapropiado
- **📊 Metadata automática** - Cálculo automático de estadísticas (conteo de palabras, caracteres, timestamps)
- **🗄️ Persistencia de datos** - Almacenamiento en SQLite con SQLAlchemy ORM 
- **🔐 Autenticación segura** - Sistema de API Keys para proteger endpoints
- **📄 Paginación inteligente** - Consultas eficientes con soporte para paginación
- **🕐 Manejo de zonas horarias** - Conversión automática a horario de Bogotá
- **🎯 Filtrado avanzado** - Filtros por sesión, remitente y otros criterios
- **📝 Documentación automática** - Documentación interactiva con Swagger/OpenAPI
- **✅ Testing completo** - Suite completa de tests unitarios y de integración

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una **arquitectura limpia (Clean Architecture)** con separación clara de responsabilidades:

```
📦 Prueba_tecnica_Nequi/
├── 🚀 main.py                    # Punto de entrada de la aplicación
├── 📋 requirements.txt           # Dependencias del proyecto
├── 🧪 tests/                     # Suite de tests
├── 📁 app/
│   ├── 🌐 api/                   # Controladores/Endpoints
│   │   └── messages.py           # Endpoints de mensajes
│   ├── ⚙️ core/                  # Configuración central
│   │   ├── config.py             # Configuraciones
│   │   └── errors.py             # Manejo de errores
│   ├── 🗄️ db/                    # Capa de base de datos
│   │   └── database.py           # Configuración SQLAlchemy
│   ├── 📊 models/                # Modelos de datos
│   │   ├── message.py            # Modelo de mensaje
│   │   └── metadata.py           # Modelo de metadata
│   ├── 🏪 repository/            # Capa de acceso a datos
│   │   └── message_repository.py # Repositorio de mensajes
│   └── 🔧 services/              # Lógica de negocio
│       └── message_service.py    # Servicio de mensajes
```

## 🔧 Requisitos Previos

- **Python 3.8+** (Recomendado: Python 3.10 o superior)
- **pip** (Gestor de paquetes de Python)
- **Git** (Para clonar el repositorio)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/rubendario90/Prueba_tecnica_Nequi.git
cd Prueba_tecnica_Nequi
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

La aplicación utiliza SQLite y se configura automáticamente al iniciar:

```bash
# La base de datos se crea automáticamente al ejecutar la aplicación
# Archivo: messages.db
```

### 5. Ejecutar la Aplicación

```bash
# Ejecutar con Uvicorn
python -m uvicorn main:app --reload --port 8000

# O usando FastAPI CLI (si está disponible)
fastapi run main.py --port 8000
```

La aplicación estará disponible en: **http://localhost:8000**

### 6. Verificar Instalación

```bash
# Verificar que la API responde
curl http://localhost:8000/

# Respuesta esperada:
{
  "mensaje": "API inicializada correctamente",
  "version": "1.0.0"
}
```

## 📖 Uso de la API

### Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Endpoints Principales

#### 1. Información de la API
```bash
GET /
```

#### 2. Crear un Mensaje
```bash
POST /api/messages
Content-Type: application/json

{
  "message_id": "msg-001",
  "session_id": "session-123", 
  "content": "Hola, ¿cómo estás?",
  "timestamp": "2024-01-15T10:30:00Z",
  "sender": "user"
}
```

#### 3. Obtener Mensajes por Sesión
```bash
GET /api/messages/{session_id}?sender=user&limit=10&offset=0
```

#### 4. Autenticación
```bash
POST /login
Content-Type: application/json

{
  "api_key": "mi_api_key_secreta"
}
```

#### 5. Endpoint Protegido (Requiere API Key)
```bash
GET /protegido
X-API-Key: mi_api_key_secreta
```

## 📚 Documentación de la API

### Modelos de Datos

#### MessageCreate (Request)
```json
{
  "message_id": "string",      // ID único del mensaje
  "session_id": "string",      // ID de la sesión de chat
  "content": "string",         // Contenido del mensaje
  "timestamp": "datetime",     // Timestamp en formato ISO 8601
  "sender": "user|system"      // Remitente del mensaje
}
```

#### MessageResponse (Response)
```json
{
  "message_id": "string",
  "session_id": "string", 
  "content": "string",
  "timestamp": "datetime",
  "sender": "user|system",
  "metadata": {
    "word_count": "integer",     // Número de palabras
    "character_count": "integer", // Número de caracteres
    "processed_at": "datetime"   // Timestamp de procesamiento
  }
}
```

### Ejemplos Detallados

#### Crear un Mensaje de Usuario

**Request:**
```bash
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-user-001",
    "session_id": "chat-session-123",
    "content": "¡Hola! Necesito ayuda con mi cuenta.",
    "timestamp": "2024-01-15T14:30:00Z",
    "sender": "user"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-user-001",
    "session_id": "chat-session-123",
    "content": "¡Hola! Necesito ayuda con mi cuenta.",
    "timestamp": "2024-01-15T14:30:00",
    "sender": "user",
    "metadata": {
      "word_count": 7,
      "character_count": 38,
      "processed_at": "2024-01-15T14:30:05.123456"
    }
  }
}
```

#### Crear un Mensaje del Sistema

**Request:**
```bash
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-system-001", 
    "session_id": "chat-session-123",
    "content": "Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?",
    "timestamp": "2024-01-15T14:30:10Z",
    "sender": "system"
  }'
```

#### Obtener Mensajes de una Sesión

**Request:**
```bash
curl "http://localhost:8000/api/messages/chat-session-123?sender=user&limit=5&offset=0"
```

**Response:**
```json
{
  "status": "success", 
  "data": [
    {
      "message_id": "msg-user-001",
      "session_id": "chat-session-123",
      "content": "¡Hola! Necesito ayuda con mi cuenta.",
      "timestamp": "2024-01-15T14:30:00",
      "sender": "user",
      "metadata": {
        "word_count": 7,
        "character_count": 38,
        "processed_at": "2024-01-15T14:30:05.123456"
      }
    }
  ],
  "pagination": {
    "limit": 5,
    "offset": 0,
    "total": 1
  }
}
```

#### Manejo de Errores

**Error de Validación:**
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Message contains inappropriate content",
    "details": "The word 'spam' is not allowed"
  }
}
```

**Error de Duplicado:**
```json
{
  "status": "error", 
  "error": {
    "code": "DUPLICATE_RESOURCE",
    "message": "Message with ID msg-001 already exists",
    "details": null
  }
}
```

## 🔐 Autenticación

La API utiliza **API Keys** para autenticación en endpoints protegidos.

### Configuración de API Key

```python
# En main.py
API_KEY = "mi_api_key_secreta"  # ⚠️ Cambiar en producción
```

### Uso de API Key

```bash
# En headers de la request
curl -H "X-API-Key: mi_api_key_secreta" http://localhost:8000/protegido
```

### Endpoint de Login

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "mi_api_key_secreta"}'
```

## ✅ Testing

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar con coverage
python -m pytest --cov=app tests/

# Ejecutar tests específicos
python -m pytest tests/test_api.py -v

# Ejecutar tests con output detallado
python -m pytest -v -s
```

### Estructura de Tests

```
tests/
├── conftest.py              # Configuración de fixtures
├── test_api.py              # Tests de endpoints
├── test_models.py           # Tests de modelos
├── test_repository.py       # Tests de repositorio  
└── test_services.py         # Tests de servicios
```

### Coverage Report

```bash
# Generar reporte de coverage HTML
python -m pytest --cov=app --cov-report=html tests/
# Ver reporte en: htmlcov/index.html
```

## 📁 Estructura del Proyecto

```
Prueba_tecnica_Nequi/
├── 📄 README.md                     # Documentación principal
├── 📋 requirements.txt              # Dependencias
├── 🚀 main.py                      # Punto de entrada FastAPI
├── 🧪 tests/                       # Suite de tests
│   ├── conftest.py                 # Configuración de fixtures
│   ├── test_api.py                 # Tests de endpoints
│   ├── test_models.py              # Tests de modelos
│   ├── test_repository.py          # Tests de repositorio
│   └── test_services.py            # Tests de servicios
└── 📁 app/                         # Código fuente principal
    ├── 🌐 api/                     # Capa de API/Controladores
    │   └── messages.py             # Endpoints de mensajes
    ├── ⚙️ core/                    # Configuración central
    │   ├── config.py               # Configuraciones de la app
    │   └── errors.py               # Clases de errores personalizados
    ├── 🗄️ db/                      # Capa de base de datos
    │   └── database.py             # Configuración SQLAlchemy
    ├── 📊 models/                  # Modelos de datos
    │   ├── message.py              # Modelo de mensaje y DTOs
    │   └── metadata.py             # Modelo de metadata
    ├── 🏪 repository/              # Capa de acceso a datos
    │   └── message_repository.py   # Repositorio de mensajes
    └── 🔧 services/                # Lógica de negocio
        └── message_service.py      # Servicio de procesamiento
```

### Descripción de Componentes

#### 🌐 API Layer (`app/api/`)
- **messages.py**: Endpoints REST para operaciones con mensajes
- Manejo de requests/responses HTTP
- Validación de entrada y serialización

#### ⚙️ Core (`app/core/`)
- **config.py**: Configuraciones centralizadas (palabras prohibidas, paginación, etc.)
- **errors.py**: Clases de error personalizadas y manejo de excepciones

#### 🗄️ Database (`app/db/`)
- **database.py**: Configuración SQLAlchemy, motor de BD, sesiones

#### 📊 Models (`app/models/`)
- **message.py**: Modelos Pydantic y SQLAlchemy para mensajes
- Validadores personalizados y tipos de datos

#### 🏪 Repository (`app/repository/`)
- **message_repository.py**: Capa de acceso a datos
- Operaciones CRUD, consultas optimizadas

#### 🔧 Services (`app/services/`)
- **message_service.py**: Lógica de negocio principal  
- Procesamiento, validación, filtrado de contenido

## ⚙️ Configuración Avanzada

### Variables de Configuración

**Archivo: `app/core/config.py`**

```python
# Filtrado de contenido
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", 
    "phishing", "scam", "fraud", "abuse", 
    "harassment", "hate", "threat", "violence"
]

# Paginación
DEFAULT_PAGE_SIZE = 10  # Elementos por página por defecto
MAX_PAGE_SIZE = 100     # Máximo elementos por página

# API
API_VERSION = "1.0.0"
API_TITLE = "Message Processing API"
API_DESCRIPTION = "A simple API for processing chat messages"
```

### Base de Datos

**Configuración SQLite:**
```python
# app/db/database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"
```

**Para PostgreSQL (Producción):**
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### Zona Horaria

La aplicación maneja automáticamente la conversión a zona horaria de Bogotá:

```python
# Conversión automática en BogotaDateTime
bogota_dt = value.astimezone(ZoneInfo("America/Bogota"))
```

### Filtrado de Contenido

Las palabras inapropiadas se validan automáticamente:

```python
# Lista personalizable en config.py
INAPPROPRIATE_WORDS = ["spam", "malware", ...]

# Validación en message_service.py
def _validate_content(self, content: str) -> None:
    content_lower = content.lower()
    for word in INAPPROPRIATE_WORDS:
        if word in content_lower:
            raise ValidationError(f"The word '{word}' is not allowed")
```

### Paginación

```python
# Parámetros configurables
DEFAULT_PAGE_SIZE = 10    # Por defecto
MAX_PAGE_SIZE = 100       # Límite máximo

# Uso en endpoints
@router.get("/messages/{session_id}")
async def get_messages(
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    offset: int = Query(0, ge=0)
):
```

## 🔧 Desarrollo y Contribución

### Configurar Entorno de Desarrollo

```bash
# 1. Clonar repositorio
git clone https://github.com/rubendario90/Prueba_tecnica_Nequi.git
cd Prueba_tecnica_Nequi

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar tests
python -m pytest

# 5. Ejecutar aplicación
python -m uvicorn main:app --reload
```

### Comandos Útiles

```bash
# Linter y formato de código
pip install black flake8
black app/ tests/
flake8 app/ tests/

# Análisis de seguridad
pip install bandit
bandit -r app/

# Generar requirements.txt
pip freeze > requirements.txt
```

## 🚀 Despliegue

### Despliegue Local

```bash
# Con Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Con Gunicorn (Producción)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (Opcional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Soporte y Contacto

Para preguntas, problemas o sugerencias:

- **GitHub Issues**: [Crear Issue](https://github.com/rubendario90/Prueba_tecnica_Nequi/issues)
- **Email**: rubendario90@example.com (reemplazar con email real)

## 📄 Licencia

Este proyecto es parte de una prueba técnica y está disponible para fines educativos.

---

**Desarrollado con ❤️ para Nequi**
