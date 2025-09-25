# Prueba Técnica Nequi 🚀

Bienvenido a **Prueba Técnica Nequi**, una API RESTful completa para el procesamiento de mensajes de chat. Este proyecto demuestra habilidades clave en desarrollo backend con Python, incluyendo arquitectura limpia, manejo de errores robusto, y pruebas exhaustivas.

## ✨ Características principales

- **Recepción de mensajes de chat:** API RESTful para recibir y procesar mensajes en tiempo real
- **Validación completa:** Validación de formato de mensajes con Pydantic
- **Filtrado de contenido:** Sistema de filtrado para contenido inapropiado
- **Procesamiento de metadatos:** Cálculo automático de estadísticas de mensajes
- **Almacenamiento persistente:** Base de datos SQLite para almacenar mensajes
- **Paginación y filtrado:** Soporte completo para paginación y filtrado por remitente
- **Manejo de errores robusto:** Respuestas de error consistentes y descriptivas
- **Arquitectura limpia:** Separación clara de responsabilidades con patrones SOLID
- **Cobertura de pruebas >92%:** Suite completa de pruebas unitarias e integración

## 🛠️ Stack Tecnológico

- **Python 3.10+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para manejo de base de datos
- **SQLite** - Base de datos ligera para desarrollo
- **Pydantic** - Validación de datos y serialización
- **Pytest** - Framework de pruebas
- **Coverage** - Análisis de cobertura de código

## 📋 Requisitos

- Python 3.10 o superior
- pip (para manejo de dependencias)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/rubendario90/Prueba_tecnica_Nequi.git
cd Prueba_tecnica_Nequi
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://localhost:8000`

## 📖 Documentación de la API

### Información General
- **Versión:** 1.0.0
- **Base URL:** `http://localhost:8000`
- **Documentación interactiva:** `http://localhost:8000/docs`

### Endpoints Principales

#### 1. Crear Mensaje
**POST** `/api/messages`

Crea un nuevo mensaje con validación y procesamiento automático.

