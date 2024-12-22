# app/api/v1/handlers/handlers_writing.py
# Versión: 1.0.1

from fastapi import HTTPException
from backend.app.services.llm_writing import (
    generate_writing_correction,
    generate_writing_instructions,
    generate_basic_writing_correction,
    generate_basic_writing_hint,
    generate_basic_writing_instructions
)
from backend.app.schemas.writing_schema import (
    LLM_writing_request,
    LLM_writing_response,
    InstructionsRequest,
    BasicInstructionsRequest,
    BasicInstructionsResponse,
    BasicCorrectionRequest,
    BasicCorrectionResponse,
    BasicHintRequest,
    BasicHintResponse
)

from backend.logs.logger_manager import get_llm_logger, get_app_logger

llm_logger = get_llm_logger()
app_logger = get_app_logger()

async def handle_llm_writing(data: LLM_writing_request) -> LLM_writing_response:
    """
    Procesa la corrección del texto enviado por el usuario.
    """
    try:
        correction_response = await generate_writing_correction(
            native_language=data.native_language,
            aspects=data.aspects,
            language=data.language,
            level=data.level,
            num_words=data.num_words,
            user_written_text=data.user_text,
            num_aspects=data.num_aspects
        )
        llm_logger.info(f"Respuesta de corrección generada correctamente: {correction_response}")
        return LLM_writing_response(response=correction_response)
    except Exception as e:
        llm_logger.error(f"Error en handle_llm_writing: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la corrección de escritura.")

async def handle_writing_instructions(data: InstructionsRequest):
    """
    Obtiene las instrucciones iniciales y detalles del ejercicio de escritura.
    """
    try:
        instructions = await generate_writing_instructions(
            native_language=data.native_language,
            language=data.language,
            level=data.level
        )
        llm_logger.info(f"Instrucciones generadas correctamente: {instructions}")

        # Retornar un diccionario con las instrucciones y el ejercicio
        return instructions

    except Exception as e:
        llm_logger.error(f"Error en handle_writing_instructions: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener las instrucciones del ejercicio.")

# Nuevos Handlers para Funcionalidades Básicas

async def handle_basic_writing_instructions(data: BasicInstructionsRequest) -> BasicInstructionsResponse:
    """
    Obtiene las instrucciones y la frase básica para traducción.
    """
    try:
        instructions = await generate_basic_writing_instructions(
            language_class=data.target_language,
            native_language=data.native_language
        )
        llm_logger.info(f"Instrucciones básicas generadas correctamente: {instructions}")

        return BasicInstructionsResponse(
            tema=instructions["tema"],
            frase=instructions["frase"]
        )
    except Exception as e:
        llm_logger.error(f"Error en handle_basic_writing_instructions: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener las instrucciones básicas de escritura.")

async def handle_basic_writing_correction(data: BasicCorrectionRequest) -> BasicCorrectionResponse:
    """
    Procesa la corrección de una traducción básica enviada por el usuario.
    """
    try:
        llm_logger.info(f"Datos recibidos del frontend: {data}")
        llm_logger.info(f"target_sentence:{data.target_sentence}")
        llm_logger.info(f"user_translation:{data.user_translation}")
        llm_logger.info(f"target_language:{data.target_language}")
        llm_logger.info(f"native_language:{data.native_language}")
        correction = await generate_basic_writing_correction(
            sentence=data.target_sentence,
            language_class=data.target_language,
            native_language=data.native_language,
            user_written_text=data.user_translation
        )
        llm_logger.info(f"Corrección básica generada correctamente: {correction}")

        return BasicCorrectionResponse(correction=correction)
    except Exception as e:
        llm_logger.error(f"Error en handle_basic_writing_correction: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la corrección básica de escritura.")

async def handle_basic_writing_hint(data: BasicHintRequest) -> BasicHintResponse:
    """
    Proporciona una pista para traducir una frase básica.
    """
    try:
        llm_logger.info(f"Datos recibidos del frontend: {data}")
        llm_logger.info(f"sentence:{data.sentence}")
        hint = await generate_basic_writing_hint(
            language_class=data.target_language,
            native_language=data.native_language,
            sentence=data.sentence
        )
        llm_logger.info(f"Pista básica generada correctamente: {hint}")

        return BasicHintResponse(hint=hint)
    except Exception as e:
        llm_logger.error(f"Error en handle_basic_writing_hint: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener la pista básica de escritura.")
