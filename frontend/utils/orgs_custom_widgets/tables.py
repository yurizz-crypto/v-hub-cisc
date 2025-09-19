from PyQt6.QtCore import QAbstractTableModel, Qt

class ViewMembers(QAbstractTableModel):
    def __init__(self, data, is_managing: bool = False):
        super().__init__()
        self._data = data
        self.is_managing = is_managing
        self._headers = ["No.", "Name", "Position", "Status", "Join Date"] + (["Actions"] if is_managing else [])

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            col = index.column()
            if col == 0:
                return str(index.row() + 1)
            elif col < len(self._headers) - 1 or not self.is_managing:
                return self._data[index.row()][col - 1]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None
    
    def flags(self, index, parent=None):
        flags = super().flags(index)
        if self.is_managing and index.column() == len(self._headers) - 1:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags