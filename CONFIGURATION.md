# ⚙️ Guía de Configuración del Sistema

Esta guía proporciona información completa sobre la configuración del **Message Processing API**, incluyendo variables de entorno, configuración de base de datos, autenticación y parámetros del sistema.

## 📋 Tabla de Contenidos

- [Variables de Configuración Disponibles](#variables-de-configuración-disponibles)
- [Configuración de Base de Datos](#configuración-de-base-de-datos)
- [Configuración de Autenticación](#configuración-de-autenticación)
- [Variables de Entorno](#variables-de-entorno)
- [Configuración de la API](#configuración-de-la-api)
- [Configuración de Contenido](#configuración-de-contenido)
- [Configuración de Paginación](#configuración-de-paginación)

## 🛠️ Variables de Configuración Disponibles

### Configuración Principal de la API

Las configuraciones principales se encuentran en `app/core/config.py`:

```python
# Información de la API
API_VERSION = "1.0.0"
API_TITLE = "Message Processing API"
API_DESCRIPTION = "A simple API for processing chat messages"

# Configuración de paginación
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Filtrado de contenido
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", "phishing", "scam",
    "fraud", "abuse", "harassment", "hate", "threat", "violence"
]
```

### Configuración en main.py

```python
# Clave de API (debe configurarse como variable de entorno en producción)
API_KEY = "mi_api_key_secreta"
```

## 🗄️ Configuración de Base de Datos

### SQLite (Configuración por defecto)

El sistema utiliza SQLite por defecto con la siguiente configuración en `app/db/database.py`:

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
```

### Configuración para Producción

Para entornos de producción, se recomienda usar PostgreSQL o MySQL:

#### PostgreSQL
```python
# Ejemplo de configuración con PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:contraseña@localhost/messages_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

#### MySQL
```python
# Ejemplo de configuración con MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/messages_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

### Configuración de Zona Horaria

El sistema utiliza la zona horaria de Bogotá por defecto. La configuración se maneja automáticamente en `app/models/message.py`:

```python
class BogotaDateTime(TypeDecorator):
    """Convierte datetime con timezone a UTC naive para compatibilidad con SQLite."""
    
    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is not None:
            bogota_dt = value.astimezone(ZoneInfo("America/Bogota")).replace(tzinfo=None)
            return bogota_dt
        return value
```

## 🔐 Configuración de Autenticación

### API Key Authentication

El sistema utiliza autenticación basada en API Key mediante el header `X-API-Key`.

#### Configuración Actual
```python
API_KEY = "mi_api_key_secreta"
api_key_header = APIKeyHeader(name="X-API-Key")

def verificar_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
```

#### Uso en Endpoints Protegidos
```python
@app.get("/protegido")
def vista_protegida(dep: None = Depends(verificar_api_key)):
    return {"mensaje": "Acceso autorizado a la vista protegida"}
```

#### Endpoints de Autenticación
```python
@app.post("/login")
async def login(request: LoginRequest):
    if request.api_key == API_KEY:
        return {"mensaje": "Autenticación exitosa"}
    else:
        raise HTTPException(status_code=401, detail="API Key inválida")
```

## 🌍 Variables de Entorno

Para una configuración más segura en producción, se recomienda usar variables de entorno:

### Archivo .env (recomendado)
```bash
# Configuración de la API
API_KEY=tu_api_key_super_secreta
API_TITLE=Message Processing API
API_VERSION=1.0.0
API_DESCRIPTION=A simple API for processing chat messages

# Configuración de Base de Datos
DATABASE_URL=sqlite:///./messages.db
# Para producción:
# DATABASE_URL=postgresql://usuario:contraseña@localhost/messages_db

# Configuración de Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Configuración de Paginación
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100

# Configuración de Contenido
ENABLE_CONTENT_FILTER=true
```

### Implementación de Variables de Entorno

Para usar variables de entorno, modifica `app/core/config.py`:

```python
import os
from typing import List

# Configuración de la API
API_KEY = os.getenv("API_KEY", "mi_api_key_secreta")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = os.getenv("API_TITLE", "Message Processing API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "A simple API for processing chat messages")

# Configuración de Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./messages.db")

# Configuración de Servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Configuración de Paginación
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "10"))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))

# Configuración de Filtrado de Contenido
ENABLE_CONTENT_FILTER = os.getenv("ENABLE_CONTENT_FILTER", "true").lower() == "true"

INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", "phishing", "scam",
    "fraud", "abuse", "harassment", "hate", "threat", "violence"
]
```

## 🚀 Configuración de la API

### FastAPI Configuration

```python
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    # Configuraciones adicionales recomendadas
    docs_url="/docs",           # Swagger UI
    redoc_url="/redoc",         # ReDoc
    openapi_url="/openapi.json" # OpenAPI Schema
)
```

### Configuración de CORS (opcional)

Para aplicaciones web, puedes habilitar CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Configuración de Logging

```python
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

## 📄 Configuración de Contenido

### Filtro de Palabras Inapropiadas

El sistema incluye un filtro de contenido configurado en `app/core/config.py`:

```python
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", "phishing", "scam",
    "fraud", "abuse", "harassment", "hate", "threat", "violence"
]
```

### Personalización del Filtro

Para personalizar las palabras filtradas:

1. **Modificar la lista directamente:**
```python
INAPPROPRIATE_WORDS = [
    "palabra1", "palabra2", "palabra3"
]
```

2. **Cargar desde archivo:**
```python
def load_inappropriate_words():
    try:
        with open("inappropriate_words.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return ["spam", "malware", "virus"]  # palabras por defecto

INAPPROPRIATE_WORDS = load_inappropriate_words()
```

3. **Cargar desde variable de entorno:**
```python
import os

INAPPROPRIATE_WORDS = os.getenv("INAPPROPRIATE_WORDS", "spam,malware,virus").split(",")
```

## 📊 Configuración de Paginación

### Parámetros de Paginación

```python
# Configuración por defecto
DEFAULT_PAGE_SIZE = 10  # Número de elementos por página por defecto
MAX_PAGE_SIZE = 100     # Máximo número de elementos por página
```

### Uso en Endpoints

```python
@router.get("/messages/{session_id}")
async def get_messages(
    session_id: str,
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    # Implementación del endpoint
```

## 🔧 Configuración para Desarrollo

### Archivo de configuración de desarrollo

Crea un archivo `config/development.py`:

```python
# config/development.py
DATABASE_URL = "sqlite:///./dev_messages.db"
DEBUG = True
API_KEY = "dev_api_key"
DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 50
ENABLE_CONTENT_FILTER = False
```

### Configuración para Testing

Crea un archivo `config/testing.py`:

```python
# config/testing.py
DATABASE_URL = "sqlite:///:memory:"
DEBUG = True
API_KEY = "test_api_key"
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
ENABLE_CONTENT_FILTER = True
```

## 🏭 Configuración para Producción

### Lista de verificación para producción

- [ ] **Cambiar la API_KEY por una clave segura y aleatoria**
- [ ] **Configurar base de datos de producción (PostgreSQL/MySQL)**
- [ ] **Habilitar logging apropiado**
- [ ] **Configurar variables de entorno**
- [ ] **Deshabilitar debug mode**
- [ ] **Configurar HTTPS**
- [ ] **Configurar límites de rate limiting**

### Configuración de producción recomendada

```python
# config/production.py
import os
import secrets

# Generar API key segura
API_KEY = os.getenv("API_KEY") or secrets.token_urlsafe(32)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL debe estar configurada en producción")

DEBUG = False
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50
ENABLE_CONTENT_FILTER = True

# Configuración de logging
LOGGING_LEVEL = "INFO"
LOG_FILE = "/var/log/message_api.log"
```

## 🚀 Comando de Inicio

### Desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Con variables de entorno
```bash
export API_KEY="tu_api_key_secreta"
export DATABASE_URL="postgresql://user:pass@localhost/db"
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📝 Notas Importantes

1. **Seguridad**: Nunca hardcodees credenciales en el código fuente
2. **Base de datos**: SQLite es solo para desarrollo, usa PostgreSQL o MySQL en producción
3. **API Key**: Genera claves seguras y rota periódicamente
4. **Logging**: Configura logging apropiado para monitoreo y debugging
5. **Respaldos**: Implementa estrategias de respaldo para la base de datos
6. **Monitoreo**: Considera herramientas de monitoreo como Prometheus o DataDog

---

Para más información sobre el uso de la API, consulta [EXAMPLES.md](./EXAMPLES.md).