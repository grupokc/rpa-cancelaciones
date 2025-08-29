from components import * 



class LogTableModel(QAbstractTableModel):
    """
    Modelo para el log de la tabla del ciclo ETL 
    """

    def __init__(self, data: list[list[str]], headers: list[str], parent: Optional[QObject] = None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    # Métodos requeridos
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]
        return section + 1

    # Helpers
    def refresh(self, data: list[list[str]]):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

