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

def analisis_sentimiento():
    if ANALIZADOR is None: # Para inicializar la carga única del modelo
        cargar_modelo()

    if ANALIZADOR is None: # Por si no se inicializó (doble verificación)
        return "No está disponible el modelo. Reintente nuevamente :("

    try: # Ejecutamos el analisis
        resultados = ANALIZADOR([texto])
        resultado = resultados[0]
        
        sentimiento = resultado['label'] # Devuelve la cantidad de estrellas
        confianza = resultado['score']
        
        emoji = EMOJIS.get(sentimiento, "❓")

        respuesta_corregida = (
                f"Sentimiento Detectado: {sentimiento.upper()} {emoji} "
                f"Confianza: {confianza:.2%})" # Solo con dos decimales
        )
        return respuesta_formateada
        
    except Exception as e:
        return f"Error durante el análisis del texto: {e}" # Mostramos el error almacenado. :)
