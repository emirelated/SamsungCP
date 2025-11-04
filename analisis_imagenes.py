import os
import base64
import telebot
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_TOKEN = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está configurado en las variables de entorno.")
if not GROQ_TOKEN:
    raise ValueError("GROQ_TOKEN no está configurado en las variables de entorno.")


bot = telebot.TeleBot(TELEGRAM_TOKEN)
cliente_groq = Groq(api_key = GROQ_TOKEN)


def imagen_a_base64(ruta_o_bytes_imagen):
    """Convierte la imagen cargada a base68 para asi enviarla a groq"""
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

## Nota: No hay una variable que sea el producto en si (Ejemplo: "Producto = 'Lavarropas'"), pq no la vi necesaria si siempre se usa el mismo enlace. Avisar con tiempo si se quiere cambiar.
def analizar_objeto_imagen(imagen_base64):
    """Envia la imagen a groq y obtiene la respuesta"""
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Respondes mensajes de una tienda de electrodomesticos de Samsung, y ninguna otra marca. Por favor, busca en la imagen un electrodomestico y analiza cual es. Demuestra un leve interes por este mismo. Si el electrodomestico es un celular, televisor, heladera, notebook o lavarropas, recomienda seguir el enlace al final del mensaje y revisar el catalogo por mas productos del mismo tipo. No envies ningun otro enlace, y no brindes informacion tecnica sobre productos de otras marcas. El cliente debe estar interesado por la tienda."
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

            model= "meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=750  # ???
        )
        return completado_chat.choices[0].message.content
    except Exception as e:
        print(f"Error en la respuesta de imagen: {e}")
        return None

##
# Averiguar si el handler de los mensajes va en el archivo principal o si hacemos tmb cada quien el suyo
# En caso de que cada quien a lo suyo:
#codigo:
##

@bot.message_handler(commands=['start'])
def enviar_bienvenida(mensaje):
    """Mensaje de bienvenida"""
    texto_bienvenida = """
De vuelta, no se si aca iria un mensaje de bienvenida o si lo saco nomas :/
    """
    bot.reply_to(mensaje, texto_bienvenida)


@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa las imágenes enviadas por el usuario"""
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
            respuesta = f"{descripcion} \n {enlace}]"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "No pude analizar la imagen. Por favor, intenta con otra imagen.")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

##
# Fin de el codigo ese que dije antes
##

## No creo que un handler con func. lambda sea necesario aca, discutirlo
# @bot.message_handler(func=lambda mensaje: True)





# if __name__ == '__main__':
#     print("🤖 Bot de descripción de imágenes iniciado...")
#     print("📸 Esperando imágenes para describir...")
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         print(f"Error al iniciar el bot: {e}")
