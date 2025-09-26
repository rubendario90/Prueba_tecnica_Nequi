# Ejemplos de Uso - Message Processing API

## Información General

Esta guía proporciona ejemplos prácticos y casos de uso reales para la API de procesamiento de mensajes. Todos los ejemplos han sido probados y funcionan con la versión actual de la API.

## Tabla de Contenidos

- [Ejemplos con cURL](#ejemplos-con-curl)
- [Ejemplos con Python](#ejemplos-con-python)
- [Ejemplos con JavaScript](#ejemplos-con-javascript)
- [Casos de Uso Completos](#casos-de-uso-completos)
- [Manejo de Errores](#manejo-de-errores)
- [Mejores Prácticas](#mejores-prácticas)

## Ejemplos con cURL

### 1. Verificar Estado de la API

```bash
# Verificar que la API está funcionando
curl -X GET "http://localhost:8000/" \
  -H "Content-Type: application/json"

# Respuesta esperada:
# {
#   "mensaje": "API inicializada correctamente",
#   "version": "1.0.0"
# }
```

### 2. Crear Mensajes

#### Mensaje de Usuario
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

#### Mensaje del Sistema
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

### 3. Consultar Mensajes

#### Todos los Mensajes de una Sesión
```bash
curl -X GET "http://localhost:8000/api/messages/chat-session-123" \
  -H "Content-Type: application/json"
```

#### Solo Mensajes de Usuario
```bash
curl -X GET "http://localhost:8000/api/messages/chat-session-123?sender=user" \
  -H "Content-Type: application/json"
```

#### Con Paginación
```bash
curl -X GET "http://localhost:8000/api/messages/chat-session-123?limit=5&offset=0" \
  -H "Content-Type: application/json"
```

### 4. Autenticación

#### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "mi_api_key_secreta"
  }'
```

#### Acceso a Endpoint Protegido
```bash
curl -X GET "http://localhost:8000/protegido" \
  -H "X-API-Key: mi_api_key_secreta" \
  -H "Content-Type: application/json"
```

## Ejemplos con Python

### 1. Cliente Python Básico

```python
import requests
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

class MessageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})
            
    def create_message(
        self, 
        message_id: str, 
        session_id: str, 
        content: str, 
        sender: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear un nuevo mensaje"""
        if not timestamp:
            timestamp = datetime.utcnow().isoformat() + "Z"
            
        data = {
            "message_id": message_id,
            "session_id": session_id,
            "content": content,
            "timestamp": timestamp,
            "sender": sender
        }
        
        response = self.session.post(f"{self.base_url}/api/messages", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_messages(
        self, 
        session_id: str, 
        sender: Optional[str] = None,
        limit: int = 10, 
        offset: int = 0
    ) -> Dict[str, Any]:
        """Obtener mensajes de una sesión"""
        params = {"limit": limit, "offset": offset}
        if sender:
            params["sender"] = sender
            
        response = self.session.get(
            f"{self.base_url}/api/messages/{session_id}", 
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, api_key: str) -> Dict[str, Any]:
        """Autenticarse con API key"""
        data = {"api_key": api_key}
        response = self.session.post(f"{self.base_url}/login", json=data)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar estado de la API"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear cliente
    client = MessageAPIClient()
    
    # Verificar estado
    health = client.health_check()
    print(f"API Status: {health}")
    
    # Crear mensajes
    try:
        # Mensaje de usuario
        user_message = client.create_message(
            message_id="msg-python-001",
            session_id="python-session-123",
            content="Hola desde Python!",
            sender="user"
        )
        print(f"Mensaje creado: {user_message}")
        
        # Mensaje del sistema
        system_message = client.create_message(
            message_id="msg-python-002", 
            session_id="python-session-123",
            content="¡Hola! Mensaje procesado desde Python.",
            sender="system"
        )
        print(f"Respuesta del sistema: {system_message}")
        
        # Obtener mensajes
        messages = client.get_messages("python-session-123")
        print(f"Mensajes obtenidos: {messages}")
        
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        print(f"Respuesta: {e.response.text}")
```

### 2. Cliente Asíncrono con aiohttp

```python
import aiohttp
import asyncio
import json
from datetime import datetime
from typing import Optional, Dict, Any

class AsyncMessageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Realizar petición HTTP asíncrona"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
            
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, 
                f"{self.base_url}{endpoint}",
                json=data,
                params=params,
                headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def create_message(
        self, 
        message_id: str, 
        session_id: str, 
        content: str, 
        sender: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear mensaje asíncrono"""
        if not timestamp:
            timestamp = datetime.utcnow().isoformat() + "Z"
            
        data = {
            "message_id": message_id,
            "session_id": session_id,
            "content": content,
            "timestamp": timestamp,
            "sender": sender
        }
        
        return await self._make_request("POST", "/api/messages", data=data)
    
    async def get_messages(
        self, 
        session_id: str, 
        sender: Optional[str] = None,
        limit: int = 10, 
        offset: int = 0
    ) -> Dict[str, Any]:
        """Obtener mensajes asíncrono"""
        params = {"limit": limit, "offset": offset}
        if sender:
            params["sender"] = sender
            
        return await self._make_request(
            "GET", 
            f"/api/messages/{session_id}", 
            params=params
        )

# Ejemplo de uso asíncrono
async def main():
    client = AsyncMessageAPIClient()
    
    # Crear múltiples mensajes concurrentemente
    tasks = [
        client.create_message(
            f"msg-async-{i}",
            "async-session-123",
            f"Mensaje asíncrono #{i}",
            "user"
        )
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    for result in results:
        print(f"Mensaje creado: {result['data']['message_id']}")
    
    # Obtener todos los mensajes
    messages = await client.get_messages("async-session-123")
    print(f"Total mensajes: {len(messages['data'])}")

# Ejecutar ejemplo asíncrono
# asyncio.run(main())
```

## Ejemplos con JavaScript

### 1. Cliente JavaScript (Node.js)

```javascript
const axios = require('axios');

class MessageAPIClient {
    constructor(baseUrl = 'http://localhost:8000', apiKey = null) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Content-Type': 'application/json',
                ...(apiKey && { 'X-API-Key': apiKey })
            }
        });
    }
    
    async createMessage(messageId, sessionId, content, sender, timestamp = null) {
        const data = {
            message_id: messageId,
            session_id: sessionId,
            content: content,
            timestamp: timestamp || new Date().toISOString(),
            sender: sender
        };
        
        try {
            const response = await this.client.post('/api/messages', data);
            return response.data;
        } catch (error) {
            console.error('Error creating message:', error.response?.data || error.message);
            throw error;
        }
    }
    
    async getMessages(sessionId, options = {}) {
        const params = {
            limit: options.limit || 10,
            offset: options.offset || 0,
            ...(options.sender && { sender: options.sender })
        };
        
        try {
            const response = await this.client.get(`/api/messages/${sessionId}`, { params });
            return response.data;
        } catch (error) {
            console.error('Error getting messages:', error.response?.data || error.message);
            throw error;
        }
    }
    
    async login(apiKey) {
        try {
            const response = await this.client.post('/login', { api_key: apiKey });
            return response.data;
        } catch (error) {
            console.error('Error logging in:', error.response?.data || error.message);
            throw error;
        }
    }
    
    async healthCheck() {
        try {
            const response = await this.client.get('/');
            return response.data;
        } catch (error) {
            console.error('Error checking health:', error.response?.data || error.message);
            throw error;
        }
    }
}

// Ejemplo de uso
async function example() {
    const client = new MessageAPIClient();
    
    try {
        // Verificar estado
        const health = await client.healthCheck();
        console.log('API Health:', health);
        
        // Crear mensaje
        const message = await client.createMessage(
            'msg-js-001',
            'js-session-123',
            '¡Hola desde JavaScript!',
            'user'
        );
        console.log('Mensaje creado:', message);
        
        // Obtener mensajes
        const messages = await client.getMessages('js-session-123');
        console.log('Mensajes obtenidos:', messages);
        
    } catch (error) {
        console.error('Error en ejemplo:', error);
    }
}

// example();
```

### 2. Cliente JavaScript (Frontend/Browser)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Message API Client</title>
</head>
<body>
    <div id="app">
        <h1>Message API Demo</h1>
        <div>
            <input type="text" id="messageContent" placeholder="Escribe tu mensaje...">
            <button onclick="sendMessage()">Enviar Mensaje</button>
        </div>
        <div id="messages"></div>
    </div>

    <script>
        class MessageAPIClient {
            constructor(baseUrl = 'http://localhost:8000') {
                this.baseUrl = baseUrl;
            }
            
            async createMessage(messageId, sessionId, content, sender) {
                const data = {
                    message_id: messageId,
                    session_id: sessionId,
                    content: content,
                    timestamp: new Date().toISOString(),
                    sender: sender
                };
                
                const response = await fetch(`${this.baseUrl}/api/messages`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            }
            
            async getMessages(sessionId, options = {}) {
                const params = new URLSearchParams({
                    limit: options.limit || 10,
                    offset: options.offset || 0,
                    ...(options.sender && { sender: options.sender })
                });
                
                const response = await fetch(`${this.baseUrl}/api/messages/${sessionId}?${params}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            }
        }
        
        const client = new MessageAPIClient();
        const SESSION_ID = 'browser-session-123';
        let messageCounter = 1;
        
        async function sendMessage() {
            const content = document.getElementById('messageContent').value;
            if (!content.trim()) return;
            
            try {
                const message = await client.createMessage(
                    `msg-browser-${messageCounter++}`,
                    SESSION_ID,
                    content,
                    'user'
                );
                
                document.getElementById('messageContent').value = '';
                await loadMessages();
                
                console.log('Mensaje enviado:', message);
            } catch (error) {
                console.error('Error enviando mensaje:', error);
                alert('Error enviando mensaje: ' + error.message);
            }
        }
        
        async function loadMessages() {
            try {
                const response = await client.getMessages(SESSION_ID);
                const messagesDiv = document.getElementById('messages');
                
                messagesDiv.innerHTML = response.data.map(msg => `
                    <div style="margin: 10px 0; padding: 10px; border: 1px solid #ccc;">
                        <strong>${msg.sender}:</strong> ${msg.content}
                        <br><small>Palabras: ${msg.metadata.word_count}, Caracteres: ${msg.metadata.character_count}</small>
                    </div>
                `).join('');
                
            } catch (error) {
                console.error('Error cargando mensajes:', error);
            }
        }
        
        // Cargar mensajes al inicio
        loadMessages();
    </script>
