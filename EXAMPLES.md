# 💡 Ejemplos Prácticos de Implementación

Esta guía proporciona ejemplos completos y casos de uso reales para la **Message Processing API**, incluyendo ejemplos con cURL, Python, JavaScript, y códigos listos para usar en aplicaciones de chatbots y análisis de mensajes.

## 📋 Tabla de Contenidos

- [Ejemplos con cURL](#ejemplos-con-curl)
- [Cliente Python](#cliente-python)
- [Cliente JavaScript/Node.js](#cliente-javascriptnodejs)
- [Cliente API Completo](#cliente-api-completo)
- [Casos de Uso Reales](#casos-de-uso-reales)
- [Manejo de Errores](#manejo-de-errores)
- [Mejores Prácticas](#mejores-prácticas)

## 🔧 Ejemplos con cURL

### Verificar el Estado de la API

```bash
# Verificar que la API esté funcionando
curl -X GET "http://localhost:8000/" \
  -H "accept: application/json"

# Respuesta esperada:
# {"mensaje":"API inicializada correctamente","version":"1.0.0"}
```

### Autenticación

```bash
# Probar endpoint protegido con API key
curl -X GET "http://localhost:8000/protegido" \
  -H "X-API-Key: mi_api_key_secreta" \
  -H "accept: application/json"

# Respuesta esperada:
# {"mensaje":"Acceso autorizado a la vista protegida"}
```

```bash
# Login con API key
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "api_key": "mi_api_key_secreta"
  }'

# Respuesta esperada:
# {"mensaje":"Autenticación exitosa"}
```

### Crear Mensajes

```bash
# Crear un mensaje de usuario
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "message_id": "msg_001",
    "session_id": "session_123",
    "content": "¡Hola! ¿Cómo estás hoy?",
    "timestamp": "2024-01-15T10:30:00",
    "sender": "user"
  }'

# Respuesta esperada:
# {
#   "status": "success",
#   "data": {
#     "message_id": "msg_001",
#     "session_id": "session_123",
#     "content": "¡Hola! ¿Cómo estás hoy?",
#     "timestamp": "2024-01-15T10:30:00",
#     "sender": "user",
#     "metadata": {
#       "word_count": 4,
#       "character_count": 23,
#       "processed_at": "2024-01-15T15:30:25.123456Z"
#     }
#   }
# }
```

```bash
# Crear un mensaje del sistema
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "message_id": "msg_002",
    "session_id": "session_123",
    "content": "¡Hola! Estoy muy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?",
    "timestamp": "2024-01-15T10:30:30",
    "sender": "system"
  }'
```

### Obtener Mensajes

```bash
# Obtener todos los mensajes de una sesión
curl -X GET "http://localhost:8000/api/messages/session_123" \
  -H "accept: application/json"
```

```bash
# Obtener mensajes con paginación
curl -X GET "http://localhost:8000/api/messages/session_123?limit=5&offset=0" \
  -H "accept: application/json"
```

```bash
# Filtrar mensajes por remitente
curl -X GET "http://localhost:8000/api/messages/session_123?sender=user" \
  -H "accept: application/json"
```

```bash
# Combinación de filtros y paginación
curl -X GET "http://localhost:8000/api/messages/session_123?sender=system&limit=10&offset=0" \
  -H "accept: application/json"
```

## 🐍 Cliente Python

### Cliente Básico

```python
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class MessageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "mi_api_key_secreta"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
    
    def check_status(self) -> Dict:
        """Verificar el estado de la API"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def login(self) -> Dict:
        """Autenticarse con la API"""
        data = {"api_key": self.api_key}
        response = self.session.post(f"{self.base_url}/login", json=data)
        response.raise_for_status()
        return response.json()
    
    def create_message(self, message_id: str, session_id: str, content: str, 
                      sender: str, timestamp: Optional[str] = None) -> Dict:
        """Crear un nuevo mensaje"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
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
    
    def get_messages(self, session_id: str, sender: Optional[str] = None, 
                    limit: int = 10, offset: int = 0) -> Dict:
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

# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar cliente
    client = MessageAPIClient()
    
    # Verificar estado
    status = client.check_status()
    print(f"API Status: {status}")
    
    # Crear mensajes
    response1 = client.create_message(
        message_id="python_msg_001",
        session_id="python_session",
        content="Hola desde Python!",
        sender="user"
    )
    print(f"Mensaje creado: {response1}")
    
    response2 = client.create_message(
        message_id="python_msg_002",
        session_id="python_session",
        content="¡Hola! Bienvenido al sistema.",
        sender="system"
    )
    print(f"Respuesta del sistema: {response2}")
    
    # Obtener mensajes
    messages = client.get_messages("python_session")
    print(f"Mensajes obtenidos: {json.dumps(messages, indent=2)}")
```

### Cliente Python Asíncrono

```python
import aiohttp
import asyncio
import json
from datetime import datetime
from typing import Dict, Optional

class AsyncMessageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "mi_api_key_secreta"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def create_message(self, session: aiohttp.ClientSession, 
                           message_id: str, session_id: str, content: str, 
                           sender: str, timestamp: Optional[str] = None) -> Dict:
        """Crear mensaje de forma asíncrona"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        data = {
            "message_id": message_id,
            "session_id": session_id,
            "content": content,
            "timestamp": timestamp,
            "sender": sender
        }
        
        async with session.post(f"{self.base_url}/api/messages", 
                              json=data, headers=self.headers) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_messages(self, session: aiohttp.ClientSession, 
                          session_id: str, sender: Optional[str] = None, 
                          limit: int = 10, offset: int = 0) -> Dict:
        """Obtener mensajes de forma asíncrona"""
        params = {"limit": limit, "offset": offset}
        if sender:
            params["sender"] = sender
        
        async with session.get(f"{self.base_url}/api/messages/{session_id}", 
                             params=params, headers=self.headers) as response:
            response.raise_for_status()
            return await response.json()

# Ejemplo de uso asíncrono
async def main():
    client = AsyncMessageAPIClient()
    
    async with aiohttp.ClientSession() as session:
        # Crear múltiples mensajes concurrentemente
        messages_to_create = [
            ("async_msg_001", "async_session", "Mensaje 1", "user"),
            ("async_msg_002", "async_session", "Mensaje 2", "user"),
            ("async_msg_003", "async_session", "Respuesta automática", "system")
        ]
        
        tasks = [
            client.create_message(session, msg_id, sess_id, content, sender)
            for msg_id, sess_id, content, sender in messages_to_create
        ]
        
        results = await asyncio.gather(*tasks)
        for result in results:
            print(f"Mensaje creado: {result['data']['message_id']}")
        
        # Obtener mensajes
        messages = await client.get_messages(session, "async_session")
        print(f"Total de mensajes: {len(messages['data'])}")

# Ejecutar ejemplo asíncrono
# asyncio.run(main())
```

## 🌐 Cliente JavaScript/Node.js

### Cliente para Node.js

```javascript
const axios = require('axios');

class MessageAPIClient {
    constructor(baseUrl = 'http://localhost:8000', apiKey = 'mi_api_key_secreta') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
        this.client = axios.create({
            baseURL: this.baseUrl,
            headers: {
                'X-API-Key': this.apiKey,
                'Content-Type': 'application/json'
            }
        });
    }

    async checkStatus() {
        try {
            const response = await this.client.get('/');
            return response.data;
        } catch (error) {
            throw new Error(`API Status Check Failed: ${error.message}`);
        }
    }

    async login() {
        try {
            const response = await this.client.post('/login', {
                api_key: this.apiKey
            });
            return response.data;
        } catch (error) {
            throw new Error(`Login Failed: ${error.message}`);
        }
    }

    async createMessage(messageId, sessionId, content, sender, timestamp = null) {
        if (!timestamp) {
            timestamp = new Date().toISOString();
        }

        const data = {
            message_id: messageId,
            session_id: sessionId,
            content: content,
            timestamp: timestamp,
            sender: sender
        };

        try {
            const response = await this.client.post('/api/messages', data);
            return response.data;
        } catch (error) {
            throw new Error(`Create Message Failed: ${error.message}`);
        }
    }

    async getMessages(sessionId, sender = null, limit = 10, offset = 0) {
        const params = { limit, offset };
        if (sender) {
            params.sender = sender;
        }

        try {
            const response = await this.client.get(`/api/messages/${sessionId}`, {
                params: params
            });
            return response.data;
        } catch (error) {
            throw new Error(`Get Messages Failed: ${error.message}`);
        }
    }
}

// Ejemplo de uso
async function example() {
    const client = new MessageAPIClient();

    try {
        // Verificar estado
        const status = await client.checkStatus();
        console.log('API Status:', status);

        // Login
        const loginResult = await client.login();
        console.log('Login Result:', loginResult);

        // Crear mensajes
        const message1 = await client.createMessage(
            'js_msg_001',
            'js_session',
            '¡Hola desde JavaScript!',
            'user'
        );
        console.log('Mensaje creado:', message1);

        const message2 = await client.createMessage(
            'js_msg_002',
            'js_session',
            'Hola! ¿En qué puedo ayudarte?',
            'system'
        );
        console.log('Respuesta del sistema:', message2);

        // Obtener mensajes
        const messages = await client.getMessages('js_session');
        console.log('Mensajes obtenidos:', JSON.stringify(messages, null, 2));

    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Ejecutar ejemplo
// example();

module.exports = MessageAPIClient;
```

### Cliente para el Navegador (Vanilla JavaScript)

```javascript
class BrowserMessageAPIClient {
    constructor(baseUrl = 'http://localhost:8000', apiKey = 'mi_api_key_secreta') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
        this.headers = {
            'X-API-Key': this.apiKey,
            'Content-Type': 'application/json'
        };
    }

    async request(method, url, data = null) {
        const config = {
            method: method,
            headers: this.headers
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseUrl}${url}`, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            throw new Error(`Request failed: ${error.message}`);
        }
    }

    async checkStatus() {
        return await this.request('GET', '/');
    }

    async createMessage(messageId, sessionId, content, sender, timestamp = null) {
        if (!timestamp) {
            timestamp = new Date().toISOString();
        }

        const data = {
            message_id: messageId,
            session_id: sessionId,
            content: content,
            timestamp: timestamp,
            sender: sender
        };

        return await this.request('POST', '/api/messages', data);
    }

    async getMessages(sessionId, sender = null, limit = 10, offset = 0) {
        let url = `/api/messages/${sessionId}?limit=${limit}&offset=${offset}`;
        if (sender) {
            url += `&sender=${sender}`;
        }
        return await this.request('GET', url);
    }
}

// Ejemplo de uso en el navegador
async function browserExample() {
    const client = new BrowserMessageAPIClient();

    try {
        // Crear mensaje
        const messageResult = await client.createMessage(
            'browser_msg_001',
            'browser_session',
            'Hola desde el navegador!',
            'user'
        );
        
        console.log('Mensaje creado:', messageResult);
        
        // Obtener mensajes
        const messages = await client.getMessages('browser_session');
        console.log('Mensajes:', messages);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}
```

## 🤖 Cliente API Completo

### Clase Python Completa con Todas las Funcionalidades

```python
import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class Message:
    message_id: str
    session_id: str
    content: str
    timestamp: str
    sender: str
    metadata: Optional[Dict] = None

class MessageAPIError(Exception):
    """Excepción personalizada para errores de la API"""
    def __init__(self, message: str, status_code: int = None, details: str = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class ComprehensiveMessageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", 
                 api_key: str = "mi_api_key_secreta",
                 timeout: int = 30,
                 retry_attempts: int = 3):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        # Configurar sesión
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "MessageAPI-Python-Client/1.0"
        })
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict:
        """Realizar petición HTTP con manejo de errores y reintentos"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.retry_attempts):
            try:
                self.logger.debug(f"Attempting {method} {url} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )
                
                # Verificar status code
                if response.status_code == 200 or response.status_code == 201:
                    return response.json()
                else:
                    error_data = response.json() if response.content else {}
                    raise MessageAPIError(
                        message=f"API request failed with status {response.status_code}",
                        status_code=response.status_code,
                        details=json.dumps(error_data)
                    )
                    
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_attempts - 1:
                    raise MessageAPIError(f"Request failed after {self.retry_attempts} attempts: {e}")
    
    def check_health(self) -> Dict:
        """Verificar el estado de salud de la API"""
        return self._make_request("GET", "/")
    
    def authenticate(self) -> Dict:
        """Autenticarse con la API"""
        data = {"api_key": self.api_key}
        return self._make_request("POST", "/login", data=data)
    
    def create_message(self, message: Union[Message, Dict]) -> Dict:
        """Crear un nuevo mensaje"""
        if isinstance(message, Message):
            data = {
                "message_id": message.message_id,
                "session_id": message.session_id,
                "content": message.content,
                "timestamp": message.timestamp,
                "sender": message.sender
            }
        else:
            data = message
        
        # Validar campos requeridos
        required_fields = ["message_id", "session_id", "content", "sender"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise MessageAPIError(f"Campo requerido faltante: {field}")
        
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        
        return self._make_request("POST", "/api/messages", data=data)
    
    def get_messages(self, session_id: str, sender: Optional[str] = None, 
                    limit: int = 10, offset: int = 0) -> Dict:
        """Obtener mensajes de una sesión"""
        params = {"limit": limit, "offset": offset}
        if sender:
            if sender not in ["user", "system"]:
                raise MessageAPIError("sender debe ser 'user' o 'system'")
            params["sender"] = sender
        
        return self._make_request("GET", f"/api/messages/{session_id}", params=params)
    
    def send_conversation(self, session_id: str, messages: List[Dict]) -> List[Dict]:
        """Enviar una conversación completa"""
        results = []
        for i, message in enumerate(messages):
            message["session_id"] = session_id
            if "message_id" not in message:
                message["message_id"] = f"{session_id}_msg_{i+1:03d}"
            
            result = self.create_message(message)
            results.append(result)
        
        return results
    
    def get_conversation_summary(self, session_id: str) -> Dict:
        """Obtener resumen de una conversación"""
        messages_response = self.get_messages(session_id, limit=100)
        messages = messages_response.get("data", [])
        
        # Calcular estadísticas
        total_messages = len(messages)
        user_messages = len([m for m in messages if m.get("sender") == "user"])
        system_messages = len([m for m in messages if m.get("sender") == "system"])
        
        total_words = sum(m.get("metadata", {}).get("word_count", 0) for m in messages)
        total_chars = sum(m.get("metadata", {}).get("character_count", 0) for m in messages)
        
        return {
            "session_id": session_id,
            "total_messages": total_messages,
            "user_messages": user_messages,
            "system_messages": system_messages,
            "total_words": total_words,
            "total_characters": total_chars,
            "messages": messages
        }

# Ejemplo de uso avanzado
def advanced_example():
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear cliente
    client = ComprehensiveMessageAPIClient()
    
    try:
        # Verificar salud de la API
        health = client.check_health()
        print(f"API Health: {health}")
        
        # Autenticarse
        auth = client.authenticate()
        print(f"Authentication: {auth}")
        
        # Crear conversación de ejemplo
        session_id = "advanced_session_001"
        conversation = [
            {"content": "Hola, necesito ayuda con mi cuenta", "sender": "user"},
            {"content": "¡Hola! Estaré encantado de ayudarte con tu cuenta. ¿Cuál es el problema específico?", "sender": "system"},
            {"content": "No puedo acceder a mis transacciones recientes", "sender": "user"},
            {"content": "Entiendo. Voy a revisar tu cuenta. Por favor, espera un momento.", "sender": "system"},
            {"content": "He revisado tu cuenta y todo parece estar en orden. ¿Podrías intentar cerrar sesión y volver a entrar?", "sender": "system"},
            {"content": "Perfecto! Ya pude acceder. Muchas gracias por tu ayuda", "sender": "user"}
        ]
        
        # Enviar conversación
        results = client.send_conversation(session_id, conversation)
        print(f"Conversación creada: {len(results)} mensajes")
        
        # Obtener resumen
        summary = client.get_conversation_summary(session_id)
        print(f"Resumen de conversación: {json.dumps(summary, indent=2)}")
        
    except MessageAPIError as e:
        print(f"Error de API: {e.message}")
        if e.details:
            print(f"Detalles: {e.details}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    advanced_example()
```

## 🎯 Casos de Uso Reales

### 1. Chatbot de Atención al Cliente

```python
import asyncio
from datetime import datetime
import uuid

class CustomerServiceBot:
    def __init__(self, api_client):
        self.api_client = api_client
        self.active_sessions = {}
    
    async def start_session(self, customer_id: str) -> str:
        """Iniciar nueva sesión de atención al cliente"""
        session_id = f"cs_{customer_id}_{uuid.uuid4().hex[:8]}"
        self.active_sessions[session_id] = {
            "customer_id": customer_id,
            "start_time": datetime.now(),
            "status": "active"
        }
        
        # Mensaje de bienvenida
        welcome_message = {
            "message_id": f"{session_id}_welcome",
            "session_id": session_id,
            "content": "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?",
            "sender": "system"
        }
        
        await self.api_client.create_message(welcome_message)
        return session_id
    
    async def process_customer_message(self, session_id: str, message: str) -> str:
        """Procesar mensaje del cliente y generar respuesta"""
        # Guardar mensaje del cliente
        customer_message = {
            "message_id": f"{session_id}_{uuid.uuid4().hex[:8]}",
            "session_id": session_id,
            "content": message,
            "sender": "user"
        }
        
        await self.api_client.create_message(customer_message)
        
        # Generar respuesta basada en palabras clave
        response = self._generate_response(message)
        
        # Guardar respuesta del sistema
        system_message = {
            "message_id": f"{session_id}_{uuid.uuid4().hex[:8]}",
            "session_id": session_id,
            "content": response,
            "sender": "system"
        }
        
        await self.api_client.create_message(system_message)
        return response
    
    def _generate_response(self, message: str) -> str:
        """Generar respuesta automática basada en el contenido del mensaje"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["saldo", "balance", "dinero"]):
            return "Para consultar tu saldo, puedes ingresar a la app o llamar al *611. ¿Necesitas ayuda con algo más?"
        
        elif any(word in message_lower for word in ["transferencia", "enviar", "transferir"]):
            return "Para hacer transferencias, ve a la sección 'Enviar dinero' en la app. ¿Te ayudo con los pasos?"
        
        elif any(word in message_lower for word in ["problema", "error", "falla"]):
            return "Lamento que tengas problemas. ¿Podrías contarme más detalles sobre lo que está pasando?"
        
        elif any(word in message_lower for word in ["gracias", "thank", "genial", "perfecto"]):
            return "¡De nada! Me alegra poder ayudarte. ¿Hay algo más en lo que pueda asistirte?"
        
        else:
            return "Entiendo tu consulta. Un agente especializado se pondrá en contacto contigo pronto. ¿Mientras tanto, hay algo más en lo que pueda ayudarte?"

# Ejemplo de uso del chatbot
async def chatbot_example():
    from aiohttp import ClientSession
    
    # Crear cliente asíncrono (simplificado para el ejemplo)
    class SimpleAsyncClient:
        def __init__(self):
            self.base_url = "http://localhost:8000"
            self.headers = {"X-API-Key": "mi_api_key_secreta", "Content-Type": "application/json"}
        
        async def create_message(self, message_data):
            async with ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/messages",
                    json=message_data,
                    headers=self.headers
                ) as response:
                    return await response.json()
    
    client = SimpleAsyncClient()
    bot = CustomerServiceBot(client)
    
    # Simular conversación
    session_id = await bot.start_session("customer_123")
    print(f"Sesión iniciada: {session_id}")
    
    # Simular mensajes del cliente
    customer_messages = [
        "Hola, necesito revisar mi saldo",
        "¿Cómo hago una transferencia?",
        "Perfecto, muchas gracias por la ayuda"
    ]
    
    for message in customer_messages:
        response = await bot.process_customer_message(session_id, message)
        print(f"Cliente: {message}")
        print(f"Bot: {response}")
        print("-" * 50)

# Ejecutar ejemplo del chatbot
# asyncio.run(chatbot_example())
```

### 2. Análisis de Mensajes y Métricas

```python
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import re
from datetime import datetime, timedelta

class MessageAnalyzer:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def analyze_session(self, session_id: str) -> Dict:
        """Análisis completo de una sesión de mensajes"""
        # Obtener todos los mensajes
        messages_response = self.api_client.get_messages(session_id, limit=1000)
        messages = messages_response.get("data", [])
        
        if not messages:
            return {"error": "No messages found for session"}
        
        # Análisis básico
        analysis = {
            "session_id": session_id,
            "total_messages": len(messages),
            "message_analysis": self._analyze_messages(messages),
            "temporal_analysis": self._analyze_temporal_patterns(messages),
            "content_analysis": self._analyze_content(messages),
            "sender_analysis": self._analyze_senders(messages)
        }
        
        return analysis
    
    def _analyze_messages(self, messages: List[Dict]) -> Dict:
        """Análisis de mensajes"""
        total_words = sum(msg.get("metadata", {}).get("word_count", 0) for msg in messages)
        total_chars = sum(msg.get("metadata", {}).get("character_count", 0) for msg in messages)
        
        avg_words = total_words / len(messages) if messages else 0
        avg_chars = total_chars / len(messages) if messages else 0
        
        return {
            "total_words": total_words,
            "total_characters": total_chars,
            "average_words_per_message": round(avg_words, 2),
            "average_characters_per_message": round(avg_chars, 2)
        }
    
    def _analyze_temporal_patterns(self, messages: List[Dict]) -> Dict:
        """Análisis de patrones temporales"""
        timestamps = [datetime.fromisoformat(msg["timestamp"].replace('Z', '+00:00')) 
                     for msg in messages]
        
        if len(timestamps) < 2:
            return {"error": "Not enough messages for temporal analysis"}
        
        # Duración de la conversación
        duration = timestamps[-1] - timestamps[0]
        
        # Intervalos entre mensajes
        intervals = [(timestamps[i+1] - timestamps[i]).total_seconds() 
                    for i in range(len(timestamps)-1)]
        
        return {
            "conversation_duration_seconds": duration.total_seconds(),
            "average_response_time_seconds": sum(intervals) / len(intervals) if intervals else 0,
            "min_response_time_seconds": min(intervals) if intervals else 0,
            "max_response_time_seconds": max(intervals) if intervals else 0
        }
    
    def _analyze_content(self, messages: List[Dict]) -> Dict:
        """Análisis de contenido"""
        all_content = " ".join(msg["content"] for msg in messages)
        
        # Extraer palabras (sin caracteres especiales)
        words = re.findall(r'\b\w+\b', all_content.lower())
        word_freq = Counter(words)
        
        # Palabras más comunes
        most_common = word_freq.most_common(10)
        
        # Detectar preguntas
        questions = [msg for msg in messages if "?" in msg["content"]]
        
        return {
            "unique_words": len(set(words)),
            "most_common_words": most_common,
            "question_count": len(questions),
            "question_percentage": round(len(questions) / len(messages) * 100, 2) if messages else 0
        }
    
    def _analyze_senders(self, messages: List[Dict]) -> Dict:
        """Análisis por remitente"""
        senders = Counter(msg["sender"] for msg in messages)
        
        user_messages = [msg for msg in messages if msg["sender"] == "user"]
        system_messages = [msg for msg in messages if msg["sender"] == "system"]
        
        user_words = sum(msg.get("metadata", {}).get("word_count", 0) for msg in user_messages)
        system_words = sum(msg.get("metadata", {}).get("word_count", 0) for msg in system_messages)
        
        return {
            "messages_by_sender": dict(senders),
            "words_by_sender": {
                "user": user_words,
                "system": system_words
            },
            "avg_words_per_message_by_sender": {
                "user": round(user_words / len(user_messages), 2) if user_messages else 0,
                "system": round(system_words / len(system_messages), 2) if system_messages else 0
            }
        }
    
    def generate_report(self, session_id: str, output_file: str = None) -> str:
        """Generar reporte detallado"""
        analysis = self.analyze_session(session_id)
        
        if "error" in analysis:
            return f"Error en análisis: {analysis['error']}"
        
        report = f"""
# Reporte de Análisis de Mensajes
## Sesión: {session_id}

### Resumen General
- **Total de mensajes**: {analysis['total_messages']}
- **Total de palabras**: {analysis['message_analysis']['total_words']}
- **Total de caracteres**: {analysis['message_analysis']['total_characters']}
- **Promedio de palabras por mensaje**: {analysis['message_analysis']['average_words_per_message']}

### Análisis Temporal
- **Duración de conversación**: {analysis['temporal_analysis']['conversation_duration_seconds']:.2f} segundos
- **Tiempo promedio de respuesta**: {analysis['temporal_analysis']['average_response_time_seconds']:.2f} segundos

### Análisis de Contenido
- **Palabras únicas**: {analysis['content_analysis']['unique_words']}
- **Preguntas realizadas**: {analysis['content_analysis']['question_count']} ({analysis['content_analysis']['question_percentage']}%)

### Palabras más comunes:
"""
        
        for word, count in analysis['content_analysis']['most_common_words']:
            report += f"- {word}: {count} veces\n"
        
        report += f"""
### Análisis por Remitente
- **Mensajes de usuario**: {analysis['sender_analysis']['messages_by_sender'].get('user', 0)}
- **Mensajes de sistema**: {analysis['sender_analysis']['messages_by_sender'].get('system', 0)}
- **Palabras promedio por mensaje (usuario)**: {analysis['sender_analysis']['avg_words_per_message_by_sender']['user']}
- **Palabras promedio por mensaje (sistema)**: {analysis['sender_analysis']['avg_words_per_message_by_sender']['system']}
"""
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report

# Ejemplo de uso del analizador
def analyzer_example():
    client = ComprehensiveMessageAPIClient()
    analyzer = MessageAnalyzer(client)
    
    # Crear sesión de ejemplo para análisis
    session_id = "analytics_session_001"
    
    # Crear algunos mensajes de ejemplo
    sample_messages = [
        {"content": "Hola, ¿cómo puedo transferir dinero?", "sender": "user"},
        {"content": "Te puedo ayudar con las transferencias. ¿A qué banco quieres enviar?", "sender": "system"},
        {"content": "Quiero enviar a Bancolombia", "sender": "user"},
        {"content": "Perfecto. Para transferir a Bancolombia necesitas el número de cuenta del destinatario.", "sender": "system"},
        {"content": "¿También necesito el tipo de cuenta?", "sender": "user"},
        {"content": "Sí, necesitas saber si es cuenta de ahorros o corriente.", "sender": "system"},
        {"content": "Entendido, muchas gracias por la información", "sender": "user"}
    ]
    
    # Crear mensajes
    for i, msg in enumerate(sample_messages):
        msg["message_id"] = f"analytics_msg_{i+1:03d}"
        msg["session_id"] = session_id
        client.create_message(msg)
    
    # Generar análisis
    report = analyzer.generate_report(session_id, "session_analysis_report.md")
    print(report)

# analyzer_example()
```

### 3. Monitor de Conversaciones en Tiempo Real

```python
import time
import threading
from datetime import datetime
from typing import Callable, Dict, List

class ConversationMonitor:
    def __init__(self, api_client, check_interval: int = 5):
        self.api_client = api_client
        self.check_interval = check_interval
        self.monitoring = False
        self.monitored_sessions = {}
        self.alerts = []
        self.callbacks = []
    
    def add_session(self, session_id: str, alert_conditions: Dict = None):
        """Agregar sesión para monitoreo"""
        self.monitored_sessions[session_id] = {
            "last_check": datetime.now(),
            "message_count": 0,
            "alert_conditions": alert_conditions or {},
            "last_message_time": None
        }
    
    def add_alert_callback(self, callback: Callable):
        """Agregar callback para alertas"""
        self.callbacks.append(callback)
    
    def start_monitoring(self):
        """Iniciar monitoreo en hilo separado"""
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        print("Monitoreo iniciado")
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring = False
        print("Monitoreo detenido")
    
    def _monitor_loop(self):
        """Loop principal de monitoreo"""
        while self.monitoring:
            for session_id in list(self.monitored_sessions.keys()):
                self._check_session(session_id)
            time.sleep(self.check_interval)
    
    def _check_session(self, session_id: str):
        """Verificar estado de una sesión específica"""
        try:
            session_info = self.monitored_sessions[session_id]
            
            # Obtener mensajes nuevos
            messages_response = self.api_client.get_messages(
                session_id, 
                limit=50,
                offset=0
            )
            
            messages = messages_response.get("data", [])
            current_message_count = len(messages)
            
            # Verificar si hay mensajes nuevos
            if current_message_count > session_info["message_count"]:
                new_messages = current_message_count - session_info["message_count"]
                self._handle_new_messages(session_id, new_messages, messages)
                session_info["message_count"] = current_message_count
            
            # Verificar condiciones de alerta
            self._check_alert_conditions(session_id, messages)
            
            session_info["last_check"] = datetime.now()
            
        except Exception as e:
            print(f"Error monitoreando sesión {session_id}: {e}")
    
    def _handle_new_messages(self, session_id: str, new_count: int, messages: List[Dict]):
        """Manejar mensajes nuevos"""
        print(f"Sesión {session_id}: {new_count} mensajes nuevos")
        
        # Notificar callbacks
        for callback in self.callbacks:
            try:
                callback({
                    "type": "new_messages",
                    "session_id": session_id,
                    "new_message_count": new_count,
                    "total_messages": len(messages),
                    "latest_messages": messages[:new_count]
                })
            except Exception as e:
                print(f"Error en callback: {e}")
    
    def _check_alert_conditions(self, session_id: str, messages: List[Dict]):
        """Verificar condiciones de alerta"""
        session_info = self.monitored_sessions[session_id]
        conditions = session_info["alert_conditions"]
        
        if not conditions:
            return
        
        # Alerta por inactividad
        if "max_inactive_minutes" in conditions:
            if messages:
                last_message_time = datetime.fromisoformat(
                    messages[0]["timestamp"].replace('Z', '+00:00')
                )
                inactive_minutes = (datetime.now(last_message_time.tzinfo) - last_message_time).total_seconds() / 60
                
                if inactive_minutes > conditions["max_inactive_minutes"]:
                    self._trigger_alert(session_id, "inactivity", f"Sesión inactiva por {inactive_minutes:.1f} minutos")
        
        # Alerta por palabras clave
        if "keyword_alerts" in conditions:
            for message in messages[:5]:  # Revisar últimos 5 mensajes
                content = message["content"].lower()
                for keyword in conditions["keyword_alerts"]:
                    if keyword.lower() in content:
                        self._trigger_alert(session_id, "keyword", f"Palabra clave detectada: {keyword}")
        
        # Alerta por duración de conversación
        if "max_conversation_length" in conditions:
            if len(messages) > conditions["max_conversation_length"]:
                self._trigger_alert(session_id, "length", f"Conversación excede {conditions['max_conversation_length']} mensajes")
    
    def _trigger_alert(self, session_id: str, alert_type: str, message: str):
        """Disparar alerta"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "type": alert_type,
            "message": message
        }
        
        self.alerts.append(alert)
        print(f"🚨 ALERTA [{alert_type.upper()}] - Sesión {session_id}: {message}")
        
        # Notificar callbacks
        for callback in self.callbacks:
            try:
                callback({
                    "type": "alert",
                    "alert": alert
                })
            except Exception as e:
                print(f"Error en callback de alerta: {e}")
    
    def get_alerts(self, session_id: str = None) -> List[Dict]:
        """Obtener alertas"""
        if session_id:
            return [alert for alert in self.alerts if alert["session_id"] == session_id]
        return self.alerts
    
    def get_monitoring_status(self) -> Dict:
        """Obtener estado del monitoreo"""
        return {
            "monitoring": self.monitoring,
            "monitored_sessions": len(self.monitored_sessions),
            "total_alerts": len(self.alerts),
            "last_check": datetime.now().isoformat()
        }

# Ejemplo de uso del monitor
def monitoring_example():
    client = ComprehensiveMessageAPIClient()
    monitor = ConversationMonitor(client, check_interval=3)
    
    # Callback para manejar eventos
    def handle_event(event):
        if event["type"] == "new_messages":
            print(f"📩 Nuevos mensajes en {event['session_id']}: {event['new_message_count']}")
        elif event["type"] == "alert":
            print(f"🚨 {event['alert']['message']}")
    
    monitor.add_alert_callback(handle_event)
    
    # Configurar monitoreo de sesión
    monitor.add_session("monitor_session_001", {
        "max_inactive_minutes": 2,
        "keyword_alerts": ["problema", "error", "ayuda urgente"],
        "max_conversation_length": 20
    })
    
    # Iniciar monitoreo
    monitor.start_monitoring()
    
    # Simular actividad creando mensajes
    print("Creando mensajes de prueba...")
    test_messages = [
        {"content": "Hola, tengo un problema con mi cuenta", "sender": "user"},
        {"content": "Hola, lamento escuchar eso. ¿Podrías contarme más detalles?", "sender": "system"},
        {"content": "No puedo acceder a mi saldo", "sender": "user"}
    ]
    
    for i, msg in enumerate(test_messages):
        msg["message_id"] = f"monitor_msg_{i+1:03d}"
        msg["session_id"] = "monitor_session_001"
        client.create_message(msg)
        time.sleep(2)  # Esperar entre mensajes
    
    # Mantener monitoreo por un tiempo
    time.sleep(10)
    
    # Mostrar estado final
    status = monitor.get_monitoring_status()
    print(f"Estado del monitoreo: {status}")
    
    alerts = monitor.get_alerts()
    print(f"Total de alertas: {len(alerts)}")
    
    monitor.stop_monitoring()

# monitoring_example()
```

## ⚠️ Manejo de Errores

### Ejemplos de Manejo de Errores

```python
# Ejemplo de manejo de errores completo
def error_handling_example():
    client = ComprehensiveMessageAPIClient()
    
    # 1. Error de autenticación
    try:
        wrong_client = ComprehensiveMessageAPIClient(api_key="wrong_key")
        wrong_client.check_health()  # Esto debería funcionar
        wrong_client.create_message({  # Esto fallará si hay endpoints protegidos
            "message_id": "test",
            "session_id": "test",
            "content": "test",
            "sender": "user"
        })
    except MessageAPIError as e:
        print(f"Error de autenticación: {e.message}")
    
    # 2. Error de validación
    try:
        client.create_message({
            "message_id": "",  # ID vacío
            "session_id": "test",
            "content": "test",
            "sender": "user"
        })
    except MessageAPIError as e:
        print(f"Error de validación: {e.message}")
    
    # 3. Error de contenido inapropiado
    try:
        client.create_message({
            "message_id": "spam_test",
            "session_id": "test",
            "content": "Este es un mensaje de spam",  # Contiene palabra prohibida
            "sender": "user"
        })
    except MessageAPIError as e:
        print(f"Error de contenido: {e.message}")
    
    # 4. Error de sender inválido
    try:
        client.create_message({
            "message_id": "invalid_sender",
            "session_id": "test",
            "content": "test",
            "sender": "invalid_sender"  # Sender inválido
        })
    except MessageAPIError as e:
        print(f"Error de sender: {e.message}")
    
    # 5. Error de conexión
    try:
        offline_client = ComprehensiveMessageAPIClient(
            base_url="http://localhost:9999",  # Puerto inexistente
            retry_attempts=1
        )
        offline_client.check_health()
    except MessageAPIError as e:
        print(f"Error de conexión: {e.message}")

# error_handling_example()
```

### cURL - Ejemplos de Errores

```bash
# Error de autenticación
curl -X GET "http://localhost:8000/protegido" \
  -H "X-API-Key: wrong_key"

# Respuesta esperada:
# {"detail":"API Key inválida"}

# Error de validación - campos faltantes
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "",
    "content": "test",
    "sender": "user"
  }'

# Error de contenido inapropiado
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "spam_msg",
    "session_id": "test_session",
    "content": "Este mensaje contiene spam",
    "timestamp": "2024-01-15T10:30:00",
    "sender": "user"
  }'

# Error de sender inválido
curl -X POST "http://localhost:8000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "invalid_msg",
    "session_id": "test_session",
    "content": "test content",
    "timestamp": "2024-01-15T10:30:00",
    "sender": "invalid_sender"
  }'
```

## 🎯 Mejores Prácticas

### 1. Estructura de Proyecto Recomendada

```
my_chatbot_project/
├── config/
│   ├── __init__.py
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── chatbot.py
│   ├── analyzer.py
│   └── monitor.py
├── tests/
│   ├── test_api_client.py
│   ├── test_chatbot.py
│   └── test_analyzer.py
├── requirements.txt
├── README.md
└── main.py
```

### 2. Configuración con Variables de Entorno

```python
# config/__init__.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_KEY: str = os.getenv("API_KEY", "mi_api_key_secreta")
    RETRY_ATTEMPTS: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()
```

### 3. Logging Configurado

```python
# src/logger.py
import logging
import os

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
```

### 4. Tests Unitarios

```python
# tests/test_api_client.py
import pytest
import responses
from src.api_client import MessageAPIClient, MessageAPIError

class TestMessageAPIClient:
    
    @responses.activate
    def test_check_health_success(self):
        responses.add(
            responses.GET,
            "http://localhost:8000/",
            json={"mensaje": "API inicializada correctamente", "version": "1.0.0"},
            status=200
        )
        
        client = MessageAPIClient()
        result = client.check_health()
        
        assert result["mensaje"] == "API inicializada correctamente"
        assert result["version"] == "1.0.0"
    
    @responses.activate
    def test_create_message_success(self):
        responses.add(
            responses.POST,
            "http://localhost:8000/api/messages",
            json={
                "status": "success",
                "data": {
                    "message_id": "test_msg",
                    "session_id": "test_session",
                    "content": "test content",
                    "sender": "user",
                    "metadata": {"word_count": 2, "character_count": 12}
                }
            },
            status=201
        )
        
        client = MessageAPIClient()
        result = client.create_message({
            "message_id": "test_msg",
            "session_id": "test_session",
            "content": "test content",
            "sender": "user"
        })
        
        assert result["status"] == "success"
        assert result["data"]["message_id"] == "test_msg"
    
    @responses.activate
    def test_create_message_validation_error(self):
        responses.add(
            responses.POST,
            "http://localhost:8000/api/messages",
            json={"detail": {"error": {"code": "INVALID_FORMAT", "message": "Campo requerido faltante"}}},
            status=400
        )
        
        client = MessageAPIClient()
        
        with pytest.raises(MessageAPIError) as exc_info:
            client.create_message({
                "message_id": "",  # ID vacío
                "session_id": "test",
                "content": "test",
                "sender": "user"
            })
        
        assert exc_info.value.status_code == 400
```

### 5. Implementación con Rate Limiting

```python
import time
from collections import defaultdict, deque

class RateLimitedClient:
    def __init__(self, api_client, requests_per_minute: int = 60):
        self.api_client = api_client
        self.requests_per_minute = requests_per_minute
        self.request_times = deque()
    
    def _check_rate_limit(self):
        now = time.time()
        # Remover requests más antiguos que 1 minuto
        while self.request_times and self.request_times[0] < now - 60:
            self.request_times.popleft()
        
        # Si hemos alcanzado el límite, esperar
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self._check_rate_limit()  # Verificar nuevamente
    
    def create_message(self, message_data):
        self._check_rate_limit()
        self.request_times.append(time.time())
        return self.api_client.create_message(message_data)
    
    def get_messages(self, session_id, **kwargs):
        self._check_rate_limit()
        self.request_times.append(time.time())
        return self.api_client.get_messages(session_id, **kwargs)
```

### 6. Cache de Respuestas

```python
import json
import hashlib
from functools import wraps
from datetime import datetime, timedelta

class CachedAPIClient:
    def __init__(self, api_client, cache_ttl: int = 300):  # 5 minutos
        self.api_client = api_client
        self.cache_ttl = cache_ttl
        self.cache = {}
    
    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        key_data = f"{method}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        return datetime.now() - timestamp < timedelta(seconds=self.cache_ttl)
    
    def get_messages(self, session_id: str, **kwargs):
        cache_key = self._get_cache_key("get_messages", session_id, **kwargs)
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return cached_data
        
        # Obtener datos frescos
        result = self.api_client.get_messages(session_id, **kwargs)
        self.cache[cache_key] = (result, datetime.now())
        return result
    
    def create_message(self, message_data):
        # Los POST no se cachean
        result = self.api_client.create_message(message_data)
        # Limpiar cache relacionado con la sesión
        session_id = message_data.get("session_id")
        if session_id:
            keys_to_remove = [k for k in self.cache.keys() if session_id in k]
            for key in keys_to_remove:
                del self.cache[key]
        return result
```

---

## 📚 Recursos Adicionales

- **Documentación de FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://sqlalchemy.org/
- **Requests**: https://requests.readthedocs.io/
- **Pydantic**: https://pydantic-docs.helpmanual.io/

Para más información sobre configuración, consulta [CONFIGURATION.md](./CONFIGURATION.md).

¡Esperamos que estos ejemplos te sean útiles para implementar tu aplicación con la Message Processing API! 🚀