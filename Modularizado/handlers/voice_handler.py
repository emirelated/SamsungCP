import telebot as tlb
from modules.voice_handler import VoiceTranscriber
from modules.groq_handler import GroqHandler
from modules.sentiment import SentimentAnalyzer


def register_voice_handler(bot: tlb.TeleBot, voice_transcriber: VoiceTranscriber,
                          groq_handler: GroqHandler, sentiment_analyzer: SentimentAnalyzer,
                          dataset: dict):
    """
    Registra el handler de mensajes de voz en el bot.
    
    Args:
        bot: Instancia del bot de Telegram
        voice_transcriber: Transcriptor de audio a texto
        groq_handler: Handler para comunicación con Groq
        sentiment_analyzer: Analizador de sentimientos
        dataset: Dataset de la empresa
    """
    
    @bot.message_handler(content_types=['voice'])
    def handle_voice_message(message: tlb.types.Message):
        """
        Procesa mensajes de voz del usuario.
        
        Flujo:
        1. Valida que el dataset esté cargado
        2. Descarga el archivo de audio
        3. Transcribe el audio a texto
        4. Obtiene respuesta del chatbot
        5. Envía transcripción + respuesta
        6. Analiza sentimiento de la transcripción
        7. Envía análisis de sentimiento
        
        Args:
            message: Mensaje de voz de Telegram recibido
        """
        # Validar dataset
        if not dataset:
            bot.reply_to(message, "⚠️ No está cargado el dataset.")
            return
        
        # Indicar que está procesando
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Descargar archivo de voz
        try:
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
        except Exception as e:
            print(f"❌ Error al descargar archivo de voz: {e}")
            bot.reply_to(message, "Error al descargar el archivo de voz.")
            return
        
        # Transcribir audio
        transcription = voice_transcriber.transcribe(downloaded_file)
        
        if not transcription:
            bot.reply_to(message, "Lo siento, no pude transcribir tú mensaje 😔")
            return
        
        # Obtener respuesta del chatbot
        groq_response = groq_handler.get_response(transcription)
        
        if groq_response:
            response_text = f"*Transcripción:* {transcription}\n\n{groq_response}"
            bot.reply_to(message, response_text, parse_mode='Markdown')
        else:
            bot.reply_to(message, "La consulta no pudo ser procesada")
            return
        
        # Análisis de sentimiento
        bot.send_chat_action(message.chat.id, "typing")
        sentiment_result = sentiment_analyzer.analyze(transcription)
        bot.send_message(
            chat_id=message.chat.id,
            text=sentiment_result,
            parse_mode='Markdown'
        )
    
    print("✅ Handler de voz registrado")