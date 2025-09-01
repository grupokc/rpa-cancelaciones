from services.Extract import * 


class GUIMessages(): 
    "Clase para mostrar mensajes en la GUI"
    
    def alert(self, mensaje): 
        pyautogui.alert( mensaje)

    def confirm(self, mensaje, buttons: list['str']): 
        pyautogui.confirm(mensaje, buttons=buttons)

    def prompt(self, mensaje): 
        pyautogui.prompt(mensaje)

    def password(self, mensaje): 
        pyautogui.password(mensaje)
