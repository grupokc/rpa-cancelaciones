from components import * 
from config import settings
from components.command_tab import CommandTab
from components.log_tab import LogTab 
from models.etl_result import ETLResult
from models.etl_worker import ETLWorker

# ---------------------- Ventana principal ----------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(settings.APP_TITLE)
        self.resize(1000, 600)

        self.log_tab = LogTab()
        self.cmd_tab = CommandTab()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.log_tab, "Log")
        self.tabs.addTab(self.cmd_tab, "Centro de mando")
        self.setCentralWidget(self.tabs)

        # Barra de estado
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Menú y toolbar
        self._setup_menu()
        self._setup_toolbar()

        # Señales
        self.cmd_tab.start_requested.connect(self.on_start)
        self.cmd_tab.cancel_requested.connect(self.on_cancel)
        # La caja de búsqueda de cmd_tab filtra el log en vivo
        self.cmd_tab.search_input.textChanged.connect(self._forward_search_to_log)

        # Hilo/worker
        self.worker_thread: Optional[QThread] = None
        self.worker: Optional[ETLWorker] = None
        self.current_input: Optional[Path] = None

    # ---- UI scaffolding ----
    def _setup_menu(self):
        menubar = QMenuBar(self)
        file_menu = QMenu("Archivo", self)

        export_csv = QAction("Exportar log a CSV", self)
        export_csv.triggered.connect(self.on_export_log)

        reload_log = QAction("Recargar log", self)
        reload_log.triggered.connect(self.log_tab.reload)

        file_menu.addAction(export_csv)
        file_menu.addAction(reload_log)
        menubar.addMenu(file_menu)
        self.setMenuBar(menubar)

    def _setup_toolbar(self):
        tb = QToolBar("Acciones")
        self.addToolBar(tb)
        act_run = QAction("Ejecutar ETL", self)
        act_run.triggered.connect(lambda: self.cmd_tab._start())
        act_reload = QAction("Recargar log", self)
        act_reload.triggered.connect(self.log_tab.reload)
        tb.addAction(act_run)
        tb.addAction(act_reload)

    # ---- Acciones ----
    def _forward_search_to_log(self, text: str):
        self.tabs.setCurrentWidget(self.log_tab)
        self.log_tab.search_edit.setText(text)

    def on_export_log(self):
        dest, _ = QFileDialog.getSaveFileName(self, "Guardar log como…", "etl_log.csv", "CSV (*.csv)")
        if not dest:
            return
        try:
            # Simplemente copiamos el archivo actual (o reescribimos)
            ensure_log_file()
            Path(dest).write_text(settings.LOG_FILE.read_text(encoding="utf-8"), encoding="utf-8")
            self.status.showMessage("Log exportado", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el log:\n{e}")

    def on_start(self, input_path: Path):
        if self.worker_thread is not None:
            QMessageBox.information(self, "En progreso", "Ya hay un proceso en ejecución")
            return

        self.current_input = input_path
        self.worker_thread = QThread()
        self.worker = ETLWorker(input_path)
        self.worker.moveToThread(self.worker_thread)

        # Conexiones
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.failed.connect(self.on_worker_failed)
        self.worker.canceled.connect(self.on_worker_canceled)
        self.worker.progress.connect(lambda msg: self.status.showMessage(msg))
        # Limpieza
        self.worker.finished.connect(self._cleanup_worker)
        self.worker.failed.connect(self._cleanup_worker)
        self.worker.canceled.connect(self._cleanup_worker)

        self.cmd_tab.set_running(True)
        self.status.showMessage("Ejecutando ETL…")
        self.worker_thread.start()

    def on_cancel(self):
        if self.worker:
            self.worker.cancel()
            self.status.showMessage("Cancelando…")

    # ---- Callbacks worker ----
    def _cleanup_worker(self):
        self.cmd_tab.set_running(False)
        if self.worker_thread is not None:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
            self.worker = None

    def on_worker_finished(self, result: ETLResult):
        # Registrar en log
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        in_name = self.current_input.name if self.current_input else "—"
        out_name = result.output_path.name
        append_log_row([now, in_name, out_name, str(result.total_records)])

        self.log_tab.reload()
        self.status.showMessage("ETL finalizado")
        QMessageBox.information(self, "Listo", f"Proceso completado. Salida: {out_name}")

    def on_worker_failed(self, err: str):
        QMessageBox.critical(self, "Error", f"El proceso falló:\n{err}")
        self.status.showMessage("Error en ETL")

    def on_worker_canceled(self):
        self.status.showMessage("Proceso cancelado")
        QMessageBox.information(self, "Cancelado", "El proceso fue cancelado")

