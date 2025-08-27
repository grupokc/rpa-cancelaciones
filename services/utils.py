from config import settings 
import csv 

# ---------------------- Utilidades de Log ----------------------

def ensure_log_file() -> None:
    if not settings.LOG_FILE.exists():
        with settings.LOG_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(settings.LOG_HEADERS)


def append_log_row(row: list[str]) -> None:
    ensure_log_file()
    with settings.LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def read_log_rows() -> list[list[str]]:
    ensure_log_file()
    with settings.LOG_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if rows and rows[0] == settings.LOG_HEADERS:
        return rows[1:]
    return rows
