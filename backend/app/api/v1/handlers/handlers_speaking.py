# backend/app/api/v1/handlers/handlers_speaking.py
# Versión: 1.3.0

from fastapi import HTTPException, UploadFile
from typing import List, Dict, Any
import tempfile

from backend.app.schemas.speaking_schema import (
    SpeakingStartRequest,
    SpeakingStartResponse,
    SpeakingRequest,
    SpeakingResponse
)
from backend.app.services.llm_speaking import (
    start_conversation,
    generate_speaking
)
from backend.logs.logger_manager import get_llm_logger

llm_logger = get_llm_logger()

# Handler para la PRIMERA interacción => start_conversation
async def handle_speaking_start(data: SpeakingStartRequest) -> SpeakingStartResponse:
    """
    Lógica para generar el primer audio (sin user_audio).
    Mapea la difficulty => teacher, etc.
    """
    try:
        if data.difficulty == "1":
            teacher = "alpha"
        elif data.difficulty == "2":
            teacher = "nova"
        elif data.difficulty == "3":
            teacher = "fable"
        else:
            teacher = "shimmer"

        # Mapeo language_explication => "español"|"ingles"
        if data.language_explication == "1":
            language = "español"
        else:
            language = "ingles"

        # Mapeo language_class => "español","ingles","italiano","frances","aleman","portugues"
        if data.language_class == "1":
            language_class = "español"
        elif data.language_class == "2":
            language_class = "ingles"
        elif data.language_class == "3":
            language_class = "italiano"
        elif data.language_class == "4":
            language_class = "frances"
        elif data.language_class == "5":
            language_class = "aleman"
        else:
            language_class = "portugues"
        llm_logger.debug("Iniciando conversación de speaking.")
        llm_logger.debug(f"Datos de entrada: {data}")
        llm_logger.debug(f"Datos mapeados: {teacher}, {language}, {language_class}")
        result = await start_conversation(
            difficulty_level=data.difficulty,
            language=language,
            teacher=teacher,
            language_class=language_class
        )
        # result => {"professor_text","professor_audio"}
        return SpeakingStartResponse(
            professor_text=result["professor_text"],
            professor_audio=result["professor_audio"]
        )

    except Exception as e:
        llm_logger.error(f"Error en handle_speaking_start: {e}")
        raise HTTPException(status_code=500, detail="Error interno al iniciar la conversación de speaking.")


# Handler para las interacciones POSTERIORES => generate_speaking
async def handle_speaking(
    difficulty: str,
    target_language: str,
    native_language: str,
    user_audio: UploadFile
) -> SpeakingResponse:
    """
    Recibe user_audio => lo guarda => llama a generate_speaking(...) => 
    Devuelve el audio y texto del profesor
    """
    try:
        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            content = await user_audio.read()
            tmp.write(content)

        # Ejemplo: conversation_history vacío, 
        # O podrías reconstruirlo desde la sesión
        conversation_history: List[Dict[str,Any]] = []

        # Mapeo "alpha"|"nova"|"fable"|"shimmer" => "1"|"2"|"3"|"4"
        # (Ajusta según tu front)
        # Aquí, asumo si 'difficulty' ya es 'alpha', mapeas => "1"
        if difficulty == "alpha":
            diff_level="1"
            teacher="alpha"
        elif difficulty=="nova":
            diff_level="2"
            teacher="nova"
        elif difficulty=="fable":
            diff_level="3"
            teacher="fable"
        else:
            diff_level="4"
            teacher="shimmer"

        llm_logger.info(f"Datos de entrada: {difficulty}, {target_language}, {native_language}")
        llm_logger.info(f"Datos mapeados: {diff_level}, {teacher}, {target_language}")
        result = await generate_speaking(
            audio_file_path=tmp_path,
            conversation_history=conversation_history,
            difficulty_level=diff_level,
            language=target_language,
            teacher=teacher,
            language_class=target_language,  # Podrías mapear "es" => "español"
            api_key="TU_API_KEY"  # O lo sacas de .env
        )
        # result => {"professor_text","professor_audio"(bytes)}

        # Devolvemos base64 en SpeakingResponse
        return SpeakingResponse(
            professor_text=result["professor_text"],
            professor_audio=result["professor_audio"]
        )

    except Exception as e:
        llm_logger.error(f"Error en handle_speaking: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar speaking.")
