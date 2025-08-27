from components import * 
from config import settings
from models.log_table import LogTableModel


# ---------------------- UI: Pestaña Log ----------------------

class LogTab(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.table_model = LogTableModel(read_log_rows(), settings.LOG_HEADERS, self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.table_model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)  # filtra en todas las columnas

        self.table_view = QTableView(self)
        self.table_view.setModel(self.proxy)
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #000000; /* Azul corporativo como fondo principal */
                gridline-color: #333333; /* Líneas de cuadrícula oscuras y marcadas */
                border: 2px solid #003d5b; /* Borde más grueso y oscuro para énfasis */
                border-radius: 4px; /* Bordes redondeados para modernidad */
                font-family: 'Segoe UI', 'Arial', sans-serif; /* Fuente profesional */
                font-size: 13px; /* Tamaño legible */
                font-weight: 700; /* Fuente en negrita */
            }

            QTableView::item {
                padding: 4px; /* Espaciado interno */
                border: 1px solid #333333; /* Bordes de celdas más marcados */
            }
            QTableView::item:selected {
                background-color: #0078d4; /* Azul claro para selección */
                color: #ffffff; /* Texto blanco en selección */
                border: 1px solid #004b73; /* Borde de selección más oscuro */
            }

            QTableView::item:hover {
                background-color: #e6f0fa; /* Fondo claro al pasar el ratón */
                color: #000000; /* Texto negro en hover para legibilidad */
            }

            QHeaderView::section {
                background-color: #003d5b; /* Azul oscuro para encabezados */
                color: #ffffff; /* Texto blanco para contraste */
                padding: 6px; /* Espaciado interno */
                border: 2px solid #333333; /* Bordes más marcados */
                font-weight: 700; /* Fuente en negrita para encabezados */
                font-size: 13px; /* Tamaño consistente */
            }

            QTableView::item:focus {
                border: 2px solid #0078d4; /* Borde azul más grueso para celdas enfocadas */
            }   
    """)


        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Buscar en log…")
        self.search_edit.textChanged.connect(self.proxy.setFilterFixedString)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Log de ejecuciones"))
        layout.addWidget(self.search_edit)
        layout.addWidget(self.table_view)

    def reload(self):
        self.table_model.refresh(read_log_rows())
        # Mantener filtro actual
        self.proxy.invalidateFilter()

