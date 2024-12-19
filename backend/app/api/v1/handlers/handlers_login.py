# app/api/v1/handlers/handlers_login.py
# Versión: 1.0.0

from fastapi import HTTPException

from backend.app.schemas.user import (
    UserLogin,
    UserResponse,
)
from backend.logs.logger_manager import get_app_logger

app_logger = get_app_logger()

# Simulación de una base de datos en memoria
mock_db = {
    "juancarlos@aiwulf.com": {
        "name": "Juan Carlos",
        "password": "password1234"
    }
}

def handle_login(data: UserLogin) -> UserResponse:
    try:
        email = data.email
        password = data.password
        # Verificamos si el usuario existe en la "bd"
        if email in mock_db and mock_db[email]['password'] == password:
            # Retornamos los datos del usuario
            return UserResponse(email=email, password=password)
        else:
            # Si el usuario no existe o la contraseña está mal, devolvemos un 401
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        app_logger.error(f"Error en handle_login: {e}")
        raise HTTPException(status_code=500, detail=str(e))
