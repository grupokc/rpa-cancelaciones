"""
Ejecuta acciones básicas dentro de la GUI, sirve como clase base para 
hermes y sus derivados
"""

from services.Extract import *
from services.Extract.gui_messages import GUIMessages


class GUIActions(GUIMessages): 
    def __init__(self, dir_save_ss: str, dir_image_locate: str,ts_primary: int = 1, ts_secondary: int = 2, ): 
        print(f"Inicializado")
        self.ts_primary = ts_primary
        self.ts_secondary = ts_secondary
        try: 
            self.dir_save_ss = Path(dir_save_ss)
            self._check_dir(dir_save_ss)
            self.dir_image_locate = Path(dir_image_locate)
            self._check_dir(dir_image_locate)
        except Exception as e: 
            print(f"[Error.GUIActions] error al inicializar la clase: {str(e)}")

    def move(self, x, y, hold: int = 1): 
        """
        Mueve el cursor al pixel formado por las entradas x, y
        """
        pyautogui.moveTo(x,y, duration=hold)

    def mclick(self, x, y, button: Literal['primary', 'secondary'] = 'primary'): 
        """
        Mueve el cursor y ejecuta un click derecho en la posicion del pixel (x, y)
        """
        self.move(x, y)
        pyautogui.click(x, y, button=button)
    
    def fill(self, text: str): 
        """
        Escribe el texto que se pase por el argumento 
        """
        try: 
            text = str(text)
            keyboard.write(text=text, delay=0.2)
        except Exception as e: 
            print(f"[Error | GUIActions] : {str(e)}")

    def press(self, key: str | list, presses: int = 1, interval: float = 0): 
        pyautogui.press(keys=key, presses=presses, interval=interval)

    def ss(self, file_name: str, region: tuple[int, int, int, int], all_screens=True) -> Path: 
        """ 
        Toma una captura de pantalla, la guarda en el directorio que se paso en el constructor y el nombre dado en el argumento file_name,
        si region no es nulo, tomara solo la screen de la region dada. 

        Args. 
            file_name (str): nombre del archivo para guardar la captura tomada. 
            region (tuple[int, int, int, int]): tupla del recorte de la imagen. 
        """
        file_path = self.dir_save_ss / f"{file_name}.png" # Nombre completo del nuevo archivo 
        screen = pyautogui.screenshot(region=region, allScreens=all_screens)
        screen.save(file_path)
        return file_path.resolve()

    def locate_image(self, filename_image: str, region: tuple[int, int, int, int]= None)-> bool: 
        """
        Localiza en la GUI la imagen que se proporcione en el argumento, estas imagenes deben estar cargadas todas en una misma carpeta, y dicha carpeta se dbe pasar en el constructor. 

        Notes. 
            Las imagenes deben estar guardadas en formato .png.

        Args. 
            filename_image (str): nombre de la imagen. Se formara al tomar {self.dir_image_locate} / {filename_image}
        """
        file_path = self.dir_image_locate / f"{filename_image}.png"
        try: 
            element_location = pyautogui.locateOnScreen(image=f"{file_path.resolve()}", minSearchTime=1.5, region=region, grayscale=False, confidence=0.8)
            print(element_location)
        except pyautogui.ImageNotFoundException: 
            print(f"No Fue posible localizar la imagen")
            return False
        except Exception as e: 
            print(f"[Error | GUIActions] al localizar la imagen: {str(e)}")
            return False

    def locate_and_click(self, filename_image: str, region: tuple[int, int, int, int]= None, button: Literal['primary', 'secondary'] = 'primary')-> bool: 
        """
        Localiza en la GUI la imagen que se proporcione en el argumento, estas imagenes deben estar cargadas todas en una misma carpeta, y dicha carpeta se dbe pasar en el constructor. 

        Notes. 
            Las imagenes deben estar guardadas en formato .png.

        Args. 
            filename_image (str): nombre de la imagen. Se formara al tomar {self.dir_image_locate} / {filename_image}
        """
        file_path = self.dir_image_locate / f"{filename_image}.png"
        try: 
            element_location = pyautogui.locateOnScreen(image=f"{file_path.resolve()}", minSearchTime=1.5, region=region, grayscale=False, confidence=0.8)
            print(element_location)
            if element_location: 
                x, y = pyautogui.center(element_location)
                self.mclick(x, y, button=button)
                return True
            return False
        except pyautogui.ImageNotFoundException: 
            print(f"No Fue posible localizar la imagen")
            return False
        except Exception as e: 
            print(f"[Error | GUIActions] al localizar la imagen: {str(e)}")
            return False
        
    def _check_dir(self, dir: str): 
        dir_path = Path(dir)
        if not dir_path.exists(): 
            raise FileNotFoundError(f"[Error | GUIActions] El directorio {dir} NO EXISTE")
        if not dir_path.is_dir():
            raise ValueError(f"[Error | GUIActions] {dir} NO es un directorio ")
        return True
