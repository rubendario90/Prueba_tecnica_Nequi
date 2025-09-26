# Guía de Configuración - Message Processing API

## Información General

Esta guía detalla todas las opciones de configuración disponibles para personalizar el comportamiento de la API de procesamiento de mensajes.

## Configuración de la Aplicación

### Archivo Principal: `app/core/config.py`

```python
from typing import List

# Content filtering configuration
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", "phishing", "scam",
    "fraud", "abuse", "harassment", "hate", "threat", "violence"
]

# Pagination configuration
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# API Configuration
API_VERSION = "1.0.0"
API_TITLE = "Message Processing API"
API_DESCRIPTION = "A simple API for processing chat messages"
```

## Variables de Configuración Detalladas

### 1. Filtrado de Contenido

**Variable**: `INAPPROPRIATE_WORDS`
**Tipo**: Lista de strings
**Descripción**: Lista de palabras que serán filtradas del contenido de los mensajes.

```python
# Configuración por defecto
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", 
    "phishing", "scam", "fraud", "abuse",
    "harassment", "hate", "threat", "violence"
]

# Personalización (ejemplo)
INAPPROPRIATE_WORDS = [
    # Palabras técnicas
    "spam", "malware", "virus", "hack",
    # Palabras de fraude
    "phishing", "scam", "fraud",
    # Palabras de abuso
    "abuse", "harassment", "hate", "threat", "violence",
    # Agregar palabras personalizadas
    "custom_word_1", "custom_word_2"
]
```

**Comportamiento**:
- La validación se realiza en minúsculas
- Si se encuentra alguna palabra, se lanza `ValidationError`
- La validación es sensible a substrings (ej: "spam" detecta "spammer")

### 2. Configuración de Paginación

**Variable**: `DEFAULT_PAGE_SIZE`
**Tipo**: Integer
**Valor por defecto**: 10
**Descripción**: Número de elementos que se devuelven por página cuando no se especifica el parámetro `limit`.

```python
DEFAULT_PAGE_SIZE = 10  # Cambiar según necesidades
```

**Variable**: `MAX_PAGE_SIZE`
**Tipo**: Integer  
**Valor por defecto**: 100
**Descripción**: Número máximo de elementos que se pueden solicitar en una sola página.

```python
MAX_PAGE_SIZE = 100  # Aumentar o disminuir según recursos del servidor
```

### 3. Información de la API

**Variable**: `API_VERSION`
**Tipo**: String
**Valor por defecto**: "1.0.0"
**Descripción**: Versión de la API (siguiendo Semantic Versioning).

```python
API_VERSION = "1.0.0"  # Actualizar con cada release
```

**Variable**: `API_TITLE`
**Tipo**: String
**Descripción**: Título que aparece en la documentación automática.

```python
API_TITLE = "Message Processing API"
```

**Variable**: `API_DESCRIPTION`
**Tipo**: String
**Descripción**: Descripción que aparece en la documentación automática.

```python
API_DESCRIPTION = "A simple API for processing chat messages"
```

## Configuración de Base de Datos

### Archivo: `app/db/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuración por defecto (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"

# Configuración alternativa usando variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./messages.db"
)
```

### Opciones de Base de Datos

#### SQLite (Desarrollo - Por defecto)
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
```

#### PostgreSQL (Producción)
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

#### MySQL (Alternativa)
```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

### Configuración con Variables de Entorno

**Archivo**: `.env` (crear en la raíz del proyecto)
```bash
# Base de datos
DATABASE_URL=sqlite:///./messages.db
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Key
API_KEY=mi_api_key_secreta_super_segura

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Uso en la aplicación**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# En app/db/database.py
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./messages.db")

# En main.py
API_KEY = os.getenv("API_KEY", "mi_api_key_secreta")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
```

## Configuración de Autenticación

### Archivo: `main.py`

```python
# Configuración básica
API_KEY = "mi_api_key_secreta"

# Configuración con variable de entorno (recomendado)
import os
API_KEY = os.getenv("API_KEY", "default_key_change_in_production")

# Configuración con múltiples API Keys
VALID_API_KEYS = [
    os.getenv("API_KEY_1", "key1"),
    os.getenv("API_KEY_2", "key2"),
    os.getenv("API_KEY_ADMIN", "admin_key")
]

def verificar_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API Key inválida")
```

## Configuración de Zona Horaria

### Archivo: `app/models/message.py`

```python
from zoneinfo import ZoneInfo

class BogotaDateTime(TypeDecorator):
    """Manejo de zona horaria de Bogotá"""
    
    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is not None:
            # Convertir a zona horaria de Bogotá
            bogota_dt = value.astimezone(ZoneInfo("America/Bogota"))
            return bogota_dt.replace(tzinfo=None)
        return value
```

**Personalización de zona horaria**:
```python
# Cambiar zona horaria por defecto
DEFAULT_TIMEZONE = "America/Bogota"  # Configurar según necesidades

# Ejemplos de otras zonas horarias
# DEFAULT_TIMEZONE = "America/Mexico_City"
# DEFAULT_TIMEZONE = "America/New_York" 
# DEFAULT_TIMEZONE = "UTC"
```

## Configuración del Servidor

### Desarrollo
```bash
# Servidor básico
python -m uvicorn main:app --reload

# Con configuraciones personalizadas
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info
```

### Producción

**Con Uvicorn**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

**Con Gunicorn**:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Archivo de configuración Gunicorn** (`gunicorn.conf.py`):
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
```

## Configuración de Logging

```python
import logging
from logging.config import dictConfig

# Configuración básica de logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "app.log",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["default", "file"],
    },
}

dictConfig(logging_config)
```

## Configuración Docker

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 8000

# Variables de entorno para la aplicación
ENV DATABASE_URL=sqlite:///./messages.db
ENV API_KEY=your_secure_api_key_here

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./messages.db
      - API_KEY=your_secure_api_key
    volumes:
      - ./data:/app/data
  
  # PostgreSQL (opcional)
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: messages_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Variables de Entorno Recomendadas

```bash
# .env (no incluir en git)
DATABASE_URL=postgresql://user:password@localhost:5432/messages_db
API_KEY=super_secret_api_key_change_in_production
DEBUG=False
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Configuraciones de filtrado
MAX_PAGE_SIZE=100
DEFAULT_PAGE_SIZE=10

# Configuraciones de seguridad
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

## Configuración de Seguridad

### Recomendaciones de Producción

1. **API Keys seguras**:
```python
import secrets

# Generar API key segura
API_KEY = secrets.token_urlsafe(32)
```

2. **HTTPS obligatorio**:
```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
```

3. **CORS configurado**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

4. **Rate limiting**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/messages")
@limiter.limit("10/minute")
async def create_message(request: Request, ...):
    # endpoint logic
```

## Testing de Configuración

```python
# tests/test_config.py
import pytest
from app.core.config import INAPPROPRIATE_WORDS, DEFAULT_PAGE_SIZE

def test_inappropriate_words_config():
    assert isinstance(INAPPROPRIATE_WORDS, list)
    assert len(INAPPROPRIATE_WORDS) > 0
    assert "spam" in INAPPROPRIATE_WORDS

def test_pagination_config():
    assert DEFAULT_PAGE_SIZE > 0
    assert DEFAULT_PAGE_SIZE <= 100
```

Esta guía cubre todas las opciones de configuración disponibles. Para configuraciones específicas de tu entorno, ajusta los valores según tus necesidades.