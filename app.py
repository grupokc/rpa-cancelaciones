# ---------------------- main ----------------------
import sys
# from services.utils import ensure_log_file 
from models import * 
from components.main_window import MainWindow
from PySide6.QtWidgets import QApplication

from config import settings


def main():
    ensure_log_file()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # print(settings.ui.points)
    vector = settings.ui.points.get("BUSCAR")
    print(vector.x, vector.y)
    main()
