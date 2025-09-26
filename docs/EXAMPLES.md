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

