
from components import *
from models.etl_result import ETLResult
from services.Extract.extract import extract_rfc
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

    # TODO: Iniciar la transformacion 

    # # Simulación: contar filas de un .xlsx sería tu lógica real.
    # # Aquí solo dormimos y generamos nombres.
    # for _ in range(10):
    #     if cancel_flag():
    #         return None
    #     time.sleep(0.1)


    # "Calculamos" cantidad de registros
    # total_records = 1234  # Reemplaza con tu conteo real

    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_name = f"ETL_OUT_{timestamp}.xlsx"
    # output_path = settings.BD_GENERADAS_DIR / output_name

    # Aquí tu backend debe crear realmente el archivo de salida.
    # Nosotros sólo lo simulamos
    try:
        output_path.touch(exist_ok=True)
    except Exception:
        pass
    
    # TODO: result debe ser la ruta dela archivo resultante
    result = Path(".")
    return ETLResult(output_extract_path=output_path, total_records=total_records, output_result_path=result)

