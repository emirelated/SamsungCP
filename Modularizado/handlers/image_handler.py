import telebot as tlb
from modules.image_handler import ImageAnalyzer


def register_image_handler(bot: tlb.TeleBot, image_analyzer: ImageAnalyzer):
    """
    Registra el handler de imágenes en el bot.
    
    Args:
        bot: Instancia del bot de Telegram
        image_analyzer: Analizador de imágenes
    """
    
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message: tlb.types.Message):
        """
        Procesa imágenes enviadas por el usuario.
        
        Flujo:
        1. Notifica que está procesando la imagen
        2. Descarga la imagen en mayor resolución
        3. Analiza el contenido con IA de visión
        4. Envía descripción + enlace al catálogo
        
        Args:
            message: Mensaje con foto de Telegram
        """
        try:
            # Notificar procesamiento
            bot.reply_to(message, "📸 Leyendo tu imagen...")
            
            # Descargar imagen (usar la de mayor resolución)
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Analizar imagen
            description = image_analyzer.analyze(downloaded_file)
            
            if description:
                bot.reply_to(message, description, parse_mode='Markdown')
            else:
                bot.reply_to(
                    message, 
                    "❌ No pude analizar la imagen. Por favor, intenta con otra imagen."
                )
        
        except Exception as e:
            print(f"❌ Error al procesar la imagen: {e}")
            bot.reply_to(
                message, 
                "⚠️ Ocurrió un error al procesar tu imagen. Intenta de nuevo."
            )
    
    print("✅ Handler de imágenes registrado")