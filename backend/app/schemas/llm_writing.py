# app/schemas/llm.py
# Versión: 1.1.0

from pydantic import BaseModel
from typing import Dict, Any

# Schemas existentes
class LLM_writing_request(BaseModel):
    aspects: str
    language: str
    level: str
    num_words: int
    user_text: str
    num_aspects: int

class LLM_writing_response(BaseModel):
    response: Dict[str, Any]

class InstructionsRequest(BaseModel):
    language: str
    level: str

class BasicInstructionsRequest(BaseModel):
    target_language: str
    native_language: str

class BasicInstructionsResponse(BaseModel):
    tema: str
    frase: str

class BasicCorrectionRequest(BaseModel):
    target_sentence: str
    target_language: str
    native_language: str
    user_translation: str

class BasicCorrectionResponse(BaseModel):
    correction: Dict[str, Any]

class BasicHintRequest(BaseModel):
    target_language: str
    native_language: str
    sentence: str

class BasicHintResponse(BaseModel):
    hint: str
