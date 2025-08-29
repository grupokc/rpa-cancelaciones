from services.Extract import * 

# Las rutas de los directorios las trae ya el settings de config.py, además este asegura la existencia de las mismas 
# Clase base de hermes extract 
class HermesExtract: 

    def __init__(self, bd_generadoas_path: str, bd_generadas_path: str, capturas_path: str):
        self.ruta_bases_generadas = bd_generadas_path
        self.ruta_bases_generadas = bd_generadoas_path
        self.ruta_capturas_extraccion = capturas_path
        # self._inicializar_rutas()
