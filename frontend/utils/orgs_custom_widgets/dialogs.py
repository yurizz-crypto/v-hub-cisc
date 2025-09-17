from PyQt6 import QtWidgets, QtCore, QtGui

class OfficerDialog(QtWidgets.QDialog):
    def __init__(self, officer_data, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.setFixedSize(400, 300)  # Adjust size as needed

        main_layout = QtWidgets.QVBoxLayout(self)

        # Top layout for close button
        top_layout = QtWidgets.QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        top_layout.addItem(spacer)
        close_btn = QtWidgets.QPushButton("X")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("background-color: transparent; border: none; color: gray;")
        close_btn.clicked.connect(self.close)
        top_layout.addWidget(close_btn)
        main_layout.addLayout(top_layout)

        # Horizontal layout for photo and info
        hlayout = QtWidgets.QHBoxLayout()
        photo_label = QtWidgets.QLabel()
        parent.set_circular_logo(photo_label, officer_data.get("photo_path", "No Photo"), size=150, border_width=4)
        hlayout.addWidget(photo_label)

        vinfo = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel(officer_data.get("name", "Unknown"))
        name_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold))
        position_label = QtWidgets.QLabel(officer_data.get("position", "Unknown Position"))
        date_label = QtWidgets.QLabel(f"{officer_data.get('start_date', '07/08/2025')} - Present")
        vinfo.addWidget(name_label)
        vinfo.addWidget(position_label)
        vinfo.addWidget(date_label)
        hlayout.addLayout(vinfo)

        main_layout.addLayout(hlayout)

        # Buttons
        cv_btn = QtWidgets.QPushButton("Curriculum Vitae")
        cv_btn.setStyleSheet("background-color: #084924; color: white; border-radius: 5px;")
        contact_btn = QtWidgets.QPushButton("Contact Me")
        contact_btn.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px;")
        main_layout.addWidget(cv_btn)
        main_layout.addWidget(contact_btn)
