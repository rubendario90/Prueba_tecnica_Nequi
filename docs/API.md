# API Documentation - Message Processing API

## Información General

- **Versión**: 1.0.0
- **Base URL**: `http://localhost:8000`
- **Protocolo**: HTTP/HTTPS
- **Formato de datos**: JSON
- **Autenticación**: API Key (Header: `X-API-Key`)

## Endpoints

### 1. Root Endpoint

**Descripción**: Endpoint de verificación del estado de la API.

```
GET /
```

**Respuesta**:
```json
{
  "mensaje": "API inicializada correctamente",
  "version": "1.0.0"
}
```

**Códigos de estado**:
- `200`: OK

---

### 2. Crear Mensaje

**Descripción**: Crea un nuevo mensaje en el sistema con validación y procesamiento automático.

```
POST /api/messages
```

**Headers**:
```
Content-Type: application/json
```

**Cuerpo de la petición**:
```json
{
  "message_id": "string",      // Requerido: ID único del mensaje
  "session_id": "string",      // Requerido: ID de la sesión
  "content": "string",         // Requerido: Contenido del mensaje
  "timestamp": "datetime",     // Requerido: ISO 8601 format
  "sender": "user|system"      // Requerido: Tipo de remitente
}
```

**Ejemplo de petición**:
```json
{
  "message_id": "msg-001",
  "session_id": "session-123",
  "content": "Hola, ¿cómo puedo ayudarte?",
  "timestamp": "2024-01-15T10:30:00",
  "sender": "user"
}
```

**Respuesta exitosa** (200):
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-001",
    "session_id": "session-123",
    "content": "Hola, ¿cómo puedo ayudarte?",
    "timestamp": "2024-01-15T10:30:00",
    "sender": "user",
    "metadata": {
      "word_count": 4,
      "character_count": 27,
      "processed_at": "2024-01-15T10:30:05.123456"
    }
  }
}
```

**Códigos de estado**:
- `200`: Mensaje creado exitosamente
- `400`: Error de validación
- `409`: Mensaje duplicado (ID ya existe)
- `422`: Error de formato en los datos

**Validaciones**:
- `message_id`: No puede estar vacío, debe ser único
- `session_id`: No puede estar vacío
- `content`: No puede estar vacío, no debe contener palabras prohibidas
- `sender`: Debe ser "user" o "system"
- `timestamp`: Debe ser un datetime válido en formato ISO 8601

---

### 3. Obtener Mensajes por Sesión

**Descripción**: Recupera mensajes de una sesión específica con soporte para filtrado y paginación.

```
GET /api/messages/{session_id}
```

**Parámetros de URL**:
- `session_id` (string, requerido): ID de la sesión

**Parámetros de consulta**:
- `sender` (string, opcional): Filtrar por remitente ("user" o "system")
- `limit` (integer, opcional): Número de mensajes por página (default: 10, max: 100)
- `offset` (integer, opcional): Número de mensajes a omitir (default: 0)

**Ejemplo de petición**:
```
GET /api/messages/session-123?sender=user&limit=5&offset=0
```

**Respuesta exitosa** (200):
```json
{
  "status": "success",
  "data": [
    {
      "message_id": "msg-001",
      "session_id": "session-123",
      "content": "Hola, ¿cómo puedo ayudarte?",
      "timestamp": "2024-01-15T10:30:00",
      "sender": "user",
      "metadata": {
        "word_count": 4,
        "character_count": 27,
        "processed_at": "2024-01-15T10:30:05.123456"
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

**Códigos de estado**:
- `200`: Mensajes recuperados exitosamente
- `400`: Parámetros de consulta inválidos
- `404`: Sesión no encontrada

---

### 4. Login/Autenticación

**Descripción**: Verifica las credenciales de API Key.

```
POST /login
```

**Headers**:
```
Content-Type: application/json
```

**Cuerpo de la petición**:
```json
{
  "api_key": "string"    // Requerido: API Key
}
```

**Respuesta exitosa** (200):
```json
{
  "mensaje": "Autenticación exitosa"
}
```

**Respuesta de error** (401):
```json
{
  "detail": "API Key inválida"
}
```

**Códigos de estado**:
- `200`: Autenticación exitosa
- `401`: API Key inválida
- `422`: Formato de datos incorrecto

---

### 5. Endpoint Protegido

**Descripción**: Endpoint de ejemplo que requiere autenticación.

```
GET /protegido
```

**Headers requeridos**:
```
X-API-Key: mi_api_key_secreta
```

**Respuesta exitosa** (200):
```json
{
  "mensaje": "Acceso autorizado a la vista protegida"
}
```

**Códigos de estado**:
- `200`: Acceso autorizado
- `401`: API Key faltante o inválida

## Modelos de Datos

### MessageCreate
```json
{
  "message_id": "string",      // ID único del mensaje
  "session_id": "string",      // ID de la sesión de chat
  "content": "string",         // Contenido del mensaje
  "timestamp": "datetime",     // Timestamp en formato ISO 8601
  "sender": "user|system"      // Remitente: 'user' o 'system'
}
```

### MessageResponse
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

### MessageMetadata
```json
{
  "word_count": "integer",     // Conteo de palabras
  "character_count": "integer", // Conteo de caracteres
  "processed_at": "datetime"   // Timestamp de cuando se procesó
}
```

## Manejo de Errores

### Estructura de Error
```json
{
  "status": "error",
  "error": {
    "code": "string",      // Código de error
    "message": "string",   // Mensaje descriptivo
    "details": "string"    // Detalles adicionales (opcional)
  }
}
```

### Códigos de Error Comunes

| Código HTTP | Código Error | Descripción |
|-------------|--------------|-------------|
| 400 | `INVALID_FORMAT` | Formato de datos incorrecto |
| 401 | `UNAUTHORIZED` | API Key inválida o faltante |
| 404 | `NOT_FOUND` | Recurso no encontrado |
| 409 | `DUPLICATE_RESOURCE` | Recurso ya existe |
| 422 | `VALIDATION_ERROR` | Error de validación de datos |
| 500 | `INTERNAL_ERROR` | Error interno del servidor |

### Ejemplos de Errores

**Contenido inapropiado**:
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

**Mensaje duplicado**:
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

**API Key inválida**:
```json
{
  "detail": "API Key inválida"
}
```

## Filtrado de Contenido

La API filtra automáticamente contenido inapropiado basado en una lista de palabras prohibidas:

```
spam, malware, virus, hack, phishing, scam, 
fraud, abuse, harassment, hate, threat, violence
```

Si se detecta alguna de estas palabras, se retorna un error `400` con código `INVALID_FORMAT`.

## Límites y Cuotas

- **Paginación máxima**: 100 elementos por página
- **Paginación por defecto**: 10 elementos por página
- **Tamaño máximo de contenido**: Sin límite específico (limitado por JSON)
- **Rate limiting**: No implementado (puede agregarse en futuras versiones)

## Zona Horaria

- Todos los timestamps se convierten automáticamente a la zona horaria de Bogotá (America/Bogota)
- Los timestamps de entrada deben estar en formato ISO 8601
- Los timestamps de salida están en formato UTC sin zona horaria explícita

## Versionado

- Versión actual: `1.0.0`
- Formato de versionado: Semantic Versioning (SemVer)
- La versión se incluye en la respuesta del endpoint root (`/`)

## Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json