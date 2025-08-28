from services.Extract import * 
# Las demas clases heredaran de Hermes Extract 


class HermesActions(): 

    """
    Hermes en Extraccion, especializado en realizar acciones, tales como
    escribir, click, screenshot, 
    """

    def mclick(self, a, b):
        """la funcion se encargara de moverse al vector (a, b) para posterioremente hacer click sobre el
        a : x-axis ; b: y-axis"""
        time.sleep(.4)
        pyautogui.moveTo(a, b)
        pyautogui.click()
    

    def get_click(self):
        """
        Esta funcion tiene un proposito exploratorio, pues nos ayuda a saber en que posicion se encuentra
        actualmente el cursor, además nos da tres segundos para poder ajustar el cursor a la posicion desada
        """
        time.sleep(3)
        (x, y) = pyautogui.position()
        return ((x, y))

    def fill(self, texto_input: str):
        """Esta funcion se encarga de escribir y mandar las teclas"""
        try:
            texto_al_input = str(texto_input)
            # Borrar con keyboard
            keyboard.write(texto_al_input)
        except Exception as e:
            print(f"Error: {e}")


    def rellenar(self, argument, x, y):
        """
        La funcion concatena a las funciones mclick, y new_fill.
        """
        self.mclick(x,y)
        time.sleep(0.3)
        self.fill(argument)



    def execute_this_actions(self,
        actions: dict[tuple | str : Literal["fill", "mclick"]], 
        delay_btween_action: int = 0 
        ) -> bool: 
        """ 
        Ejecuta las acciones que se declaren en actions, el cual debe tener la forma:
        acciones = {
        (x2, y2): "mclick",
        "Textopara rellenar": "fill",        
        (x3, 63) :  "mclick"
        }

        Dentro de las acciones permitidas se encuentran : 
            - fill: manda la cadena que se pase en key
            - mclick: mueve y hace un click en los vectores que pase el key

        Las acciones se ejecutaran en el orden en que se pasen en su diccionario. 


        """
        for order, action in actions.items():
            time.sleep(delay_btween_action)
            try: 
                if action == "mclick": 
                    self.mclick(a=order[0], b=order[1])
                if action == "fill": 
                    self.fill(order)
        
            except Exception as e: 
                print(f"[Error.HermesActions.execute_this_actions] Error al ejecutar la accion: {e} ")
                continue
        return True
              
 