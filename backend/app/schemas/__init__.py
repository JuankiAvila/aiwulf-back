# app/schemas/__init__.py

# Importa tus esquemas Pydantic aquí
from .user import UserLogin, UserResponse
from .writing_schema import LLM_writing_request, LLM_writing_response, InstructionsRequest, BasicInstructionsRequest, BasicInstructionsResponse, BasicCorrectionRequest, BasicCorrectionResponse, BasicHintRequest, BasicHintResponse
