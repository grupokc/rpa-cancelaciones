from models import * 
from models.etl_result import ETLResult


# TODO: cambiar este modulo por el real del ciclo etl 
from services.run_backend_etl import run_backend_etl

class ETLWorker(QObject):
    finished = Signal(ETLResult)
    failed = Signal(str)
    canceled = Signal()
    progress = Signal(str)  # mensajes breves opcionales

    def __init__(self, input_path: Path):
        super().__init__()
        self.input_path = input_path
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            # Simula chequear cancelación de forma cooperativa
            for _ in range(5):
                if self._cancel:
                    self.canceled.emit()
                    return
                self.progress.emit("Procesando…")
                time.sleep(0.3)

            # Aquí llamas tu backend real
            result = run_backend_etl(self.input_path, cancel_flag=lambda: self._cancel)
            if result is None:  # cancelado desde backend
                self.canceled.emit()
                return
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))


