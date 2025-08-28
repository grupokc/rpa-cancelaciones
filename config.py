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
    AUTOR: str = "Mauricio Casarin"
    RESIZE_X: int = 1000 
    RESIZE_Y: int = 700

    # ---- Sobre la tabla de log ---- 
    LOG_HEADERS: list = [
        "Fecha Extraccion",
        "Archivo Entrada",
        "Archivo Salida",
        "Total Registros",
    ]

    # ---- Ruta de directorios relevantes ---- 
    CAPTURAS_DIR: Path = Path("data/capturas")
    BD_GENERADAS_DIR:  Path = Path("data/bd_generadas")
    BD_GENERADORAS_DIR: Path =Path("data/bd_generadoras")
    LOG_FILE: Path =  Path("log/etl_log.csv")
    
    DIRS: list  = [CAPTURAS_DIR, BD_GENERADAS_DIR, BD_GENERADORAS_DIR]
    # for dir in DIRS: 
    #     dir.mkdir(parents=True, exist_ok=True)

    


    # ---- Sobre el proceso ETL  ---- 
    OCR_MODEL: str = "Hermes_v1" 


settings = Settings()

# Asegurar que las carpetas necesarias existan
for dir in settings.DIRS: 
    dir.mkdir(parents=True, exist_ok=True)
