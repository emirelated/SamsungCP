"""
Configuración central del proyecto Samsung Bot.
Contiene todas las constantes, API keys y configuraciones globales.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ==================== API KEYS ====================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Validación de credenciales
if not TELEGRAM_TOKEN:
    raise ValueError("El Token de Telegram no fue cargado.")
if not GROQ_API_KEY:
    raise ValueError("El Key de Groq no fue cargado.")

# ==================== MODELO DE SENTIMIENTO ====================
SENTIMENT_MODEL_NAME = "pysentimiento/robertuito-sentiment-analysis"

# Emojis para cada categoría de sentimiento
SENTIMENT_EMOJIS = {
    '5 stars': "😊",
    '4 stars': "🙂",
    '3 stars': "😐",
    '2 stars': "😟",
    '1 star': "😠"
}

# ==================== ENLACES SAMSUNG ====================
SAMSUNG_SHOP_URL = "https://shop.samsung.com/ar/"
SAMSUNG_SUPPORT_URL = "https://www.samsung.com/ca/support/contact/"

# ==================== CONFIGURACIÓN GROQ ====================
# Modelos
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_WHISPER_MODEL = "whisper-large-v3"

# Parámetros de generación
CHAT_TEMPERATURE = 0.3
CHAT_MAX_TOKENS = 500
VISION_TEMPERATURE = 0.7
VISION_MAX_TOKENS = 750

# ==================== ARCHIVOS ====================
DATASET_PATH = "dataset.json"
TEMP_VOICE_FILE = "temp_voice.ogg"