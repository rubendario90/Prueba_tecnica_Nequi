# Guía de Despliegue - Message Processing API

## Información General

Esta guía proporciona instrucciones detalladas para desplegar la API de procesamiento de mensajes en diferentes entornos: desarrollo, staging y producción.

## Tabla de Contenidos

- [Preparación para Despliegue](#preparación-para-despliegue)
- [Despliegue Local](#despliegue-local)
- [Despliegue con Docker](#despliegue-con-docker)
- [Despliegue en Servidor (Linux)](#despliegue-en-servidor-linux)
- [Despliegue en la Nube](#despliegue-en-la-nube)
- [Configuración de Base de Datos](#configuración-de-base-de-datos)
- [Monitoreo y Logs](#monitoreo-y-logs)
- [Seguridad](#seguridad)
- [Mantenimiento](#mantenimiento)

## Preparación para Despliegue

### 1. Lista de Verificación Pre-Despliegue

- [ ] Tests pasando (100% coverage recomendado)
- [ ] Variables de entorno configuradas
- [ ] API Keys seguras generadas
- [ ] Base de datos configurada
- [ ] Certificados SSL/TLS (para HTTPS)
- [ ] Configuración de CORS
- [ ] Logging configurado
- [ ] Monitoreo configurado

### 2. Generar API Keys Seguras

```python
import secrets

# Generar API key segura
secure_api_key = secrets.token_urlsafe(32)
print(f"API_KEY={secure_api_key}")
```

### 3. Configurar Variables de Entorno

Crear archivo `.env.production`:
```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/messages_production

# Seguridad
API_KEY=your_super_secure_api_key_here
SECRET_KEY=your_secret_key_here

# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO

# Configuraciones específicas
MAX_PAGE_SIZE=50
DEFAULT_PAGE_SIZE=10
```

## Despliegue Local

### Desarrollo Rápido

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
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción Local

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Con archivo de configuración
gunicorn main:app -c gunicorn.conf.py
```

**Archivo `gunicorn.conf.py`**:
```python
# Worker configuration
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# Socket configuration
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes configuration
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Timeout configuration
timeout = 30
keepalive = 5

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "message_processing_api"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/gunicorn.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (si se usa)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
```

## Despliegue con Docker

### 1. Dockerfile

```dockerfile
FROM python:3.10-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Crear usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /var/log/gunicorn /var/run/gunicorn
RUN chown -R appuser:appuser /app /var/log/gunicorn /var/run/gunicorn

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Comando de inicio
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/messages_db
      - API_KEY=${API_KEY}
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - ./logs:/var/log/gunicorn
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: messages_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### 3. Comandos Docker

```bash
# Construir imagen
docker build -t message-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name message-api-container message-api

# Con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Escalar servicios
docker-compose up -d --scale app=3
```

## Despliegue en Servidor (Linux)

### 1. Preparación del Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    postgresql \
    postgresql-contrib \
    supervisor \
    curl

# Crear usuario para la aplicación
sudo adduser --system --group --disabled-password --shell /bin/bash appuser
```

### 2. Configuración de PostgreSQL

```bash
# Cambiar a usuario postgres
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE messages_production;
CREATE USER appuser WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE messages_production TO appuser;
\quit

# Configurar autenticación
sudo vim /etc/postgresql/13/main/pg_hba.conf
# Agregar línea:
# local   messages_production    appuser                                md5
```

### 3. Despliegue de la Aplicación

```bash
# Cambiar a usuario de aplicación
sudo su - appuser

# Clonar repositorio
git clone https://github.com/rubendario90/Prueba_tecnica_Nequi.git
cd Prueba_tecnica_Nequi

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# Configurar variables de entorno
cp .env.example .env.production
vim .env.production

# Ejecutar migraciones (si las hay)
python main.py  # Para crear tablas automáticamente

# Probar aplicación
gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```

### 4. Configuración de Supervisor

**Archivo `/etc/supervisor/conf.d/message-api.conf`**:
```ini
[program:message-api]
command=/home/appuser/Prueba_tecnica_Nequi/venv/bin/gunicorn main:app -c /home/appuser/Prueba_tecnica_Nequi/gunicorn.conf.py
directory=/home/appuser/Prueba_tecnica_Nequi
user=appuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/message-api.log
environment=PATH="/home/appuser/Prueba_tecnica_Nequi/venv/bin"
```

```bash
# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start message-api

# Verificar estado
sudo supervisorctl status
```

### 5. Configuración de Nginx

**Archivo `/etc/nginx/sites-available/message-api`**:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redireccionar HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # Configuración SSL
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Headers de seguridad
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logs
    access_log /var/log/nginx/message-api.access.log;
    error_log /var/log/nginx/message-api.error.log;

    # Configuración de proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Archivos estáticos (si los hay)
    location /static/ {
        alias /home/appuser/Prueba_tecnica_Nequi/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/message-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Despliegue en la Nube

### 1. AWS EC2

```bash
# 1. Crear instancia EC2 (Ubuntu 20.04 LTS)
# 2. Configurar Security Groups (puertos 22, 80, 443)
# 3. Conectar por SSH

# Script de instalación automática
#!/bin/bash
curl -sSL https://raw.githubusercontent.com/rubendario90/Prueba_tecnica_Nequi/main/deploy/aws-deploy.sh | bash
```

### 2. Google Cloud Platform

```bash
# Crear instancia
gcloud compute instances create message-api-instance \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-small \
    --zone=us-central1-a \
    --tags=http-server,https-server

# Configurar firewall
gcloud compute firewall-rules create allow-http --allow tcp:80
gcloud compute firewall-rules create allow-https --allow tcp:443
```

### 3. DigitalOcean

```bash
# Usar droplet con Ubuntu 20.04
# Seguir los mismos pasos que el despliegue en servidor Linux
```

### 4. Heroku

**Archivo `Procfile`**:
```
web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**Archivo `runtime.txt`**:
```
python-3.10.8
```

```bash
# Instalar Heroku CLI
# Crear aplicación
heroku create message-processing-api

# Configurar variables de entorno
heroku config:set API_KEY=your_secure_api_key
heroku config:set DATABASE_URL=your_database_url

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

## Configuración de Base de Datos

### PostgreSQL (Recomendado para Producción)

```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Configurar base de datos
sudo -u postgres createuser --interactive
sudo -u postgres createdb messages_production

# Configurar conexión
DATABASE_URL=postgresql://username:password@localhost:5432/messages_production
```

### MySQL (Alternativa)

```bash
# Instalar MySQL
sudo apt install mysql-server

# Configurar base de datos
sudo mysql
CREATE DATABASE messages_production;
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON messages_production.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;

# Configurar conexión
DATABASE_URL=mysql+pymysql://appuser:password@localhost:3306/messages_production
```

## Monitoreo y Logs

### 1. Configuración de Logs

```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/message-api/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "detailed",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/message-api/error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "detailed",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file", "error_file"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 2. Monitoreo con Prometheus + Grafana

**docker-compose.monitoring.yml**:
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

## Seguridad

### 1. Configuración HTTPS

```bash
# Certificados Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Firewall

```bash
# UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### 3. Fail2Ban

```bash
# Instalar Fail2Ban
sudo apt install fail2ban

# Configurar
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Mantenimiento

### 1. Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump messages_production > /backups/db_backup_$DATE.sql
tar -czf /backups/app_backup_$DATE.tar.gz /home/appuser/Prueba_tecnica_Nequi
```

### 2. Actualizaciones

```bash
#!/bin/bash
# update.sh
cd /home/appuser/Prueba_tecnica_Nequi
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart message-api
```

### 3. Monitoreo de Salud

```bash
#!/bin/bash
# health_check.sh
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "API is healthy"
else
    echo "API is down, restarting..."
    sudo supervisorctl restart message-api
fi
```

Esta guía cubre los aspectos principales del despliegue. Ajusta las configuraciones según tus necesidades específicas y el entorno de despliegue elegido.