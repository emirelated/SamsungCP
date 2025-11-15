import telebot as tlb
from modules.groq_handler import GroqHandler
from modules.sentiment import SentimentAnalyzer


def register_text_handler(bot: tlb.TeleBot, groq_handler: GroqHandler, 
                          sentiment_analyzer: SentimentAnalyzer, dataset: dict):
    """
    Registra el handler de mensajes de texto en el bot.
    
    Args:
        bot: Instancia del bot de Telegram
        groq_handler: Handler para comunicación con Groq
        sentiment_analyzer: Analizador de sentimientos
        dataset: Dataset de la empresa
    """
    
    @bot.message_handler(content_types=['text'])
    def handle_text_message(message: tlb.types.Message):
        """
        Procesa mensajes de texto del usuario.
        
        Flujo:
        1. Valida que el dataset esté cargado
        2. Obtiene respuesta del chatbot vía Groq
        3. Envía la respuesta al usuario
        4. Analiza el sentimiento del mensaje
        5. Envía el análisis de sentimiento
        
        Args:
            message: Mensaje de Telegram recibido
        """
        # Validar dataset
        if not dataset:
            bot.reply_to(message, "⚠️ No se cargo el dataset, intentar luego.")
            return
        
        # Indicar que está escribiendo
        bot.send_chat_action(message.chat.id, "typing")
        
        # Obtener respuesta del chatbot
        groq_response = groq_handler.get_response(message.text)
        
        if groq_response:
            bot.reply_to(message, groq_response)
        else:
            bot.reply_to(message, "Lo siento no pude procesar su solicitud de chat.")
            return
        
        # Análisis de sentimiento
        bot.send_chat_action(message.chat.id, "typing")
        sentiment_result = sentiment_analyzer.analyze(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=sentiment_result,
            parse_mode='HTML'
        )
    
    print("✅ Handler de texto registrado")
