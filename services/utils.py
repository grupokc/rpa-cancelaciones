from config import settings 
import csv 

# ---------------------- Utilidades de Log ----------------------

def ensure_log_file() -> None:
    """ 
    Asegura la existencia del archivo de log
    """
    if not settings.LOG_FILE.exists():
        with settings.LOG_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(settings.LOG_HEADERS)


def append_log_row(row: list[str]) -> None:
    """ 
    Agrega una nueva fila al registro del log. 

    Args. 
        row (list(str)). Nueva fila con el log del ciclo etl reciente. 
    """
    ensure_log_file()
    with settings.LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def read_log_rows() -> list[list[str]]:
    """
    Lee el archivo del log. 

    Returns. 
        list[list[str]]. Cada elemento de la lista exterior es una fila del log, cada elemento de la lista interior es un registro del log.
    """
    ensure_log_file()
    with settings.LOG_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if rows and rows[0] == settings.LOG_HEADERS:
        return rows[1:]
    return rows


# ---------------------- Utilidades de Generales ----------------------

import datetime as dt 

def get_date() -> str: 
    "Devuelve una cadena de la fecha"
    return dt.datetime.now().strftime("%y%m%d%H%M%S")

