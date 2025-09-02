
from components import *
from models.etl_result import ETLResult
from services.Extract.extract import extract_rfc
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
    
    # Leer el archivo en un dframe 
    df = pd.read_excel(input_path)
    total_records = df.shape[0] # Conteo de registros 

    output_path, df_searched = extract_rfc(df, column_name="RFC")

    print(df_searched)

    # TODO: Iniciar la transformacion 
    matriz = transform_process_rfc(df_searched)
    
    print(f"Iniciando transformacion...")
    df_result = pd.DataFrame(matriz)
    print(f"Transformacion finalizada, total registros: {df_result.shape[0]}")
    result = settings.BD_GENERADAS_DIR / f"ETL_{settings.CLAVE_EXTRACCION}_{input_path.stem}.xlsx"
    df_result.to_excel(output_path, index=False)

    try:
        result.touch(exist_ok=True)
    except Exception:
        pass
    # TODO: result debe ser la ruta dela archivo resultante

    print(df_result.head(10))
    return ETLResult(output_extract_path=output_path, total_records=total_records, output_result_path=result)