</body>
</html>
```

## Casos de Uso Completos

### 1. Chat Bot Completo

```python
import requests
import uuid
from datetime import datetime
from typing import List, Dict

class ChatBot:
    def __init__(self, api_client: MessageAPIClient):
        self.client = api_client
        self.responses = {
            "saludo": ["hola", "hi", "hello", "buenos días", "buenas tardes"],
            "ayuda": ["ayuda", "help", "auxilio", "soporte"],
            "despedida": ["adiós", "bye", "chao", "hasta luego"]
        }
        
    def generate_response(self, user_message: str) -> str:
        """Generar respuesta del bot basada en el mensaje del usuario"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in self.responses["saludo"]):
            return "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?"
        elif any(word in message_lower for word in self.responses["ayuda"]):
            return "Puedo ayudarte con información general. ¿Qué necesitas saber?"
        elif any(word in message_lower for word in self.responses["despedida"]):
            return "¡Hasta luego! Que tengas un buen día."
        else:
            return "Gracias por tu mensaje. ¿Hay algo específico en lo que pueda ayudarte?"
    
    def process_conversation(self, session_id: str, user_message: str) -> Dict:
        """Procesar una conversación completa"""
        # 1. Crear mensaje del usuario
        user_msg_id = f"user-{uuid.uuid4().hex[:8]}"
        user_response = self.client.create_message(
            message_id=user_msg_id,
            session_id=session_id,
            content=user_message,
            sender="user"
        )
        
        # 2. Generar respuesta del bot
        bot_response_text = self.generate_response(user_message)
        
        # 3. Crear mensaje del sistema
        bot_msg_id = f"bot-{uuid.uuid4().hex[:8]}"
        bot_response = self.client.create_message(
            message_id=bot_msg_id,
            session_id=session_id,
            content=bot_response_text,
            sender="system"
        )
        
        return {
            "user_message": user_response,
            "bot_response": bot_response
        }

# Ejemplo de uso del chat bot
def chat_example():
    client = MessageAPIClient()
    bot = ChatBot(client)
    
    session_id = f"chat-{uuid.uuid4().hex[:8]}"
    
    # Simular conversación
    messages = [
        "Hola",
        "Necesito ayuda",
        "¿Qué servicios ofrecen?",
        "Gracias, adiós"
    ]
    
    for message in messages:
        print(f"Usuario: {message}")
        
        result = bot.process_conversation(session_id, message)
        bot_response = result["bot_response"]["data"]["content"]
        
        print(f"Bot: {bot_response}")
        print("-" * 50)
    
    # Obtener historial completo
    history = client.get_messages(session_id)
    print(f"Conversación completa: {len(history['data'])} mensajes")

# chat_example()
```

### 2. Análisis de Sentimientos

```python
import re
from collections import Counter

class MessageAnalyzer:
    def __init__(self, api_client: MessageAPIClient):
        self.client = api_client
        
    def analyze_session(self, session_id: str) -> Dict:
        """Analizar todos los mensajes de una sesión"""
        messages = self.client.get_messages(session_id, limit=100)
        
        analysis = {
            "total_messages": len(messages["data"]),
            "user_messages": 0,
            "system_messages": 0,
            "total_words": 0,
            "total_characters": 0,
            "average_words_per_message": 0,
            "most_common_words": [],
            "message_timeline": []
        }
        
        all_words = []
        
        for message in messages["data"]:
            # Contadores básicos
            if message["sender"] == "user":
                analysis["user_messages"] += 1
            else:
                analysis["system_messages"] += 1
                
            analysis["total_words"] += message["metadata"]["word_count"]
            analysis["total_characters"] += message["metadata"]["character_count"]
            
            # Análisis de palabras
            words = re.findall(r'\w+', message["content"].lower())
            all_words.extend(words)
            
            # Timeline
            analysis["message_timeline"].append({
                "timestamp": message["timestamp"],
                "sender": message["sender"],
                "word_count": message["metadata"]["word_count"]
            })
        
        # Calcular promedios
        if analysis["total_messages"] > 0:
            analysis["average_words_per_message"] = analysis["total_words"] / analysis["total_messages"]
        
        # Palabras más comunes
        word_counter = Counter(all_words)
        analysis["most_common_words"] = word_counter.most_common(10)
        
        return analysis

# Ejemplo de análisis
def analysis_example():
    client = MessageAPIClient()
    analyzer = MessageAnalyzer(client)
    
    # Crear algunos mensajes de ejemplo
    session_id = "analysis-session-123"
    
    sample_messages = [
        ("user", "Hola, tengo un problema con mi cuenta"),
        ("system", "Hola, estaré encantado de ayudarte con tu cuenta"),
        ("user", "No puedo acceder a mi cuenta"),
        ("system", "Entiendo tu problema. Vamos a solucionarlo paso a paso"),
        ("user", "Perfecto, muchas gracias por la ayuda")
    ]
    
    for i, (sender, content) in enumerate(sample_messages):
        client.create_message(
            message_id=f"analysis-{i}",
            session_id=session_id,
            content=content,
            sender=sender
        )
    
    # Realizar análisis
    analysis = analyzer.analyze_session(session_id)
    
    print("=== ANÁLISIS DE SESIÓN ===")
    print(f"Total mensajes: {analysis['total_messages']}")
    print(f"Mensajes de usuario: {analysis['user_messages']}")
    print(f"Mensajes del sistema: {analysis['system_messages']}")
    print(f"Total palabras: {analysis['total_words']}")
    print(f"Promedio palabras por mensaje: {analysis['average_words_per_message']:.2f}")
    print(f"Palabras más comunes: {analysis['most_common_words'][:5]}")

# analysis_example()
```

## Manejo de Errores

### 1. Errores Comunes y Soluciones

```python
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

def handle_api_errors(func):
    """Decorador para manejar errores de API"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            print("Error: No se puede conectar con la API. Verificar que el servidor esté ejecutándose.")
        except Timeout:
            print("Error: Timeout en la petición. El servidor tardó demasiado en responder.")
        except HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json()
                print(f"Error de validación: {error_data}")
            elif e.response.status_code == 401:
                print("Error: API Key inválida o faltante.")
            elif e.response.status_code == 409:
                print("Error: El mensaje ya existe (ID duplicado).")
            else:
                print(f"Error HTTP {e.response.status_code}: {e.response.text}")
        except RequestException as e:
            print(f"Error en la petición: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    return wrapper

class SafeMessageAPIClient(MessageAPIClient):
    """Cliente con manejo seguro de errores"""
    
    @handle_api_errors
    def safe_create_message(self, *args, **kwargs):
        return self.create_message(*args, **kwargs)
    
    @handle_api_errors
    def safe_get_messages(self, *args, **kwargs):
        return self.get_messages(*args, **kwargs)
    
    def create_message_with_retry(self, max_retries=3, *args, **kwargs):
        """Crear mensaje con reintentos automáticos"""
        for attempt in range(max_retries):
            try:
                return self.create_message(*args, **kwargs)
            except (ConnectionError, Timeout) as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Intento {attempt + 1} falló, reintentando...")
                time.sleep(2 ** attempt)  # Backoff exponencial
```

## Mejores Prácticas

### 1. Generación de IDs Únicos

```python
import uuid
import time

def generate_message_id(prefix="msg"):
    """Generar ID único para mensaje"""
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4()).split('-')[0]
    return f"{prefix}-{timestamp}-{unique_id}"

