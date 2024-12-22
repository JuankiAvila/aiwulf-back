# backend/app/schemas/speaking_schema.py
# Versión: 1.2.0

from pydantic import BaseModel
from typing import Optional

class SpeakingStartRequest(BaseModel):
    difficulty: str  # '1','2','3','4'
    language_explication: str  # '1' => español, '2' => inglés
    language_class: str        # '1'...'6'

class SpeakingStartResponse(BaseModel):
    professor_text: str
    professor_audio: str  # Audio codificado en base64

class SpeakingRequest(BaseModel):
    difficulty: str
    target_language: str
    native_language: str
    # El archivo user_audio se envía como UploadFile, no se declara aquí.

class SpeakingResponse(BaseModel):
    professor_text: str
    professor_audio: str  # base64
