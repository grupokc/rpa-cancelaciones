from services.Extract import * 
from services.Extract.consultador import Consultador



class SearchInSeus(Consultador): 
    
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
    
    
    def search_many_rfc(
        self, 
        data: pd.DataFrame,
        delay_btwn_searches: int, 
    ):
        searched = list()
        for i, row in data.iterrows(): 
            try: 
                asegurado = row['NOMBRE']
                rfc = row['RFC']
                try:
                    rfc = rfc[:10]
                except Exception:
                    rfc = rfc 
                    
                time.sleep(delay_btwn_searches)
                self.clear_input_rfc()
                print(f"Busqueda Numero: {i} // {data.shape[0]} || Rfc: {rfc}")
                # start_in_home = True if id == 0 else False
                start_in_home = True if pyautogui.pixel(180, 666) == (0,0, 128) else False
                file_name_rfc = self._search_rfc(rfc, is_start_home=start_in_home, screen_shot=True)
                if file_name_rfc: 
                    searched.append({
                        "RFC": rfc,
                        "FILE_NAME": file_name_rfc, 
                        "NOMBRE": asegurado
                    })
            except Exception as e: 
                msg = f"[Error.SearchInSeus | search_many_rfc] error al buscar el rfc {rfc}: {str(e)}"
                print(msg)
                continue
        return searched
