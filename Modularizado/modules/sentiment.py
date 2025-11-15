from transformers import pipeline
from typing import Optional
from config import SENTIMENT_MODEL_NAME, SENTIMENT_EMOJIS


class SentimentAnalyzer:
    """
    Clase para análisis de sentimiento en textos en español.
    
    Attributes:
        model: Pipeline de transformers para análisis de sentimiento
    """
    
    def __init__(self):
        """Inicializa el analizador y carga el modelo."""
        self.model = None
        self.load_model()
    
    def load_model(self):
        """
        Carga el modelo de análisis de sentimientos.
        Utiliza RoBERTuito optimizado para español.
        """
        if self.model is not None:
            print("⚠️  Modelo de análisis de sentimiento ya cargado.")
            return
        
        print(f"📥 Cargando modelo: {SENTIMENT_MODEL_NAME}...")
        try:
            self.model = pipeline(
                "sentiment-analysis",
                model=SENTIMENT_MODEL_NAME
            )
            print("✅ Modelo de Sentimiento cargado con éxito.")
        except Exception as e:
            print(f"❌ Error al cargar el modelo de sentimiento: {e}")
            self.model = None
    
    def analyze(self, text: str) -> str:
        """
        Analiza el sentimiento de un texto.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            str: Resultado formateado con emoji y porcentaje de confianza
            
        Example:
            >>> analyzer = SentimentAnalyzer()
            >>> result = analyzer.analyze("Estoy muy feliz con el producto")
            >>> print(result)
            📈 Análisis de Sentimiento del Cliente:
            Sentimiento Detectado: *5 STARS* 😊 
            (Confianza: 95.32%)
        """
        if self.model is None:
            return "⚠️ Modelo de Sentimiento no disponible."
        
        try:
            # Realizar análisis
            results = self.model([text])
            result = results[0]
            
            # Extraer datos
            sentiment = result['label']
            confidence = result['score']
            emoji = SENTIMENT_EMOJIS.get(sentiment, "❓")
            
            # Formatear respuesta
            formatted_response = (
                f"📈 Análisis de Sentimiento del Cliente:\n"
                f"Sentimiento Detectado: *{sentiment.upper()}* {emoji} \n"
                f"(Confianza: {confidence:.2%})"
            )
            return formatted_response
        
        except Exception as e:
            print(f"❌ Error durante el análisis de sentimiento: {e}")
            return f"Error durante el análisis del texto: {e}"
    
    def get_raw_sentiment(self, text: str) -> Optional[dict]:
        """
        Obtiene el resultado crudo del análisis sin formatear.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            dict: Diccionario con 'label' y 'score', o None si falla
        """
        if self.model is None:
            return None
        
        try:
            results = self.model([text])
            return results[0]
        except Exception as e:
            print(f"❌ Error en análisis crudo: {e}")
            return None