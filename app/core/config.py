from typing import List

#  Configuración del filtrado de contenido
INAPPROPRIATE_WORDS = [
    "spam", "malware", "virus", "hack", "phishing", "scam",
    "fraud", "abuse", "harassment", "hate", "threat", "violence"
]

# Configuración de paginación
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Configuración de la API
API_VERSION = "1.0.0"
API_TITLE = "Message Processing API"
API_DESCRIPTION = "A simple API for processing chat messages"