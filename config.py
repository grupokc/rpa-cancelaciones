"""
Encapsula todas las variables para la configuracion de la aplicacion.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
from models.vectores import Point, UIMap
import yaml 

class Settings(BaseSettings):   

    # Tome las variables del archvivo .env 
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # ---- Informacion del aplicativo ---- 
    APP_TITLE: str = "RPA: Disminuciones y Cancelaciones"
    VERSION: str = "1.0.7"
    AUTOR: str = "Mauricio Casarin"
    RESIZE_X: int = 1000 
    RESIZE_Y: int = 700

    # ---- Sobre la tabla de log ---- 
    LOG_HEADERS: list = [
        "Fecha Extraccion",
        "Archivo Origen",
        "Archivo Extraccion",
        "Total Registros",
        "Archivo Resultante",
    ]

    # ---- Ruta de directorios relevantes ---- 
    CAPTURAS_DIR: Path = Path("data/capturas")
    BD_GENERADAS_DIR:  Path = Path("data/bd_generadas")
    BD_GENERADORAS_DIR: Path =Path("data/bd_generadoras")
    STATIC_ELEMENTS_DIR: Path = Path("static")
    
    LOG_FILE: Path =  Path("log/etl_log.csv")
    
    DIRS: list  = [CAPTURAS_DIR, BD_GENERADAS_DIR, BD_GENERADORAS_DIR]

    # ---- Sobre el proceso ETL  ---- 
    CLAVE_EXTRACCION: str = "Testing"


    # ---- Vectores del Consultador  ----
    ui_file: Path = Path("vectores") # carpeta base
    ui: UIMap | None = None
    
    @field_validator("ui")
    def load_ui(cls, v, values):
        # base = values.get("ui_file", Path("config"))
        base: Path = Path("vectores") # carpeta base
        path = base / f"ui_vectores.yaml"
        if not path.exists():
            raise FileNotFoundError(f"No existe config UI: {path}")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return UIMap(**data) 

    # ---- Variables para la Transformacion ----
    CUSTOM_CONFIG: str = "dpi 300 --psm 6"
    MODELO_HERMES_OCR: str =  "Hermes_v1"
    COL_TRANSFORM: list = [
        'FILE_NAME',
        'RFC', 
        'NOMBRE'
     ]

settings = Settings()

# Asegurar que las carpetas necesarias existan
for dir in settings.DIRS: 
    dir.mkdir(parents=True, exist_ok=True)
