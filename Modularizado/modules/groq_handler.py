import json
from groq import Groq
from typing import Optional
from config import (
    GROQ_API_KEY, 
    GROQ_CHAT_MODEL, 
    CHAT_TEMPERATURE, 
    CHAT_MAX_TOKENS,
    SAMSUNG_SUPPORT_URL
)


class GroqHandler:
    """
    Maneja las interacciones con la API de Groq.
    
    Attributes:
        client: Cliente de Groq API
        dataset: Dataset con información de la empresa
    """
    
    def __init__(self, dataset: dict):
        """
        Inicializa el handler de Groq.
        
        Args:
            dataset (dict): Dataset con información empresarial
        """
        self.client = Groq(api_key=GROQ_API_KEY)
        self.dataset = dataset
        print("✅ GroqHandler inicializado")
    
    def get_response(self, user_message: str) -> Optional[str]:
        """
        Obtiene respuesta del chatbot basada en el dataset.
        
        Args:
            user_message (str): Mensaje del usuario
            
        Returns:
            str: Respuesta generada por el modelo, o None si falla
        """
        try:
            system_prompt = self._build_system_prompt()
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=GROQ_CHAT_MODEL,
                temperature=CHAT_TEMPERATURE,
                max_tokens=CHAT_MAX_TOKENS
            )
            
            return chat_completion.choices[0].message.content.strip()
        
        except Exception as error:
            print(f"❌ Error al obtener respuesta de Groq: {str(error)}")
            return None
    
    def _build_system_prompt(self) -> str:
        """
        Construye el system prompt con el dataset y reglas de negocio.
        
        Returns:
            str: System prompt completo
        """
        return f"""Eres el asistente virtual de una tienda de Samsung. Tu tarea es \
responder basándote en la información proporcionada en el dataset, \
siendo *resolutivo y empático.*

*Instrucción de Empatía:* Debes analizar el tono o el sentimiento \
implícito en el mensaje del cliente (por ejemplo: frustración, \
confusión, urgencia, alegría o interés). *Toda respuesta debe \
comenzar con una frase breve y humana que reconozca este sentimiento* \
antes de proceder con la información resolutiva.

En caso de no encontrar la respuesta en el dataset, índica de manera \
amistosa y amable que no cuentas con esa información, sugiriendo \
contactar directamente con la empresa.

Datos de la empresa:
{json.dumps(self.dataset, ensure_ascii=False, indent=2)}

Reglas importantes:
1. Solo responde información proporcionada en el dataset.
2. No inventes, añadas o busques información adicional a menos de que \
sea para proporcionar un enlace directo a la tienda en caso de que \
el cliente este buscando ESE producto en especifico.
3. Si la información solicitada no esta en el dataset, sugiere contactar \
a {SAMSUNG_SUPPORT_URL}
4. No respondas preguntas no relacionadas con la empresa.
5. No incluyas en tus respuestas nunca un dato sensible como el número \
de algún miembro del personal, en caso de ser solicitados debes \
responder: "No puedo brindar dicha información."
6. *Sé empático, amable, profesional y orientado a la resolución.* \
Tu respuesta siempre debe empezar con una frase que reconozca el \
estado emocional del cliente.
    * *Ejemplos de frases empáticas:* "Entiendo perfectamente su \
frustración con este tema," "Me alegra mucho que esté \
considerando este producto," "Lamento el inconveniente que \
esto le ha causado," o "Gracias por la claridad en su consulta."
7. Solo saluda en la primera interacción.
8. Puedes utilizar emojis en tus respuestas, hasta un máximo de 3.
9. No incluyas saludos si la conversación ya fue iniciada.
10. Siempre responde evitando la redundancia y repetición de información.
11. Nunca envies links inactivos, en caso de que se soliciten productos \
o categorias de productos, debes proporcionar la lista completa de \
páginas que figura en el dataset.
12. Utiliza correctamente el punto y seguido.
13. Utiliza correctamente el punto y aparte.
14. No brindes enlaces especificos a un producto, solo envía enlaces a la categoria del producto por ejemplo https://www.samsung.com/ar/smartphones/."""