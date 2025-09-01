from services.Extract import *
from services.Extract.hermes_use_consultador import HermesUseConsultador


def extract_rfc(
    df_base: pd.DataFrame, 
    column_name: str = 'RFC',
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
    use = HermesUseConsultador(delay_actions=1)
    searched = use.search_many_rfc(
        rfc_list=rfc_search,
        delay_btwn_searches=delay_actions
    )
    df_searched = pd.DataFrame(searched, columns=["RFC", "FILE_NAME"])
    id_unico = str(uuid.uuid4())[:5] # Generamos un id_unico 
    df_searched.to_excel(f"{clave_extraccion}_{id_unico}_DYC.xlsx")

