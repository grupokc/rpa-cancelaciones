from services.Extract import *
from services.Extract.search_in_seus import SearchInSeus

# Directorio para guardar las prebases 
SEARCHED_DIR = settings.BD_GENERADORAS_DIR

def extract_rfc(
    df_base: pd.DataFrame, 
    column_name: str = 'RFC',
    dir_to_save: Path = SEARCHED_DIR, 
    registros_por_recorrido: int = 300, 
    delay_actions: int = 1, 
    clave_extraccion: str = "Testing"
    ):
    """
    Busca usando las herramientas de Hermes.Extract los rfc que se proporcionen en el dataframe entrante. 

    Args. 
        df_base (pd.DataFrame): dataframe inicial para el ciclo ETL. 
        column_name (str): 
        registros_por_recorrido (int): 
        delay_actions (int)
        clave_extraccion (str)
    
    """
    if not column_name in df_base.columns.to_list(): 
        msg = f"El archivo no contiene la columna necesaria: {column_name}"
        raise ValueError(msg)
    
    rfc_search = df_base['RFC'].drop_duplicates()
    rfc_search = rfc_search[:registros_por_recorrido].tolist()
    rfc_to_search = []
    for rfc in rfc_search: 
        rfc = str(rfc)
        if len(rfc) > 10 : 
            rfc_to_search.append(rfc[:10])
        if len(rfc) == 10 : 
            rfc_to_search.append(rfc)
        else: 
            continue
    use = SearchInSeus(ts_primary=2) # AQUI PODEMOS CAMBIARLO 
    searched = use.search_many_rfc(
        rfc_list=rfc_search,
        delay_btwn_searches=delay_actions
    )
    df_searched = pd.DataFrame(searched, columns=["RFC", "FILE_NAME"])
    id_unico = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = dir_to_save / f"{clave_extraccion}_{id_unico}_DYC.xlsx"
    df_searched.to_excel(file_path, index=False)

    return file_path, df_searched