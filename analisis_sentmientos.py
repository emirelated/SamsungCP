## from transformers import pipeline

analizador_sentimiento = pipeline(
    "sentiment-analysis",
    model = "pysentimiento/robertuito-sentiment-analysis"
)

def analizar_sentimiento(frase):
    resultado = analizador_sentimiento(frase)[0]

    sentimiento = resultado["label"]
    confianza = resultado["score"]

    if sentimiento == "POS":
        emoji = ":)"
    elif sentimiento == "NEG":
        emoji = ">:("
    elif sentimiento == "NEU":
        emoji = ":/"
    else:
        emoji = "¿?"
    
    return f"sentimiento: {sentimiento.upper()} {emoji}\nConfianza: {confianza:.2%}"


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hola, y bienvenido a un bot de analisis de sentimientos.")

@bot.message_handler(func=lambda message: True)
def analizar_mensaje(message):
    texto = message.text
    resultado = analizar_sentimiento(texto)
    bot.reply_to(message, resultado)