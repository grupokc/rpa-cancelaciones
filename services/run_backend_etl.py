
from components import *
from models.etl_result import ETLResult
from services.Extract.extract import extract_rfc
from services.Transform.transform import transform_process_rfc
from config import settings
import pandas as pd 


def run_backend_etl(input_path: Path, cancel_flag=lambda: False) -> Optional[ETLResult]:
    """
    Sustituye esta función por tu integración real.
    Debe retornar ETLResult o None si se canceló.
    """

    # Leer el archivo en un dframe 
    df = pd.read_excel(input_path)
    total_records = df.shape[0] # Conteo de registros 

    output_path, df_searched = extract_rfc(df, column_name="RFC")

    print(df_searched)
    # TODO: Iniciar la transformacion 


    try:
        output_path.touch(exist_ok=True)
    except Exception:
        pass
    
    # TODO: result debe ser la ruta dela archivo resultante
    result = Path(".")
    return ETLResult(output_extract_path=output_path, total_records=total_records, output_result_path=result)

