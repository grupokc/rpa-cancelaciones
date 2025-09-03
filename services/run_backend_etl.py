
from components import *
from models.etl_result import ETLResult
from services.Extract.extract import extract_rfc
from services.Extract.gui_messages import GUIMessages
from services.Transform.transform import transform_process_rfc
from config import settings
import pandas as pd 


def run_backend_etl(input_path: Path, cancel_flag=lambda: False) -> Optional[ETLResult]:
    """
    Ejecuta el proceso ETL completo: Extraccion y Transformacion.

    Args.
        input_path (Path): ruta del archivo de entrada (Excel) que contiene los RFC a buscar.
        cancel_flag (lambda): funcion que retorna True si se debe cancelar el proceso ETL.  

    Returns.
        Optional[ETLResult]: resultado del proceso ETL, None si fue cancelado.
    """
    df = pd.read_excel(input_path) # Cargar el archivo de entrada como un dataframe
    if df.empty:
        GUIMessages.show_error("El archivo de entrada esta vacio.")
        return None
    total_records = df.shape[0] # Conteo de registros 
    output_path, df_searched, id_unico = extract_rfc(df, column_name="RFC") 

    # Transformacion
    print(f"\nIniciando transformacion...")
    matriz = transform_process_rfc(df_searched) 
    df_result = pd.DataFrame(matriz)
    print(f"Transformacion finalizada, total registros: {df_result.shape[0]}")
    result = settings.BD_GENERADAS_DIR / f"ETL_{settings.CLAVE_EXTRACCION}_{id_unico}.xlsx"  # Ruta del archivo para guardar
    df_result.to_excel(result, index=False)
    # try:
    #     result.touch(exist_ok=True)
    # except Exception:
    #     pass
    print(df_result.head(10))
    return ETLResult(output_extract_path=output_path, total_records=total_records, output_result_path=result)

