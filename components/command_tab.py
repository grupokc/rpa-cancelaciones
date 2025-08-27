from components import * 

# ---------------------- UI: Pestaña Centro de Mando ----------------------

class CommandTab(QWidget):
    input_selected = Signal(Path)
    start_requested = Signal(Path)
    cancel_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.selected_file: Optional[Path] = None

        self.file_label = QLabel("Archivo de entrada: —")
        self.btn_select = QPushButton("Seleccionar .xlsx…")
        self.btn_start = QPushButton("Ejecutar ETL")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setEnabled(False)

        self.search_label = QLabel("Buscar (en log):")
        self.search_input = QLineEdit()

        self.btn_select.clicked.connect(self._pick_file)
        self.btn_start.clicked.connect(self._start)
        self.btn_cancel.clicked.connect(self.cancel_requested.emit)

        top = QVBoxLayout()
        top.addWidget(self.file_label)

        row = QHBoxLayout()
        row.addWidget(self.btn_select)
        row.addWidget(self.btn_start)
        row.addWidget(self.btn_cancel)
        top.addLayout(row)

        srch = QHBoxLayout()
        srch.addWidget(self.search_label)
        srch.addWidget(self.search_input)
        top.addLayout(srch)

        self.setLayout(top)

    def _pick_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecciona archivo de entrada",
            "",
            "Excel (*.xlsx)",
        )
        if path:
            p = Path(path)
            if p.suffix.lower() != ".xlsx":
                QMessageBox.warning(self, "Formato inválido", "Selecciona un archivo .xlsx")
                return
            self.selected_file = p
            self.file_label.setText(f"Archivo de entrada: {p.name}")
            self.input_selected.emit(p)

    def _start(self):
        if not self.selected_file:
            QMessageBox.information(self, "Falta archivo", "Selecciona primero un archivo .xlsx")
            return
        self.start_requested.emit(self.selected_file)

    # Helpers visuales
    def set_running(self, running: bool):
        self.btn_select.setEnabled(not running)
        self.btn_start.setEnabled(not running)
        self.btn_cancel.setEnabled(running)

