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
        self.tabs.addTab(self.log_tab, "Registro de Ejecuciones")
        self.tabs.addTab(self.cmd_tab, "Centro de mando")
        self.setCentralWidget(self.tabs)

        # Barra de estado
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Menu
        self._setup_menu()

        # Señales
        self.cmd_tab.start_requested.connect(self.on_start)
        self.cmd_tab.cancel_requested.connect(self.on_cancel)
        # La caja de búsqueda de cmd_tab filtra el log en vivo
        self.cmd_tab.search_input.textChanged.connect(self._forward_search_to_log)

        # Hilo/worker
        self.worker_thread: Optional[QThread] = None
        self.worker: Optional[ETLWorker] = None
        self.current_input: Optional[Path] = None

    # ---- Menu superior  ----
    def _setup_menu(self):
        """
        Mapea el menu superior
        """
        # Instanciar una barra para el menu 
        menubar = QMenuBar(self)

        # ---- Menu Desplegable: Archivo ----
        file_menu = QMenu("Archivo", self)
        # Definimos Acciones en este menu: cada QAction se mapea como un boton
        export_csv = QAction("Exportar log a CSV", self) # Accion 1 asociada al menu desplegable de archivo. Se mapea tambien como boton
        export_csv.triggered.connect(self.on_export_log) # Coneccion de la accion del menu desplegable con alguna funcion 
        reload_log = QAction("Recargar log", self) # Accion 2
        reload_log.triggered.connect(self.log_tab.reload) # Coneccion entre la Accion 2 y alguna fncion interna de la clase 
        # Añadir cada accion al menu de archivo 
        file_menu.addAction(export_csv)
        file_menu.addAction(reload_log)
        # Añadir el menu de archivo a la barra de menu 
        menubar.addMenu(file_menu)

        # ---- Menu desplegable: Ejecutar CICLO ETL  ----
        ejecutar_menu = QMenu("Ejecutar", self)
        # Definimos un accion 
        act_run = QAction("Ejecutar ETL", self) # Accion 1 
        act_run.triggered.connect(lambda: self.cmd_tab._start())
        # Agregar dicha accion al menu desplegable 
        ejecutar_menu.addAction(act_run)
        # Añadir el menu de archivo a la barra de menu 
        menubar.addMenu(ejecutar_menu)

        # ---- Menu desplegable: Recargar Log   ----
        recargar_menu = QMenu("Log", self)
        # Definimos una accion en el menu 
        act_reload = QAction("Recargar log", self)
        act_reload.triggered.connect(self.log_tab.reload)
        # Agregar accion al menu desplegable asociado 
        recargar_menu.addAction(act_reload)
        # Añadir el menu de archivo a la barra de meu 
        menubar.addMenu(recargar_menu)


        # ---- Menu desplegable: Recargar Log   ----
        info_menu = QMenu("Info", self)
        # Definimos una accion en el menu 
        act_info = QAction("About", self)
        act_info.triggered.connect(self.show_app_info)
        # Agregar accion al menu desplegable asociado 
        info_menu.addAction(act_info)
        # Añadir el menu de archivo a la barra de meu 
        menubar.addMenu(info_menu)


        # ---- Version ---- 
        version_menu = QMenu(f"Version:     {settings.VERSION}", self)
        menubar.addMenu(version_menu) 

        # Setear el Menubar con el menubar compuesto por todos los elementos anteriores
        self.setMenuBar(menubar)

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


    def show_app_info(self): 
        """
        Pinta una tarjeta con la informacion del aplicativo 
        """
        QMessageBox.information(
            self, 
            "Sobre la aplicacion",
            f"""
            Nombre aplicacion: {settings.APP_TITLE}
            VERSION: {settings.VERSION}
            MODELO OCR: {settings.OCR_MODEL}


            Grupo KC.

            AUTOR: Mauricio Casarin
            """
        )


