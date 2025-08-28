from services.Extract import * 

from services.Extract.hermes_extract_base import HermesExtract


class HermesLoad(HermesExtract): 
    """
    Clase enfocada en la carga de la base generadora 
    
    """
    def obtener_df_base(
        self, 
        file_name: str | Path, 
        base_sinavid: bool = False,
        index_headers: int = 0
    ): 
        if isinstance(file_name, str): 
            file_name = Path(file_name)


        if not file_name.absolute().exists():
            raise FileNotFoundError(f"El archivo no exite, asegurese de cargarlo en: {self.ruta_bases_generadoras}")
        
        if base_sinavid: 
            base = pd.read_csv(file_name.absolute(), sep="\t", encoding="latin-1")

        else: 
            if file_name.suffix == '.xlsx': 
                base= pd.read_excel(file_name.absolute(), header=index_headers)

            elif file_name.suffix in ['.txt', '.csv'] :
                base = pd.read_csv(file_name.absolute(), sep=',')
    
        return base 


    def load_log_base(self, file_name: str | Path): 

        try: 
            if isinstance(file_name, str):
                file_name = Path(file_name)

            new_file_name =  file_name.stem + "_logs.txt"
            name_log = self.ruta_logs/ new_file_name
            print(name_log, "Es el nombre del log") # Debug
            with open(name_log, "w+") as log_file:
                log_file.write("")
                # Setear el nombre del log 
                self.log_file = name_log
                print(f"Log leido exitosamente: {name_log}")

        except Exception as e: 
            mensaje = f"Error al obtener el log de la base: {e}"
            print(mensaje)
            # log_error(mensaje=mensaje)


    def get_idx_log(self):

        """
        Los logs siguen la siguiente forma: 

        log = "\n%s: %d - %d" % (fecha, start, end); donde start es el incio de la extraccion, end el final de la extraccion

        """
        
        try:
            # Los logs se acomodaran del menos reciente al más reciente de arriba a abajo
            # Por lo que basta obtener el ultimo reenglon

            with open(self.log_file, 'r') as file:
                contenido = file.read().strip()
                renglones = contenido.splitlines()

                # # Si es un log nuevo entonces
                if len(renglones) == 0:
                    print("Es un nuevo log") # Debug
                    ultimo_recorrido = 0 

                if len(renglones) >0 : 
                    # Obtener el ultimo log 
                    ultimo_log = renglones[-1]
                    print(ultimo_log, "Es el ultimo log") # Debug
                    # Separarlo por el caracter de separacion que es -
                    ultimo_recorrido = int(ultimo_log.split(" - ")[-1].strip())
            
            # El inicio de esta extraccion es el final de la anterior
            start = ultimo_recorrido
            # En cada extracción avanzaremos solo 300 registros
            end = start + 300
            
            # Obtener la fecha actual
            import datetime
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            # fecha = datetime.date.now().date()

            # Agregar log actual
            log = "\n%s: %d - %d" % (fecha, start, end)

            with open(self.log_file, 'a') as file:
                file.write(log)
                print(f"{log}")

            # Devolver el rango 
            rango_esta_extraccion = [start, end]

            return rango_esta_extraccion

        except ValueError as ex:
            print(f"[Error.HermesLoad.get_idx_log] en el ultimo registro del log, verificar el log {ex}")
            return None
        except Exception as e:
            print(f"[Error.HermesLoad.get_idx_log] Error al obtener el indice de inicio: {e}")
            return None



