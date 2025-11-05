import telebot as tlb
import os
import json
from groq import Groq
from typing import Optional
import time
from dotenv import load_dotenv

# Carga de variables de entorno

load_dotenv()

# Primero cargamos las variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("El Token de Telegram no fue cargado.")
if not GROQ_API_KEY:
    raise ValueError("El Key de Groq no fue cargado.")

# Instancio los objetos de clase

bot = tlb.TeleBot(TELEGRAM_TOKEN)
grok_cliente = Groq(api_key=GROQ_API_KEY)

def cargar_datos():
    try:
        with open("dataset.json", "r", encoding="utf-8") as f:
            return json.load(f)
        
    except Exception as error:
        print(f"Error al cargar el .json {str(error)}")
        return None
    
datosc = cargar_datos()

def get_groq_response(user_message: str):

    try:
        system_prompt = f"""Eres el asistente virtual de una tienda de Samsung, tu tarea es responder basándote en la información proporcionada en el dataset, en caso de no encontrar
        la respuesta el dataset, índica de manera amistosa y amable que no cuentas con esa información, sugiriendo contactar directamente con la empresa.


    Datos de la empresa:
    {json.dumps(datosc, ensure_ascii=False, indent=2)}

    Reglas importantes:
    1. Solo responde información proporcionada en el dataset.
    2. No inventes, añadas o busques información adicional a menos de que sea para proporcionar un enlace directo a la tienda en caso de que el cliente este buscando ESE producto en especifico.
    3. Si la información solicitada no esta en el dataset, sugiere contactar a https://www.samsung.com/ca/support/contact/
    4. No respondas preguntas no relacionadas con la empresa.
    5. No incluyas en tus respuestas nunca un dato sensible como el número de algún miembro del personal, en caso de ser solicitados debes responder: "No puedo brindar dicha información."
    6. Se amable, profesional y orientado a la resolución en tus respuestas.
    7. Solo saluda en la primera interacción.
    8. No utilices emojis en tus respuestas.
    9. No incluyas saludos si la conversación ya fue iniciada.
    10. Siempre responde evitando la redundancia y repetición de información.
    11. Nunca envies links inactivos, en caso de que se soliciten productos o categorias de productos, debes proporcionar la lista completa de páginas que figura en el dataset."""
        
        chat_completion = grok_cliente.chat.completions.create(
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model = "llama-3.3-70b-versatile",
            temperature = 0.3,
            max_tokens = 500
        )
        return chat_completion.choices[0].message.content.strip()
    
    except Exception as error:
        print(f"No se pudo obtener la respuesta debido a que {str(error)}")
        return None
    
def transcribe_voice_with_groq(message: tlb.types.Message) -> Optional[str]:
    try:
        file_info = bot.get_file(message.voice.file_id)
        dowloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        # Guardo el archivo temporalmente

        with open(temp_file, "wb") as f:
            f.write(dowloaded_file)
        with open(temp_file, "rb") as audio_file:
            transcription = grok_cliente.audio.transcriptions.create(
                file = audio_file,
                model = "whisper-large-v3",
                prompt = "Especificar contexto o pronunciación",
                response_format = "json",
                language = "es",
                temperature = 1
            )
        os.remove(temp_file)

        return transcription.text
    except Exception as error:
        print(f"Error al transcribir  {str(error)}")
        return None
    
# -------------------------- Manejadores -----------------------------

@bot.message_handler(commands=["start", "help"])
def send_welcome(message: tlb.types.Message):
    if not datosc:
        bot.reply_to(message, "Error, no se cargo el dataset, intente más tarde.")
        return
    bot.send_chat_action(message.chat.id, "typing")

    welcome_prompt = "Genera un mensaje de bienvenida para la tienda de Samsung, que incluya una breve descripción de la empresa."

    response = get_groq_response(welcome_prompt)

    if response:
        bot.reply_to(message, response)
    else:
        er = "Lo siento no pude procesar su mensaje."
        bot.reply_to(message, er)

@bot.message_handler(content_types=['text'])
def handle_text_message(message: tlb.types.Message):
    if not datosc:
        bot.reply_to(message, "No se cargo el dataset, intentar luego.")
        return
    bot.send_chat_action(message.chat.id, "typing")
    response = get_groq_response(message.text)
    if response:
        bot.reply_to(message, response)
    else:
        er = "Lo siento no pude procesar su audio."
        bot.reply_to(message, er)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: tlb.types.Message):
    if not datosc:
        bot.reply_to(message, "No está cargado el dataset.")
        return
    bot.send_chat_action(message.chat.id, 'typing')

    transcription = transcribe_voice_with_groq(message)

    if not transcription:
        bot.reply_to(message, "Lo siento, no pude transcribir tú mensaje :(")
        return
    
    response = get_groq_response(transcription)
    if response:
        bot.reply_to(message, response)
    else:
        error = "La consulta no pudo ser procesada"
        bot.reply_to(message, error)
    
if __name__ == "__main__":
    if datosc:
        print(f"bot de {datosc['company_info']['name']} iniciado correctamente")

        while True:
            try:
                bot.polling(none_stop= True, interval=0, timeout=20)
            except Exception as e:
                print(f"Error, no se pudo procesar porque {str(e)}")
                print("Reiniciando el bot")
                time.sleep(5)
    else: print("No se pudo iniciar desde la raíz...")