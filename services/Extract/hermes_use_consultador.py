from services.Extract import * 
from services.Extract.hermes_consultador import HermesConsultador



class HermesUseConsultador(HermesConsultador): 
    ruta_capturas = Path('../capturas') 

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
            file_name = self.ss(prefijo="rfc", sufijo=str(rfc), path_to_save=self.ruta_capturas)

        self.mclick(656,146)
        return file_name if screen_shot else None
    
    
    def search_many_rfc(
        self, 
        rfc_list: list[str],
        delay_btwn_searches: int
    ):
        searched = list()
        for id, rfc in enumerate(rfc_list): 
            time.sleep(delay_btwn_searches)
            self.clear_input_rfc()
            print(f"Busqueda Numero: {id} // {len(rfc_list)} || Rfc: {rfc}")
            # start_in_home = True if id == 0 else False
            start_in_home = True if pyautogui.pixel(180, 666) == (0,0, 128) else False
            file_name_rfc = self._search_rfc(rfc, is_start_home=start_in_home, screen_shot=True)

            if file_name_rfc:
                searched.append({
                    "RFC": rfc,
                    "FILE_NAME": file_name_rfc
                })
        
        return searched
