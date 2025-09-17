from PyQt6.QtCore import QAbstractTableModel, Qt

class ViewMembers(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Name", "Position", "Status", "Join Date"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None