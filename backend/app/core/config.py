# app/core/config.py
# Versión: 1.0.0

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Clase de configuración para almacenar variables globales.
    """

    def __init__(self):
        # Variables de  OpenAI
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
