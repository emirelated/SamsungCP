import json
import os
import time
import base64
from dotenv import load_dotenv
from typing import Optional
import telebot as tlb
from groq import Groq
from transformers import pipeline


MODEL_NAME = "pysentimiento/robertuito-sentiment-analysis"
ANALIZADOR = None
EMOJIS = {
    '5 stars': "😊",
    '4 stars': "🙂",
    '3 stars': "😐",
    '2 stars': "😟",
    '1 star': "😠"
}


def carga_modelo():
    """Carga el modelo de análisis de sentimientos completo de una sola vez."""
    global ANALIZADOR
    if ANALIZADOR is not None:
        print("Modelo de análisis de sentimiento ya cargado.")
        return

    print(f"Cargando modelo de análisis de sentimientos ({MODEL_NAME})...")
    try:
        ANALIZADOR = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME
        )
        print("Modelo de Sentimiento cargado con éxito. Listo para analizar textos.")
    except Exception as e:
        print(f"Error: No se pudo cargar el modelo de sentimiento. Detalle: {e}")
        ANALIZADOR = None


def analisis_sentimiento(texto: str) -> str:
    """Analiza el sentimiento de un texto y devuelve un resultado formateado."""
    if ANALIZADOR is None:
        carga_modelo()

    if ANALIZADOR is None:
        return "⚠ Modelo de Sentimiento no disponible. Ejecute 'carga_modelo()' para diagnosticar."

    try:
        resultados = ANALIZADOR([texto])
        resultado = resultados[0]
        sentimiento = resultado['label']
        confianza = resultado['score']
        emoji = EMOJIS.get(sentimiento, "❓")
        respuesta_formateada = (
            f"📈 Análisis de Sentimiento del Cliente:\n"
            f"Sentimiento Detectado: *{sentimiento.upper()}* {emoji} \n"
            f"(Confianza: {confianza:.2%})"
        )
        return respuesta_formateada

    except Exception as e:
        return f"Error durante el análisis del texto: {e}"


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("El Token de Telegram no fue cargado.")
if not GROQ_API_KEY:
    raise ValueError("El Key de Groq no fue cargado.")

bot = tlb.TeleBot(TELEGRAM_TOKEN)
grok_cliente = Groq(api_key=GROQ_API_KEY)


def cargar_datos():
    """Abre el dataset."""
    try:
        with open("dataset.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as error:
        print(f"Error al cargar el .json {str(error)}")
        return None


datosc = cargar_datos()


def get_groq_response(user_message: str):
    """Obtiene la respuesta del chatbot de Groq basado en el dataset."""
    try:
        system_prompt = (
            f"""Eres el asistente virtual de una tienda de Samsung. Tu tarea es """
            f"""responder basándote en la información proporcionada en el dataset, """
            f"""siendo *resolutivo y empático.*
            *Instrucción de Empatía:* Debes analizar el tono o el sentimiento """
            f"""implícito en el mensaje del cliente (por ejemplo: frustración, """
            f"""confusión, urgencia, alegría o interés). *Toda respuesta debe """
            f"""comenzar con una frase breve y humana que reconozca este sentimiento* """
            f"""antes de proceder con la información resolutiva.
            En caso de no encontrar la respuesta en el dataset, índica de manera """
            f"""amistosa y amable que no cuentas con esa información, sugiriendo """
            f"""contactar directamente con la empresa.

            Datos de la empresa:
            {json.dumps(datosc, ensure_ascii=False, indent=2)}

            Reglas importantes:
            1. Solo responde información proporcionada en el dataset.
            2. No inventes, añadas o busques información adicional a menos de que """
            f"""sea para proporcionar un enlace directo a la tienda en caso de que """
            f"""el cliente este buscando ESE producto en especifico.
            3. Si la información solicitada no esta en el dataset, sugiere contactar """
            f"""a https://www.samsung.com/ca/support/contact/
            4. No respondas preguntas no relacionadas con la empresa.
            5. No incluyas en tus respuestas nunca un dato sensible como el número """
            f"""de algún miembro del personal, en caso de ser solicitados debes """
            f"""responder: "No puedo brindar dicha información."
            6. *Sé empático, amable, profesional y orientado a la resolución.* """
            f"""Tu respuesta siempre debe empezar con una frase que reconozca el """
            f"""estado emocional del cliente.
                * *Ejemplos de frases empáticas:* "Entiendo perfectamente su """
                f"""frustración con este tema," "Me alegra mucho que esté """
                f"""considerando este producto," "Lamento el inconveniente que """
                f"""esto le ha causado," o "Gracias por la claridad en su consulta."
            7. Solo saluda en la primera interacción.
            8. Puedes utilizar emojis en tus respuestas, un máximo de 3.
            9. No incluyas saludos si la conversación ya fue iniciada.
            10. Siempre responde evitando la redundancia y repetición de información.
            11. Nunca envies links inactivos, en caso de que se soliciten productos """
            f"""o categorias de productos, debes proporcionar la lista completa de """
            f"""páginas que figura en el dataset.
            12. Utiliza correctamente el punto y seguido.
            13. Utiliza correctamente el punto y aparte.
            14. No brindes enlaces especificos a un producto, solo envía enlaces a la categoria del producto por ejemplo https://www.samsung.com/ar/smartphones/."""
        )

        chat_completion = grok_cliente.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content.strip()

    except Exception as error:
        print(f"No se pudo obtener la respuesta debido a que {str(error)}")
        return None


def transcribe_voice_with_groq(message: tlb.types.Message) -> Optional[str]:
    """Transcribe un mensaje de voz utilizando la API de Groq (Whisper)."""
    try:
        file_info = bot.get_file(message.voice.file_id)
        dowloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"
        with open(temp_file, "wb") as f:
            f.write(dowloaded_file)
        with open(temp_file, "rb") as audio_file:
            transcription = grok_cliente.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                prompt="Especificar contexto o pronunciación",
                response_format="json",
                language="es",
                temperature=1
            )
        os.remove(temp_file)
        return transcription.text

    except Exception as error:
        print(f"Error al transcribir {str(error)}")
        return None


