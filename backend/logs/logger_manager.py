# Versión: 1.0.0

import logging
import os

class LoggerManager:
    """Manejador de diferentes loggers para la aplicación, permitiendo la creación y configuración de loggers personalizados."""
    def __init__(self):
        # Crear el directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)

    def get_logger(self, logger_name: str, log_file: str, level=logging.INFO):
        """Crea y configura un logger según el nombre, archivo y nivel especificado."""
        
        # Crear un logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        # Asegurarse de que no se añadan múltiples handlers si ya existen
        if not logger.handlers:
            # Crear un manejador para escribir en archivo
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)

            # Crear un formato para los logs
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            file_handler.setFormatter(formatter)

            # Agregar el manejador al logger
            logger.addHandler(file_handler)

        return logger

# Instancia global de LoggerManager
logger_manager = LoggerManager()

# Funciones convenientes para obtener diferentes loggers con niveles específicos
def get_app_logger(level=logging.INFO):
    """Obtiene el logger para la aplicación con el nivel especificado (INFO por defecto)."""
    return logger_manager.get_logger('app_logger', 'logs/app.log', level)

def get_llm_logger(level=logging.DEBUG):
    """Obtiene el logger para LLM con el nivel DEBUG por defecto."""
    return logger_manager.get_logger('llm_logger', 'logs/llm.log', level)

def get_auth_logger(level=logging.WARNING):
    """Obtiene el logger para autenticación con el nivel WARNING por defecto."""
    return logger_manager.get_logger('auth_logger', 'logs/auth.log', level)

def get_custom_logger(name: str, file_name: str, level=logging.INFO):
    """Crea un logger personalizado con el nivel especificado."""
    return logger_manager.get_logger(name, f'logs/{file_name}.log', level)
