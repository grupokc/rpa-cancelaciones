from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):   

    # Tome las variables del archvivo .env 
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)



    