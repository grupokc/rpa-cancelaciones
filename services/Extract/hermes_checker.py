from services.Extract import * 
from services.Extract.hermes_extract_base import HermesExtract 




class HermesChecker(HermesExtract):
    def _get_rgb(
        self,
        pix: tuple[int, int],
        delay: int=0.5, 
        pixeles: list[tuple]= None
    ) -> tuple[int, int, int]:

        if not isinstance(delay, float): 
            raise ValueError("El delay debe ser un float")
        time.sleep(delay)
        if pixeles: 
            all_rgb = list()
            for pix in pixeles: 
                try: 
                    rgb = pyautogui.pixel(pix[0], pix[1])
                    all_rgb.append(rgb)
                except Exception as e: 
                    print(f"Error en el pix: {pix}. Error: {e}")

            return all_rgb

        return pyautogui.pixel(pix[0], pix[1])
        

    def consultador_activo(self) -> bool: 
        """ 
        Indica si el consultador se encuentr activo en la pantalla para iniciar a extraer

        """
        # fIJAR LOS VECTORES 
        activo = False
        pix = (203, 229, 562, 953)
        rgb_activo = (0, 0, 128)
        # Comparar los colores de cada vector con los activos 
        if self._get_rgb(pix=(pix[0], pix[1])) == rgb_activo and  self._get_rgb(pix=(pix[2], pix[3])) != rgb_activo: 
            activo = True

        return activo 
    
    def verifica_mas_polizas(self):
        """
        Verifica si en la busqueda el asegurado tiene más polizas asociadas al nombre que se busco, de ser así, bajara a la siguiente búsqueda del consultador.

        Retorna:
        bool, True si existen más polizas, False si no existen.
        """
        time.sleep(.3)
        if self._get_rgb((748, 330)) == (245, 245, 245):
            return True
        else:
            return False
    
    def obtener_estatus_poliza(self) -> str:
        """
        la función fija  dos vectores 2-dimensional en pixeles específicos de la pantalla, y evalua la triada asociada en t momento al color de dicho vector. En particular, t momento es cuando se llame a la función.
        Dependiendo el valor de la triada asociada se define el estatus de poliza
        Ejemplo: sea (xi, yi) un vector en un pixel, para todo vector en t momento Existe una triada asociada al vector, (x1, y1) --> (ri, gi, bi) este ultimo caracteriza al color del pixel.

        Retorna:
        tipo: str, estatus de la poliza {"C" si Cancelada, "V" si vigente, "N" si no existe un poliza}

        """
    
        #  VECTORES DE CRITERIO FIJOS
        pix_1= (386, 263)
        pix_2 = (356, 260)
        # (ax, ay) = (203, 229) ya no es necesario 
        
        time.sleep(2)
        criterio_cancelada = self._get_rgb(pix_1)
        criterio_vigente = self._get_rgb(pix_2)
        
        if (criterio_cancelada == (255, 255, 255) and criterio_vigente == (255, 255, 255)):
            print("La Poliza NO EXISTE")
            estatus = "N"
        
        elif (criterio_cancelada != (255, 255, 255)):
            print("POLIZA CANCELADA")
            estatus = "C"

        elif (criterio_vigente != (255, 255, 255)):
            print("POLIZA VIGENTE")
            estatus = "V"

        return estatus



