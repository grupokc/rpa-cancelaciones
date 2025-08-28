"""
Encapsula todas las variables para la configuracion de la aplicacion.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):   

    # Tome las variables del archvivo .env 
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # ---- Informacion del aplicativo ---- 
    APP_TITLE: str = "RPA: Disminuciones y Cancelaciones"
    VERSION: str = "1.0.1"
    RESIZE_X: int = 1000 
    RESIZE_Y: int = 700
    
    # ---- Sobre la tabla de log ---- 
    LOG_HEADERS: list = [
        "Fecha Extraccion",
        "Archivo Entrada",
        "Archivo Salida",
        "Total Registros",
    ]
    LOG_FILE: Path =  Path("log/etl_log.csv")

    # ---- Sobre el proceso ETL  ---- 
    OCR_MODEL: str = "Hermes_v1" 


settings = Settings()