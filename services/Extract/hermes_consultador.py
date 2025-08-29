from services.Extract import * 

from services.Extract.hermes_extract_base import HermesExtract
from services.Extract.hermes_actions import HermesActions


# No parece ser necesario que hermes

class HermesConsultador(
    HermesExtract, # Para poder fijar los directorios 
    HermesActions # Para poder hacer las acciones estandares
):  
    """
    Enfocado en realizar las acciones en el consultador.
    
    """
    # Serie de clicks para llegar al consultador 
    acciones_to_rfc = {
        (388,93): "mclick",
        (415, 130): "mclick", 
        (120, 70): "mclick", # Expandir el la pestaña

    }

    # Serie de clicks para llegar al consultador 
    acciones_to_consultador = {
        (388,93): "mclick",
        (415, 115): "mclick", 
    }

    def __init__(self, delay_actions: int): 
        self.delay = delay_actions

    def buscar(self):
        """Se dara click en el boton de búsqueda del Seus"""
        self.mclick(280, 169)

    def contactos_tab(self):
        """Esta funcion se encarga de moverse a la pestaña de contactos"""
        self.mclick(218, 208)  


    def btn_limpiar(self):
        """La función toma de apoyo a mclick de hermes, y ejecuta un click en el vector fijo de limpiar campos dentro del consultador
        Retorna: None, ejecuta un click"""
        self.mclick(222, 169)
    

    def btn_bajar(self):
        """
        presiona el boton de bajar a la siguiente poliza dentro del consultador. 
        """
        self.mclick(453, 168) 

    def input_poliza(self, poliza:str):
        """
        Rellena el input de la poliza dentro del consultador.
        Args:
        poliza (str): La poliza a rellenar.

        """
        self.mclick(126, 263)
        self.fill(poliza)

    def input_nombre(self, nombre: str):
        self.mclick(502, 351)
        self.fill(nombre)


    def input_paterno(self, paterno: str ):

        self.mclick(100, 351)
        self.fill(paterno)


    def input_materno(self, materno: str):
        """ 
        """
        self.mclick(303, 351)
        self.fill(materno)


    def input_retenedor(self, retenedor: str):
        self.mclick(576, 409)
        self.fill(retenedor)

    def go_to_consultador(self):
        self.execute_this_actions(actions=self.acciones_to_consultador, delay_btween_action=self.delay)

    def go_to_rfc_inpt(self): 
        self.execute_this_actions(actions=self.acciones_to_rfc, delay_btween_action=self.delay)

    def bttn_buscar_rfc(self): 
        self.mclick(690, 267) 

    def input_rfc(self, rfc: str): 
        self.mclick(240, 403) 
        self.fill(rfc)

    def clear_input_rfc(self):
        self.mclick(222,147)

        
    def ss(self, prefijo: str, sufijo: str, path_to_save: str |  Path): 
        """La funcion se encarga de tomar una screen shot cuando sea llamada
        tipo: str (será el prefijo con el que se guardara el archivo.png); poliza: str (será el sufijo con el que se guarda el archivo)"""
        
        if not isinstance(path_to_save, str): 
            path_to_save = Path(path_to_save)

        if not path_to_save.is_dir(): 
            raise ValueError(f"path_to_save debe ser un directorio")
        
        file_name = path_to_save / f"{prefijo}_{sufijo}.png"

        # Verificar si el archivo ya existe
        if file_name.exists(): 
            repeated = file_name.resolve() 
            file_name = path_to_save / f"{prefijo}_{sufijo}_{random.randint(0, 999)}.png"
            print(f"Archivo: {repeated} ya existe, se guardo como ")
        pyautogui.screenshot().save(file_name.absolute())
        print(f"captura de pantalla guardada: {file_name.resolve()} ")
        return file_name.resolve()
    
    
    def ss_contacto(self, prefijo: str):
        """
        La función tomará captura de la pestaña de contacto del consultador, de la forma : {prefijo}_contacto.png
        Parametros:
        prefijo: str, dará el prefijo del nombre con el que será almacenada la captura, (vease docstring de la funcion ss en hermes)
        
        Retorna:
        str, name_png, retorna el nombre del archivo png
        """
        
        self.mclick(218, 207)
        time.sleep(1)
        name_png = self.ss(prefijo, "contacto", self.ruta_capturas_extraccion) # modificar el directorio para que se almacenen en una carpeta sec
        time.sleep(.8)

        return name_png

