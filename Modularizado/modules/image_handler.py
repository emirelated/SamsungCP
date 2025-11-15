import base64
from groq import Groq
from typing import Optional
from config import (
    GROQ_API_KEY, 
    GROQ_VISION_MODEL, 
    VISION_TEMPERATURE, 
    VISION_MAX_TOKENS,
    SAMSUNG_SHOP_URL
)


class ImageAnalyzer:
    """
    Maneja el análisis de imágenes de productos.
    
    Attributes:
        client: Cliente de Groq API para visión
    """
    
    def __init__(self):
        """Inicializa el analizador de imágenes."""
        self.client = Groq(api_key=GROQ_API_KEY)
        print("✅ ImageAnalyzer inicializado")
    
    def analyze(self, image_bytes: bytes) -> Optional[str]:
        """
        Analiza una imagen y devuelve descripción del producto.
        
        Args:
            image_bytes (bytes): Bytes de la imagen
            
        Returns:
            str: Descripción del producto con enlace al catálogo, o None si falla
            
        Example:
            >>> analyzer = ImageAnalyzer()
            >>> with open("phone.jpg", "rb") as f:
            ...     img_bytes = f.read()
            >>> result = analyzer.analyze(img_bytes)
            >>> print(result)
            "Veo que estás interesado en un Galaxy S24..."
        """
        try:
            # Convertir imagen a base64
            image_base64 = self._bytes_to_base64(image_bytes)
            
            if not image_base64:
                return None
            
            # Analizar con modelo de visión
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self._get_vision_prompt()
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                model=GROQ_VISION_MODEL,
                temperature=VISION_TEMPERATURE,
                max_tokens=VISION_MAX_TOKENS
            )
            
            description = chat_completion.choices[0].message.content
            return f"{description}\n\n{SAMSUNG_SHOP_URL}"
        
        except Exception as e:
            print(f"❌ Error en análisis de imagen: {e}")
            return None
    
    def _bytes_to_base64(self, image_bytes: bytes) -> Optional[str]:
        """
        Convierte bytes de imagen a string base64.
        
        Args:
            image_bytes (bytes): Bytes de la imagen
            
        Returns:
            str: String base64, o None si falla
        """
        try:
            return base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            print(f"❌ Error al convertir imagen a base64: {e}")
            return None
    
    def _get_vision_prompt(self) -> str:
        """
        Obtiene el prompt para análisis de visión.
        
        Returns:
            str: Prompt configurado para identificar productos Samsung
        """
        return (
            "Respondes mensajes de una tienda de "
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
            "tienda."
        )