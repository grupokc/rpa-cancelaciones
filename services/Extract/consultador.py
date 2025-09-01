"""
Modulo para la automatizacion del Consultador de Metlife 

"""

from services.Extract import * 
from services.Extract.gui_actions import GUIActions
from models.vectores import Point


# Directorio para almacenar las capturas tomadas 
CAPTURAS_DIR = settings.CAPTURAS_DIR

# En setttings tenemos tambien ya cargados los vectores 
VECTORES = settings.ui.points

# Settings ya trae las carpetas que nos interesan 
DIR_SAVE_SS = settings.CAPTURAS_DIR
DIR_IMAGE_LOCATE = settings.STATIC_ELEMENTS_DIR


# Hereda de la clase GUIActions 
class Consultador(GUIActions):
    """
    Clase que ejecuta las principales acciones dentro del consultador de Metlife 
    """
    def __init__(self, dir_save_ss=DIR_SAVE_SS, dir_image_locate=DIR_IMAGE_LOCATE, vectores: dict = VECTORES, ts_primary = 1, ts_secondary = 2):
        super().__init__(dir_save_ss, dir_image_locate, ts_primary, ts_secondary) # Constructor de la clase que hereda
        if not vectores: 
            raise ValueError(f"[Error.Consultador] NO se han encontrado vectores para la extraccion")
        self.vectores = vectores

    def buscar(self):
        """Se dara click en el boton de búsqueda del Seus"""
        x, y = self._get_vector("BUSCAR")
        self.mclick(x, y)

    def contactos_tab(self): 
        x, y = self._get_vector("TAB_CONTACTOS")
        self.mclick(x, y)

    def btn_limpiar(self):
        """La función toma de apoyo a mclick de hermes, y ejecuta un click en el vector fijo de limpiar campos dentro del consultador
        Retorna: None, ejecuta un click"""
        x, y = self._get_vector("LIMPIAR")
        self.mclick(x, y)

    def btn_bajar(self):
        """
        presiona el boton de bajar a la siguiente poliza dentro del consultador. 
        """
        x, y = self._get_vector("BAJAR")
        self.mclick(x, y)

    def input_poliza(self, poliza:str):
        """
        Rellena el input de la poliza dentro del consultador.
        Args:
        poliza (str): La poliza a rellenar.
        """
        x, y = self._get_vector("INP_POLIZA")
        self.mclick(x, y)
        self.fill(poliza)

    def input_nombre(self, nombre: str):
        x, y = self._get_vector("INP_NOMBRE")
        self.mclick(x, y)
        self.fill(nombre)

    def input_paterno(self, paterno: str ):
        x, y = self._get_vector("INP_PATERNO")
        self.mclick(x, y)
        self.fill(paterno)

    def input_materno(self, materno: str):
        x, y = self._get_vector("INP_MATERNO")
        self.mclick(x, y)
        self.fill(materno)

    def input_retenedor(self, retenedor: str):
        x, y = self._get_vector("INP_RETENEDOR")
        self.mclick(x, y)
        self.fill(retenedor)

    def bttn_buscar_rfc(self): 
        x, y = self._get_vector("BUSCAR_RFC")
        self.mclick(x, y)

    def input_rfc(self, rfc: str): 
        x, y = self._get_vector("INP_RFC")
        self.mclick(x, y)
        self.fill(rfc)

    def clear_input_rfc(self):
        x, y = self._get_vector("BORRAR_RFC")
        self.mclick(x, y)

    def go_to_rfc_inpt(self): 
        (a, b) = self._get_vector("GENERALES")
        (c, d) = self._get_vector("GENERALES_RFC")
        (e, f) = self._get_vector("EXPANDIR_RFC")
        flow = [(a, b), (c, d), (e,f)]    
        self.execute_clicks(vectores_acciones=flow)

    def go_to_consultador(self): 
        (a, b) = self._get_vector("GENERALES")
        (c, d) = self._get_vector("GENERALES_CONSULTADOR")
        flow = [(a, b), (c, d)]
        self.execute_clicks(vectores_acciones=flow)

    
    def _search_rfc(
        self,
        rfc: str,
        is_start_home: bool = False, 
        screen_shot: bool = True
    ):
        if is_start_home: 
            self.go_to_rfc_inpt()
            
        time.sleep(2)
        self.input_rfc(rfc=rfc)
        self.bttn_buscar_rfc()

        if screen_shot:
            time.sleep(1.2) 
            file_name = self.ss(f"rfc_{rfc}")

        self.mclick(656,146)
        return file_name if screen_shot else None
    

    # def search_many_rfc(
    #     self, 
    #     rfc_list: list[str], 
    #     dela
    # )



    def _get_vector(self, key): 
        try: 
            vector = self.vectores.get(key)
            if not isinstance(vector, (Point, tuple)): 
                raise ValueError(f"[Error.Consultador | _get_vector] no es una tupla el vector: {e}")
            return vector.x, vector.y
        
        except Exception as e: 
            return None

    






