"""
Modulo para la transformacion de Imagenes a texto cuando la extraccion se dio por medio de la busqueda por RFC. 
Implementa algún modelo OCR, en particular Hermes_v2
"""

import pandas as pd 
from pathlib import Path
import pytesseract
from PIL import Image
from config import settings


HERMES_OCR = settings.MODELO_HERMES_OCR 
RI_RFC = settings.ui.regions.get("TABLA_RFC") # Region de interes para el recorte 
COL_NECESARIAS = settings.COL_TRANSFORM # LISTA DE COLUMNAS NECESARIAS 
CUSTOM_CONFIG_OCR = settings.CUSTOM_CONFIG


def transform_process_rfc(
    dframe : pd.DataFrame, 
    ocr: str = HERMES_OCR, 
    crop: tuple = RI_RFC, 
)-> dict: 
    """
    Transforma la imagen en texto
    
    """
    
    matriz = list()

    if not COL_NECESARIAS in dframe.columns.to_list(): 
        raise ValueError(f"El Dataframe inicial requiere la presencia de las columnas: {COL_NECESARIAS}")
    
    for i, row in dframe.iterrows(): 
        try: 
            file_name = row['FILE_NAME']

            if isinstance(file_name, str): 
                file_name = Path(file_name)
            if not file_name.exists(): 
                print(f"[Error | transform_process_rfc] el archivo: {file_name} NO existe")
                continue
            else: 
                print("-"*20, f"Transformado Imagen{i}/ {dframe.shape[0]} || Archivo: {file_name}", "-"*20)
                imagen = Image.open(file_name).convert('L').crop(crop)
                # Esto hace que la imagen sea más grande para mejorar la precisión del OCR, el Image.LANCZOS es un filtro de alta calidad
                imagen = imagen.resize((imagen.width * 2, imagen.height * 2), Image.LANCZOS)
                # Binarizar la imagen, ESTO SIRVE PARA MEJORAR LA PRECISION DEL OCR
                imagen = imagen.point(lambda x: 0 if x< 128 else 255, '1')

                if ocr: 
                    texto = pytesseract.image_to_string(imagen, lang=ocr, config=CUSTOM_CONFIG_OCR)
                else: 
                    texto = pytesseract.image_to_string(imagen, config=CUSTOM_CONFIG_OCR)
                contenido = "\n".join([x for x in texto.splitline() if x!=""])
                renglones = contenido.split("\n")
                for i_renglon, renglon in enumerate(renglones): 
                    data = {
                        "RFC": row['RFC'],
                        "POLIZA": "", 
                        "PROMOTORIA": "",
                        "SOLICITUD": "", 
                        "STATUS": "",
                        "FECHA_EMISION": "",
                        "NOMBRE": row['NOMBRE'],
                        "SEXO": "",
                        "RET": "",
                        "FILE_NAME": file_name
                    }
                    if renglon.strip() == "":
                        continue
                    else: 
                        pre_renglon = renglon
                        renglon = renglon.replace("|", " ").replace("(", "").replace("[", " ").replace(",", " ").replace("{", " ").replace("!", "").replace(":", "").replace(".", "").replace("  ", " ").replace("  ", " ").replace(" ", "|").strip()
                        try: 
                            partes = renglon.split("|")
                            data['POLIZA'] = partes[1].strip()
                            data['PROMOTORIA'] = partes[2].strip() if len(partes) > 2 else ""
                            data['SOLICITUD'] = partes[3].strip() if len(partes) > 3 else ""
                            data['STATUS'] = partes[4].strip() if len(partes) > 4 else ""
                            data['FECHA_EMISION'] = partes[5].strip() if len(partes) > 5 else ""
                            data['SEXO'] = partes[-4].strip() 
                            data['RET'] = partes[-3].strip() 
                        except Exception as e: 
                            try: 
                                data['POLIZA'] = renglones[1] if len(renglones) > 1 else ""
                                data['PROMOTORIA'] = renglones[2] if len(renglones) > 2 else ""
                                data['SOLICITUD'] = renglones[3] if len(renglones) > 3 else ""
                                data["FECHA_EMISION"] = renglones[4] if len(renglones) > 4 else ""
                                data["NOMBRE"] = renglones[5] if len(renglones) > 5 else ""
                                data["RET"] = renglon[7] if len(renglones) > 7 else ""
                                
                            except Exception as e: 
                                print(f"Error al extraer la imagen: {e}")
                        finally: 
                            print(data)
                    # Agregar a la matriz 
                    matriz.append(data)
        except Exception as e: 
            print(f"Ha ocurrido un error durante la Transformacion del renglon {i}: {e}")
            continue
        except KeyboardInterrupt: 
            print(f"Se ha interrumpido el proceso")
            return matriz 
        
    return matriz 