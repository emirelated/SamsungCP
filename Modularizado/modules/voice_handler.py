import os
from groq import Groq
from typing import Optional
from config import GROQ_API_KEY, GROQ_WHISPER_MODEL, TEMP_VOICE_FILE


class VoiceTranscriber:
    """
    Maneja la transcripción de mensajes de voz a texto.
    
    Attributes:
        client: Cliente de Groq API para Whisper
    """
    
    def __init__(self):
        """Inicializa el transcriptor de voz."""
        self.client = Groq(api_key=GROQ_API_KEY)
        print("✅ VoiceTranscriber inicializado")
    
    def transcribe(self, voice_file_bytes: bytes) -> Optional[str]:
        """
        Transcribe un archivo de audio a texto.
        
        Args:
            voice_file_bytes (bytes): Bytes del archivo de audio
            
        Returns:
            str: Texto transcrito, o None si falla
            
        Example:
            >>> transcriber = VoiceTranscriber()
            >>> with open("audio.ogg", "rb") as f:
            ...     audio_bytes = f.read()
            >>> text = transcriber.transcribe(audio_bytes)
            >>> print(text)
            "Hola, quiero información sobre los Galaxy S24"
        """
        temp_file = TEMP_VOICE_FILE
        
        try:
            # Guardar archivo temporal
            with open(temp_file, "wb") as f:
                f.write(voice_file_bytes)
            
            # Transcribir con Whisper
            with open(temp_file, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model=GROQ_WHISPER_MODEL,
                    prompt="Especificar contexto o pronunciación",
                    response_format="json",
                    language="es",
                    temperature=1
                )
            
            # Limpiar archivo temporal
            self._cleanup_temp_file(temp_file)
            
            return transcription.text
        
        except Exception as error:
            print(f"❌ Error al transcribir audio: {str(error)}")
            self._cleanup_temp_file(temp_file)
            return None
    
    def _cleanup_temp_file(self, file_path: str):
        """
        Elimina el archivo temporal de forma segura.
        
        Args:
            file_path (str): Ruta del archivo a eliminar
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"⚠️  No se pudo eliminar el archivo temporal: {e}")