from services.Extract import *
from services.Extract.search_in_seus import SearchInSeus

# Directorio para guardar las prebases 
SEARCHED_DIR = settings.BD_GENERADORAS_DIR
clave_extraccion = settings.CLAVE_EXTRACCION

def extract_rfc(
    df_base: pd.DataFrame, 
    column_name: str = 'RFC',
    dir_to_save: Path = SEARCHED_DIR, 
    delay_actions: int = 1, 
    clave_extraccion: str = clave_extraccion
) -> tuple[Path, pd.DataFrame, str]:
    """
    Busca usando las herramientas de Hermes.Extract los rfc que se proporcionen en el dataframe entrante. 

    Args. 
        df_base (pd.DataFrame): dataframe inicial para el ciclo ETL. 
        column_name (str): 
        registros_por_recorrido (int): 
        delay_actions (int)
        clave_extraccion (str)
    Returns.
        tuple[Path, pd.DataFrame, str]: ruta del archivo guardado, dataframe con los rfc buscados y el id unico del proceso.
    """
    if not column_name in df_base.columns.to_list(): 
        msg = f"El archivo no contiene la columna necesaria: {column_name}"
        raise ValueError(msg)

    # Obtener el nombre y rfc 
    data = df_base.loc[:, ['RFC', 'NOMBRE']].drop_duplicates(subset=['RFC'])
    
    use = SearchInSeus(ts_primary=2)
    searched = use.search_many_rfc(
        data=data, 
        delay_btwn_searches=delay_actions,
    )

    df_searched = pd.DataFrame(searched, columns=["RFC", "FILE_NAME", "NOMBRE"])
    id_unico = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = dir_to_save / f"{clave_extraccion}_{id_unico}_DYC.xlsx"
    df_searched.to_excel(file_path, index=False)

    return file_path, df_searched, id_unico