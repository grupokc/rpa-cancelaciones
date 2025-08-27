from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):   

    # Tome las variables del archvivo .env 
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)



    # ------------------------------------------------
    # Informacion del aplicativo 
    # ------------------------------------------------

    APP_TITLE: str = "RPA: Disminuciones y Cancelaciones"
    VERSION: str = "0.0.5"

    LOG_HEADERS: list = [
    "Fecha Extraccion",
    "Archivo Entrada",
    "Archivo Salida",
    "Total Registros",
    ]

    LOG_FILE: Path =  Path("log/ETL_log.csv")

    RESIZE_X: int = 1000 
    RESIZE_Y: int = 700


    EXCEL_PATH: Path = Path("data/bd_generadas/base.xlsx")



settings = Settings()