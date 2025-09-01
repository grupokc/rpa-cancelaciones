"""
Modulo para la automatizacion del Consultador de Metlife 

"""

from services.Extract import * 
from services.Extract.gui_actions import GUIActions

# Directorio para almacenar las capturas tomadas 
CAPTURAS_DIR = settings.CAPTURAS_DIR

# En setttings tenemos tambien ya cargados los vectores 
VECTORES = settings.ui.points



# Hereda de la clase GUIActions 
class Consultador(GUIActions):
    """
    Clase que ejecuta las principales acciones dentro del consultador de Metlife 
    """
    def __init__(self, dir_save_ss, dir_image_locate, vectores: dict = VECTORES, ts_primary = 1, ts_secondary = 2):
        super().__init__(dir_save_ss, dir_image_locate, ts_primary, ts_secondary) # Constructor de la clase que hereda
        if not vectores: 
            raise ValueError(f"[Error.Consultador] NO se han encontrado vectores para la extraccion")
        self.vectores = vectores

    def buscar(self):
        """Se dara click en el boton de búsqueda del Seus"""
        vector = self.vectores.get("BUSCAR")
        self.mclick(vector.x, vector.y)




        

    






