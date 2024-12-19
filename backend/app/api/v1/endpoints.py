# app/api/v1/endpoints.py
# Versión: 1.0.1

from fastapi import APIRouter, HTTPException
from backend.app.api.v1.handlers.handlers_writing import (
    handle_llm_writing,
    handle_writing_instructions,
    handle_basic_writing_instructions,
    handle_basic_writing_correction,
    handle_basic_writing_hint
)
from backend.app.api.v1.handlers.handlers_login import handle_login
from backend.app.schemas.llm_writing import (
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
from backend.app.schemas.user import UserLogin, UserResponse
from backend.logs.logger_manager import get_llm_logger, get_app_logger

llm_logger = get_llm_logger()
app_logger = get_app_logger()

# Configurar el logger para este módulo
router = APIRouter()

@router.post('/login', response_model=UserResponse)
async def login(data: UserLogin):
    try:
        response = handle_login(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /login: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /login: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post('/llm/writing', response_model=LLM_writing_response)
async def llm_writing(data: LLM_writing_request):
    """
    Endpoint para procesar y corregir textos enviados por el usuario.
    """
    try:
        response = await handle_llm_writing(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /llm/writing: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /llm/writing: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post('/llm/writing-instructions')
async def llm_writing_instructions(data: InstructionsRequest):
    """
    Endpoint para obtener las instrucciones y detalles del ejercicio de escritura.
    """
    try:
        response = await handle_writing_instructions(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /llm/writing-instructions: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /llm/writing-instructions: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener las instrucciones del ejercicio.")

@router.post('/llm/basic-writing-instructions', response_model=BasicInstructionsResponse)
async def llm_basic_writing_instructions(data: BasicInstructionsRequest):
    """
    Endpoint para obtener instrucciones básicas y una frase para traducción.
    """
    try:
        response = await handle_basic_writing_instructions(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /llm/basic-writing-instructions: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /llm/basic-writing-instructions: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener las instrucciones básicas de escritura.")

@router.post('/llm/basic-writing-correction', response_model=BasicCorrectionResponse)
async def llm_basic_writing_correction(data: BasicCorrectionRequest):
    """
    Endpoint para procesar y corregir una traducción básica enviada por el usuario.
    """
    try:
        response = await handle_basic_writing_correction(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /llm/basic-writing-correction: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /llm/basic-writing-correction: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la corrección básica de escritura.")

@router.post('/llm/basic-writing-hint', response_model=BasicHintResponse)
async def llm_basic_writing_hint(data: BasicHintRequest):
    """
    Endpoint para obtener una pista para traducir una frase básica.
    """
    try:
        response = await handle_basic_writing_hint(data)
        return response
    except HTTPException as http_exc:
        llm_logger.error(f"HTTPException en /llm/basic-writing-hint: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        llm_logger.error(f"Error inesperado en /llm/basic-writing-hint: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener la pista básica de escritura.")
