from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPixmap
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from frontend.ui.org_main_ui import Ui_MainWindow

def get_logo_path(rel_path):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    abs_path = os.path.join(base_dir, rel_path)
    return abs_path if os.path.exists(abs_path) else rel_path

joined_orgs = [
    {"id": 1, "name": "Tech Society", "logo_path": get_logo_path("frontend/assets/organization/sample_orgs/Sample Org 1.jpg"), "details": "View Details"},
    {"id": 2, "name": "Art Club", "logo_path": get_logo_path("frontend/assets/organization/sample_orgs/Sample Org 2.png"), "details": "View Details"},
    {"id": 3, "name": "Music Group", "logo_path": get_logo_path("frontend/assets/organization/sample_orgs/Sample Org 3.png"), "details": "View Details"},
    {"id": 4, "name": "Sports Team", "logo_path": get_logo_path("frontend/assets/organization/sample_orgs/Sample Org.png"), "details": "View Details"},
    {"id": 5, "name": "Literature Circle", "logo_path": get_logo_path("frontend/assets/organization/sample_orgs/CiSCo Logo.jpg"), "details": "View Details"},
    {"id": 6, "name": "Science Forum", "logo_path": "No Photo", "details": "More Details"},
    {"id": 7, "name": "Drama Society", "logo_path": "No Photo", "details": "More Details"},
    {"id": 8, "name": "Photography Club", "logo_path": "No Photo", "details": "More Details"},
]

college_orgs = [
    {"id": 1, "name": "Robotics Club", "logo_path": "No Photo", "description": "Build and program robots.", "details": "More Details", "apply": "Apply"},
    {"id": 2, "name": "Chess Club", "logo_path": "No Photo", "description": "Play and learn chess.", "details": "More Details", "apply": "Apply"},
    {"id": 3, "name": "Debate Team", "logo_path": "No Photo", "description": "Join debates and competitions.", "details": "More Details", "apply": "Apply"},
    {"id": 4, "name": "Eco Warriors", "logo_path": "No Photo", "description": "Environmental activities.", "details": "More Details", "apply": "Apply"},
    {"id": 5, "name": "Coding Club", "logo_path": "No Photo", "description": "Learn programming.", "details": "More Details", "apply": "Apply"},
    {"id": 6, "name": "Business Society", "logo_path": "No Photo", "description": "Entrepreneurship events.", "details": "More Details", "apply": "Apply"},
    {"id": 7, "name": "Film Makers", "logo_path": "No Photo", "description": "Create short films.", "details": "More Details", "apply": "Apply"},
    {"id": 8, "name": "Math Club", "logo_path": "No Photo", "description": "Math competitions.", "details": "More Details", "apply": "Apply"},
]

joined_branches = [
    {"id": 1, "name": "Tech Subgroup", "logo_path": "No Photo", "details": "View Details"},
    {"id": 2, "name": "Art Section", "logo_path": "No Photo", "details": "View Details"},
]
college_branches = [
    {"id": 1, "name": "Robotics Section", "logo_path": "No Photo", "description": "Robotics branch.", "details": "More Details", "apply": "Apply"},
    {"id": 2, "name": "Chess Section", "logo_path": "No Photo", "description": "Chess branch.", "details": "More Details", "apply": "Apply"},
]

class JoinedOrgCard(QtWidgets.QFrame):
    def __init__(self, logo_path, more_details):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.setMinimumSize(250, 275)

        self.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)

        logo_label = QtWidgets.QLabel()
        logo_label.setFixedSize(200, 200)
        logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        if logo_path != "No Photo":
            pixmap = QPixmap(logo_path).scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("No Logo")
        else:
            logo_label.setText("No Logo")

        btn_details = QtWidgets.QPushButton(more_details)
        btn_details.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        layout.addWidget(logo_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btn_details)

class CollegeOrgCard(QtWidgets.QFrame):
    def __init__(self, logo_path, description, more_details, apply):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.setMinimumSize(250, 275)

        self.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)

        logo_label = QtWidgets.QLabel()
        logo_label.setFixedSize(200, 200)
        logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        if logo_path != "No Photo":
            pixmap = QPixmap(logo_path).scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("No Logo")
        else:
            logo_label.setText("No Logo")

        desc_label = QtWidgets.QLabel()
        desc_label.setText(description)
        desc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        desc_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        desc_label.setWordWrap(True)

        btn_details = QtWidgets.QPushButton(more_details)
        btn_apply = QtWidgets.QPushButton(apply)
        btn_details.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        btn_apply.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        layout.addWidget(logo_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(desc_label)
        layout.addWidget(btn_details)
        layout.addWidget(btn_apply)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.joined_org_count = 0
        self.college_org_count = 0
        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_changed)

        self.load_orgs()

    def clear_grid(self, grid_layout):
        for i in reversed(range(grid_layout.count())):
            item = grid_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def load_orgs(self):
        self.clear_grid(self.ui.joined_org_grid)
        self.clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0
        for org in joined_orgs:
            self.add_joined_org(org)
        for org in college_orgs:
            self.add_college_org(org)

        self.ui.joined_org_scroll.adjustSize()
        self.ui.college_org_scroll.adjustSize()
        self.ui.joined_org_scroll.updateGeometry()
        self.ui.college_org_scroll.updateGeometry()
        self.update()

    def load_branches(self):
        self.clear_grid(self.ui.joined_org_grid)
        self.clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0
        for branch in joined_branches:
            self.add_joined_org(branch)
        for branch in college_branches:
            self.add_college_org(branch)

        self.ui.joined_org_scroll.adjustSize()
        self.ui.college_org_scroll.adjustSize()
        self.ui.joined_org_scroll.updateGeometry()
        self.ui.college_org_scroll.updateGeometry()
        self.update()

    def on_combobox_changed(self, index):
        if index == 0:
            self.load_orgs()
            self.ui.joined_label.setText("Joined Organization(s)")
            self.ui.college_label.setText("College Organization(s)")
        else:
            self.load_branches()
            self.ui.joined_label.setText("Joined Branch(es)")
            self.ui.college_label.setText("College Branch(es)")

        self.ui.joined_org_scrollable.verticalScrollBar().setValue(0)
        self.ui.college_org_scrollable.verticalScrollBar().setValue(0)

    def add_joined_org(self, joined_data):
        card = JoinedOrgCard(joined_data["logo_path"], joined_data["details"])
        col = self.joined_org_count % 5
        row = self.joined_org_count // 5
        self.ui.joined_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.joined_org_count += 1

        self.ui.joined_org_grid.setRowMinimumHeight(row, 300)

    def add_college_org(self, college_data):
        card = CollegeOrgCard(
            college_data["logo_path"],
            college_data["description"],
            college_data["details"],
            college_data["apply"]
        )
        col = self.college_org_count % 5
        row = self.college_org_count // 5
        self.ui.college_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.college_org_count += 1
        self.ui.college_org_grid.setRowMinimumHeight(row, 300)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())