**Request Body:**
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 5,
      "character_count": 31,
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}
```

**Response Error (400):**
```json
{
  "detail": {
    "status": "error",
    "error": {
      "code": "INVALID_FORMAT",
      "message": "Message contains inappropriate content",
      "details": "The word 'spam' is not allowed"
    }
  }
}
```

#### 2. Obtener Mensajes por Sesión
**GET** `/api/messages/{session_id}`

Recupera mensajes para una sesión específica con soporte para filtrado y paginación.

**Parámetros de consulta:**
- `sender` (opcional): Filtrar por remitente (`user` o `system`)
- `limit` (opcional): Número de mensajes por página (1-100, por defecto: 10)
- `offset` (opcional): Número de mensajes a omitir (por defecto: 0)

**Ejemplo:**
```
GET /api/messages/session-abcdef?sender=user&limit=5&offset=0
```

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "message_id": "msg-123456",
      "session_id": "session-abcdef",
      "content": "Hola, ¿cómo puedo ayudarte hoy?",
      "timestamp": "2023-06-15T14:30:00Z",
      "sender": "system",
      "metadata": {
        "word_count": 5,
        "character_count": 31,
        "processed_at": "2023-06-15T14:30:01Z"
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

### Esquema de Mensaje

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `message_id` | string | Identificador único del mensaje | ✅ |
| `session_id` | string | Identificador de sesión | ✅ |
| `content` | string | Contenido del mensaje | ✅ |
| `timestamp` | datetime | Marca de tiempo ISO 8601 | ✅ |
| `sender` | enum | Remitente: `"user"` o `"system"` | ✅ |

### Metadatos Generados Automáticamente

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `word_count` | integer | Número de palabras en el mensaje |
| `character_count` | integer | Número de caracteres en el mensaje |
| `processed_at` | datetime | Timestamp de procesamiento |

### Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 400 | Error de validación o formato inválido |
| 409 | Recurso duplicado (mensaje con ID existente) |
| 422 | Error de validación de datos |
| 500 | Error interno del servidor |

## 🧪 Pruebas

### Ejecutar todas las pruebas
```bash
python -m pytest tests/ -v
```

### Ejecutar pruebas con reporte de cobertura
```bash
python -m coverage run -m pytest tests/
python -m coverage report --include="app/*,main.py"
```

### Tipos de pruebas incluidas
- **Pruebas unitarias:** Servicios, repositorios y modelos
- **Pruebas de integración:** Endpoints de API completos
- **Pruebas de validación:** Validación de datos de entrada
- **Pruebas de manejo de errores:** Casos de error y excepciones

**Cobertura actual: 92%** ✅ (>80% requerido)

## 🏗️ Arquitectura

### Estructura del Proyecto
```
Prueba_tecnica_Nequi/
├── app/
│   ├── api/          # Endpoints y controladores
│   ├── core/         # Configuración y manejo de errores
│   ├── db/           # Configuración de base de datos
│   ├── models/       # Modelos de datos (Pydantic y SQLAlchemy)
│   ├── repository/   # Capa de acceso a datos
│   └── services/     # Lógica de negocio
├── tests/            # Suite de pruebas
├── main.py           # Punto de entrada de la aplicación
└── requirements.txt  # Dependencias
```

### Principios de Diseño
- **Separación de responsabilidades:** Cada capa tiene una responsabilidad específica
- **Inversión de dependencias:** Las dependencias se inyectan desde capas superiores
- **Principio abierto/cerrado:** Extensible sin modificar código existente
- **Responsabilidad única:** Cada clase tiene una sola razón para cambiar

## 🔧 Configuración

### Variables de Configuración (app/core/config.py)
- **INAPPROPRIATE_WORDS:** Lista de palabras prohibidas para filtrado
- **DEFAULT_PAGE_SIZE:** Tamaño de página por defecto (10)
- **MAX_PAGE_SIZE:** Tamaño máximo de página (100)

### Base de Datos
- **Motor:** SQLite
- **Archivo:** `messages.db` (creado automáticamente)
- **Migración:** Tablas creadas automáticamente al iniciar

## 🔍 Funcionalidades Avanzadas

### Filtrado de Contenido
El sistema incluye un filtro básico para palabras inapropiadas:
- Palabras prohibidas configurables
- Validación en tiempo real
- Mensajes de error descriptivos

### Paginación
- Soporte completo para paginación con `limit` y `offset`
- Metadatos de paginación en las respuestas
- Límites configurables para prevenir sobrecarga

### Manejo de Errores
- Códigos de error consistentes
- Mensajes descriptivos en español
- Detalles técnicos para debugging
- Logging estructurado

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de tabla no encontrada**
   ```
   Solución: La aplicación crea las tablas automáticamente al iniciar
   ```

2. **Error de validación de datos**
   ```
   Verificar que todos los campos requeridos estén presentes
   Confirmar que el formato de timestamp sea ISO 8601
   ```

3. **Error de contenido inapropiado**
   ```
   Revisar la lista de palabras prohibidas en app/core/config.py
   ```

## 🚀 Mejoras Futuras

### Implementaciones Opcionales
- **Autenticación:** Sistema de autenticación con JWT
- **WebSocket:** Actualizaciones en tiempo real
- **Búsqueda:** Motor de búsqueda de mensajes
- **Docker:** Contenederización para despliegue
- **Rate Limiting:** Limitación de tasa de peticiones
- **IaC:** Infraestructura como código con Terraform

## 👥 Contribución

Este proyecto fue desarrollado como parte de una evaluación técnica para Nequi, demostrando competencias en:

- ✅ Diseño e implementación de APIs RESTful
- ✅ Desarrollo backend con Python y FastAPI
- ✅ Manejo robusto de errores y validación
- ✅ Pruebas unitarias e integración exhaustivas
- ✅ Documentación completa y clara
- ✅ Arquitectura limpia y mantenible

## 📞 Contacto

**Desarrollador:** Rubén Darío  
**Repositorio:** [https://github.com/rubendario90/Prueba_tecnica_Nequi](https://github.com/rubendario90/Prueba_tecnica_Nequi)

---

¡Gracias por revisar este proyecto! 🙏
