# app/api/__init__.py

"""
Paquete para las rutas de la API.
"""

from fastapi import APIRouter

router = APIRouter()

from .endpoints import router as endpoints_router

router.include_router(endpoints_router)
