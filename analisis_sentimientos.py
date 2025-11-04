# Importamos el modelo
from transformers import pipeline

# Variable para que el modelo se cargue una sola vez
ANALIZADOR = None
EMOJIS = { # Hacemos un diccionario para simplificar
    '5 stars': "😊", # Muy positivo
    '4 stars': "🙂",  # Positivo
    '3 stars': "😐",  # Neutral
    '2 stars': "😟",  # Negativo
    '1 star':  "😠"   # Muy negativo
}

def carga_modelo(): # Para que cargue solo al inicio del bot (es muy pesado el mdoelo). 
    global ANALIZADOR # Para que se cargue una vez y sea accesible por todas las funciones
    if ANALIZADOR is not None:
        print("Modelo de analisis cargado") # Ya cargado anteriormente
        return
    
    print(f"Cargando modelo de análisis de sentimientos...")
    try:
        ANALIZADOR = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME
        )
        print("Modelo de Sentimiento cargado con éxito!! :)")
    
    except Exception as e: 
        print(f"Error: no se cargó el modelo. Reinicie el bot.")
        ANALIZADOR = None



# FUNCION DESARROLLADA EN CLASE! (a modificar y reusar para aplicarla en telegram)

# analizador_sentimiento = pipeline(
#     "sentiment-analysis",
#         model="pysentimiento/robertuito-sentiment-analysis"
# )
# print("Cargado exitosamente ✅"


# # Usamos el pipeline para obtener el sentimiento de cada frase
# print("\nAnalizando frases...")
# resultados = analizador_sentimiento(frases_para_analizar)

# # Resultados
# for frase, resultado in zip(frases_para_analizar, resultados):
#     sentimiento = resultado['label']
#     confianza = resultado['score']
    
#     # Modificamos con emojis para que quede más estetica la muestra por pantalla. 
#     emoji = "❓"
#     if "star" in sentimiento:
#         if sentimiento == '5 stars':
#             emoji = "😊" # Muy positivo
#         elif sentimiento == '4 stars':
#             emoji = "🙂" # Positivo
#         elif sentimiento == '3 stars':
#             emoji = "😐" # Neutral
#         elif sentimiento == '2 stars':
#             emoji = "😟" # Negativo
#         elif sentimiento == '1 star':
#             emoji = "😠" # Muy negativo

#     print(f"\nFrase: '{frase}'")
#     print(f"  -> Sentimiento Detectado: {sentimiento.upper()} {emoji} (Confianza: {confianza:.2%})")