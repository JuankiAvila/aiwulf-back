# app/main.py
# Versión: 1.0.0

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import router as api_v1_router
from backend.app.__version__ import __version__  # Importar correctamente desde backend.app.__version__
from backend.logs.logger_manager import get_app_logger

app_logger = get_app_logger()

app_logger.info(f"Versión de la aplicación: {__version__}")

def create_app():
    app = FastAPI(
        title="AIWulf",
        version=__version__
    )
    
    # Configuración de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Cambia esto según tus necesidades
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registro de rutas
    app.include_router(api_v1_router, prefix="/api/v1")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
