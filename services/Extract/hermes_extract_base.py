from services.Extract import * 


# Clase base de hermes extract 
class HermesExtract: 

    ruta_logs = ""
    ruta_bases_generadoras = ""
    ruta_bases_generadas = ""
    ruta_capturas_extraccion = ""

    def __init__(self): 
        print("=" * 10)
        self._inicializar_rutas()


    # Metodos inicializadores
    def _inicializar_rutas(self):
        """
        apunta los campos de Hermes a los directorios, en caso de que no existan 
        seran creados al inicializarse
        """
        mis_directorios = self._get_paths()
        for dirname, dirpath in mis_directorios.items():
            try: 
                if dirname == "bd_generadoras":
                    self.ruta_bases_generadoras = dirpath
                    
                elif dirname == "bd_generadas":
                    self.ruta_bases_generadas = dirpath

                elif dirname == "logs":
                    self.ruta_logs = dirpath

                elif dirname == "capturas":
                    self.ruta_capturas_extraccion = dirpath

            except Exception as e:
                print(f"Error al inicializar directorios: {e}")


    def _get_paths(self) ->  dict:
        """
        Encuentra los directorios principales que seran ocupados 
        en todo el proceso para Hermes.

        """
        p = Path("..")
        
        # Devolver las rutas del directorio en un diccionario 
        our_paths = {}

        # Enlistamos las claves que deben estar presentes, en este caso son las carpetas necesarias
        keys = ["bd_generadoras", "logs", "bd_generadas", "capturas"]
        for x in p.iterdir(): # iterar directorio 
            if x.is_dir() : # Si es una carpeta
                if x.name in keys: # si el nombre de la carpeta esta en nuestras claves 
                    our_paths[x.name] = x
                    keys.remove(x.name) # Eliminar las claves que ya se han encontrado

        # Si no hubo directorios que no se encontraron, entonces los creará
        if len(keys) > 0:
            for y in keys:
                try:
                    directorio = p.absolute().resolve()
                    pre_name = os.path.join(directorio, y)
                    os.makedirs(pre_name, exist_ok=True) # si el directorio ya existe entonces no creara uno nuevo
                    print(f"Directorio {pre_name} creado con exito")
                    our_paths[y] = pre_name
                except Exception as e:
                  print(f"Error al crear el nuevo directorio: {e}")

        if len(keys) == 0 :
            print("Todos los directorios ya existen")

        return our_paths

    def __str__(self): 
        """
        Dunder metodo que define la representacion del objeto
        """
        return f"Hermes enfocado en el proceso de Extraccion"
    
    
