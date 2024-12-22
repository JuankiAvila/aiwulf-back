# backend/app/schemas/speaking_schema.py
# Versión: 1.2.0

from pydantic import BaseModel
from typing import Optional

class SpeakingStartRequest(BaseModel):
    difficulty: str              # '1','2','3','4'
    language_explication: str     # '1' (español) o '2' (ingles)
    language_class: str           # '1','2','3','4','5','6' => español, inglés, italiano, etc.

class SpeakingStartResponse(BaseModel):
    professor_text: str
    professor_audio: str  # base64 del audio

class SpeakingRequest(BaseModel):
    difficulty: str
    target_language: str
    native_language: str
    # user_audio se envía como archivo (UploadFile), no se tipa aquí

class SpeakingResponse(BaseModel):
    professor_text: str
    professor_audio: str  # base64