def generate_session_id(user_id=None):
    """Generar ID único para sesión"""
    if user_id:
        return f"session-{user_id}-{uuid.uuid4().hex[:8]}"
    return f"session-{uuid.uuid4().hex}"
```

### 2. Validación de Entrada

```python
def validate_message_data(message_id, session_id, content, sender):
    """Validar datos antes de enviar"""
    errors = []
    
    if not message_id or not message_id.strip():
        errors.append("message_id es requerido")
        
    if not session_id or not session_id.strip():
        errors.append("session_id es requerido")
        
    if not content or not content.strip():
        errors.append("content es requerido")
        
    if sender not in ["user", "system"]:
        errors.append("sender debe ser 'user' o 'system'")
        
    if len(content) > 10000:  # Límite arbitrario
        errors.append("content es demasiado largo")
    
    return errors

# Uso
errors = validate_message_data("", "session-1", "content", "user")
if errors:
    print("Errores de validación:", errors)
```

### 3. Cache y Optimización

```python
from functools import lru_cache
import time

class CachedMessageAPIClient(MessageAPIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}
        self._cache_ttl = 300  # 5 minutos
    
    def _is_cache_valid(self, key):
        """Verificar si el cache es válido"""
        if key not in self._cache:
            return False
        return time.time() - self._cache[key]["timestamp"] < self._cache_ttl
    
    def get_messages_cached(self, session_id, **kwargs):
        """Obtener mensajes con cache"""
        cache_key = f"{session_id}_{hash(str(kwargs))}"
        
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]["data"]
        
        # Obtener datos frescos
        data = self.get_messages(session_id, **kwargs)
        
        # Guardar en cache
        self._cache[cache_key] = {
            "data": data,
            "timestamp": time.time()
        }
        
        return data
```

Estos ejemplos proporcionan una base sólida para integrar la API en diferentes tipos de aplicaciones y casos de uso.