def imagen_a_base64(ruta_o_bytes_imagen):
    """Convierte la imagen cargada a base68 para asi enviarla a groq."""
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')

    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None


enlace = "https://shop.samsung.com/ar/"


def analizar_objeto_imagen(imagen_base64):
    """Envia la imagen a groq y obtiene la respuesta."""
    try:
        completado_chat = grok_cliente.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": ("Respondes mensajes de una tienda de "
                                     "electrodomesticos de Samsung, y ninguna "
                                     "otra marca. Por favor, busca en la imagen "
                                     "un electrodomestico y analiza cual es. "
                                     "Demuestra un leve interes por este mismo. "
                                     "Si el electrodomestico es un celular, "
                                     "televisor, heladera, notebook o lavarropas, "
                                     "recomienda seguir el enlace al final del "
                                     "mensaje y revisar el catalogo por mas "
                                     "productos del mismo tipo. No envies ningun "
                                     "otro enlace, y no brindes informacion "
                                     "tecnica sobre productos de otras marcas. "
                                     "El cliente debe estar interesado por la "
                                     "tienda.")
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagen_base64}"
                            }
                        }
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=750
        )
        return completado_chat.choices[0].message.content

    except Exception as e:
        print(f"Error en la respuesta de imagen: {e}")
        return None


@bot.message_handler(commands=["start", "help"])
def send_welcome(message: tlb.types.Message):
    """Genera y envia un mensaje de bienvenida."""
    if not datosc:
        bot.reply_to(message, "Error, no se cargo el dataset, intente más tarde.")
        return
    bot.send_chat_action(message.chat.id, "typing")
    welcome_prompt = ("Genera un mensaje de bienvenida para la tienda de Samsung, "
                      "que incluya una breve descripción de la empresa.")
    response = get_groq_response(welcome_prompt)

    if response:
        bot.reply_to(message, response)

    else:
        er = "Lo siento no pude procesar su mensaje."
        bot.reply_to(message, er)


@bot.message_handler(content_types=['text'])
def handle_text_message(message: tlb.types.Message):
    """Responde mensajes de texto."""
    if not datosc:
        bot.reply_to(message, "No se cargo el dataset, intentar luego.")
        return
    bot.send_chat_action(message.chat.id, "typing")
    groq_response = get_groq_response(message.text)

    if groq_response:
        bot.reply_to(message, groq_response)

    else:
        er = "Lo siento no pude procesar su solicitud de chat."
        bot.reply_to(message, er)
        return

    bot.send_chat_action(message.chat.id, "typing")
    sentiment_result = analisis_sentimiento(message.text)
    bot.send_message(
        chat_id=message.chat.id,
        text=sentiment_result,
        parse_mode='HTML'
    )


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: tlb.types.Message):
    """Responde mensajes de voz."""
    if not datosc:
        bot.reply_to(message, "No está cargado el dataset.")
        return
    bot.send_chat_action(message.chat.id, 'typing')
    transcription = transcribe_voice_with_groq(message)

    if not transcription:
        bot.reply_to(message, "Lo siento, no pude transcribir tú mensaje :(")
        return
    groq_response = get_groq_response(transcription)

    if groq_response:
        bot.reply_to(message, f"*Transcripción:* {transcription}\n\n{groq_response}",
                     parse_mode='Markdown')
    else:
        error = "La consulta no pudo ser procesada"
        bot.reply_to(message, error)
        return

    bot.send_chat_action(message.chat.id, "typing")
    sentiment_result = analisis_sentimiento(transcription)
    bot.send_message(
        chat_id=message.chat.id,
        text=sentiment_result,
        parse_mode='Markdown'
    )


@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa y responde imágenes enviadas por el usuario."""
    try:
        bot.reply_to(mensaje, "Leyendo tu imagen...")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        imagen_base64 = imagen_a_base64(archivo_descargado)
        if not imagen_base64:
            bot.reply_to(mensaje, "Error al procesar la imagen. Por favor, intente nuevamente.")
            return
        descripcion = analizar_objeto_imagen(imagen_base64)
        if descripcion:
            respuesta = f"{descripcion} \n {enlace}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "No pude analizar la imagen. Por favor, intenta con otra imagen.")

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "Ocurrió un error al procesar tu imagen. Intenta de nuevo.")


if __name__ == "__main__":
    carga_modelo()
    if datosc:
        print(f"bot de {datosc['company_info']['name']} iniciado correctamente")
        while True:
            try:
                bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as e:
                print(f"Error, no se pudo procesar porque {str(e)}")
                print("Reiniciando el bot")
                time.sleep(1)

    else:
        print("No se pudo iniciar desde la raíz...")
