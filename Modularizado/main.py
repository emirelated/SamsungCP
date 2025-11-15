import json
import time
import telebot as tlb
from config import TELEGRAM_TOKEN, DATASET_PATH
from modules.sentiment import SentimentAnalyzer
from modules.groq_handler import GroqHandler
from modules.voice_handler import VoiceTranscriber
from modules.image_handler import ImageAnalyzer
from handlers.text_handler import register_text_handler
from handlers.voice_handler import register_voice_handler
from handlers.image_handler import register_image_handler


def load_dataset():
    """
    Carga el dataset de la empresa desde el archivo JSON.
    
    Returns:
        dict: Dataset con información de la empresa o None si falla
    """
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {DATASET_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {DATASET_PATH} no tiene formato JSON válido")
        return None
    except Exception as error:
        print(f"Error al cargar el dataset: {str(error)}")
        return None


def main():
    """Función principal del bot."""
    print("=" * 50)
    print("Iniciando Samsung Bot...")
    print("=" * 50)
    
    # Cargar dataset
    print("\n[1/5] Cargando dataset...")
    dataset = load_dataset()
    if not dataset:
        print("❌ No se pudo cargar el dataset. Abortando...")
        return
    print(f"✅ Dataset cargado: {dataset.get('company_info', {}).get('name', 'Samsung')}")
    
    # Inicializar bot de Telegram
    print("\n[2/5] Conectando con Telegram...")
    try:
        bot = tlb.TeleBot(TELEGRAM_TOKEN)
        print("✅ Bot de Telegram conectado")
    except Exception as e:
        print(f"❌ Error al conectar con Telegram: {e}")
        return
    
    # Inicializar módulos
    print("\n[3/5] Inicializando módulos de IA...")
    try:
        sentiment_analyzer = SentimentAnalyzer()
        groq_handler = GroqHandler(dataset)
        voice_transcriber = VoiceTranscriber()
        image_analyzer = ImageAnalyzer()
        print("✅ Todos los módulos inicializados correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar módulos: {e}")
        return
    
    # Registrar comando de bienvenida
    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message: tlb.types.Message):
        """Genera y envía un mensaje de bienvenida."""
        bot.send_chat_action(message.chat.id, "typing")
        welcome_prompt = (
            "Genera un mensaje de bienvenida para la tienda de Samsung, "
            "que incluya una breve descripción de la empresa."
        )
        response = groq_handler.get_response(welcome_prompt)
        
        if response:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Lo siento no pude procesar su mensaje.")
    
    # Registrar handlers
    print("\n[4/5] Registrando handlers de mensajes...")
    try:
        register_text_handler(bot, groq_handler, sentiment_analyzer, dataset)
        register_voice_handler(bot, voice_transcriber, groq_handler, sentiment_analyzer, dataset)
        register_image_handler(bot, image_analyzer)
        print("✅ Handlers registrados correctamente")
    except Exception as e:
        print(f"❌ Error al registrar handlers: {e}")
        return
    
    # Iniciar bot
    print("\n[5/5] Iniciando polling...")
    print("=" * 50)
    print(f"Bot de {dataset['company_info']['name']} ACTIVO")
    print("=" * 50)
    print("\nFuncionalidades disponibles:")
    print("   • Mensajes de texto con análisis de sentimiento")
    print("   • Transcripción de notas de voz")
    print("   • Análisis de imágenes de productos")
    print("\n⚠️  Presiona Ctrl+C para detener el bot\n")
    
    # Loop principal con manejo de errores
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot detenido por el usuario")
            print("Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"\n⚠️  Error en polling: {str(e)}")
            print("🔄 Reiniciando el bot en 5 segundos...")
            time.sleep(1)


if __name__ == "__main__":
    main()