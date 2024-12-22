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

async def handle_speaking_start(data: SpeakingStartRequest) -> SpeakingStartResponse:
    """
    PRIMER audio => llama a start_conversation
    """
    try:
        # Mapeos difficulty => teacher
        # '1' => 'alpha', '2' => 'nova', '3' => 'fable', '4' => 'shimmer'
        teacher_map = {
            "1": "alpha",
            "2": "nova",
            "3": "fable",
            "4": "shimmer"
        }
        teacher = teacher_map.get(data.difficulty, "shimmer")

        # language_explication => '1' => "español", '2' => "ingles"
        language_map = {
            "1": "español",
            "2": "ingles"
        }
        language = language_map.get(data.language_explication, "ingles")

        # language_class => '1' => "español", '2' => "ingles", '3' => "italiano", '4' => "frances", '5' => "aleman", '6' => "portugues"
        language_class_map = {
            "1": "español",
            "2": "ingles",
            "3": "italiano",
            "4": "frances",
            "5": "aleman",
            "6": "portugues"
        }
        language_class = language_class_map.get(data.language_class, "portugues")

        llm_logger.info(f"start_conversation => difficulty={data.difficulty}, teacher={teacher}, language_class={language_class}")

        result = await start_conversation(
            difficulty_level=data.difficulty,
            language=language,
            teacher=teacher,
            language_class=language_class
        )
        return SpeakingStartResponse(
            professor_text=result["professor_text"],
            professor_audio=result["professor_audio"]
        )
    except Exception as e:
        llm_logger.error(f"Error en handle_speaking_start: {e}")
        raise HTTPException(status_code=500, detail="Error interno al iniciar la conversación de speaking.")

async def handle_speaking(
    difficulty: str,
    target_language: str,
    native_language: str,
    user_audio: UploadFile
) -> SpeakingResponse:
    """
    Interacciones POSTERIORES => Se recibe user_audio => se transcribe => GPT => TTS
    """
    try:
        # Guardar el audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            content = await user_audio.read()
            tmp.write(content)

        # conversation_history => vacío (o recupéralo de la sesión)
        conversation_history: List[Dict[str,Any]] = []

        # Mapeo de difficulty => '1','2','3','4' si llega 'alpha','nova'...
        teacher_map = {
            "1": "alpha",
            "2": "nova",
            "3": "fable",
            "4": "shimmer"
        }
        teacher = teacher_map.get(difficulty, "shimmer")

        llm_logger.info(f"handle_speaking => difficulty={difficulty}, => mapeado => {difficulty}/{teacher}")

        # Mapeo de language_class a partir de target_language
        language_class_map = {
            'es': 'español',
            'en': 'ingles',
            'it': 'italiano',
            'fr': 'frances',
            'de': 'aleman',
            'pt': 'portugues'
        }
        language_class = language_class_map.get(target_language, 'ingles')

        llm_logger.info(f"language_class: {language_class}")

        # Llamar generate_speaking
        result = await generate_speaking(
            audio_file_path=tmp_path,
            conversation_history=conversation_history,
            difficulty_level=difficulty,
            language=target_language,
            teacher=teacher,
            language_class=language_class
        )
        return SpeakingResponse(
            professor_text=result["professor_text"],
            professor_audio=result["professor_audio"]
        )
    except Exception as e:
        llm_logger.error(f"Error en handle_speaking: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar speaking.")
