from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPixmap
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from frontend.ui.org_main_ui import Ui_MainWindow

def get_logo_path(rel_path):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    abs_path = os.path.join(base_dir, rel_path)
    return abs_path if os.path.exists(abs_path) else rel_path

# Load data from JSON file
json_path = os.path.join(os.path.dirname(__file__), 'organizations_data.json')
try:
    with open(json_path, 'r') as file:
        data = json.load(file)
        joined_orgs = data.get('joined_orgs', [])
        college_orgs = data.get('college_orgs', [])
        joined_branches = data.get('joined_branches', [])
        college_branches = data.get('college_branches', [])
except FileNotFoundError:
    print(f"Error: {json_path} not found.")
    joined_orgs = []
    college_orgs = []
    joined_branches = []
    college_branches = []
except json.JSONDecodeError:
    print(f"Error: {json_path} contains invalid JSON.")
    joined_orgs = []
    college_orgs = []
    joined_branches = []
    college_branches = []

class JoinedOrgCard(QtWidgets.QFrame):
    def __init__(self, logo_path, more_details, org_data, main_window):
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
        btn_details.clicked.connect(lambda: main_window.show_org_details(org_data))

        layout.addWidget(logo_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btn_details)

class CollegeOrgCard(QtWidgets.QFrame):
    def __init__(self, logo_path, description, more_details, apply, org_data, main_window):
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
        btn_details.clicked.connect(lambda: main_window.show_org_details(org_data))

        layout.addWidget(logo_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(desc_label)
        layout.addWidget(btn_details)
        layout.addWidget(btn_apply)

class OfficerCard(QtWidgets.QFrame):
    def __init__(self, officer_data, main_window):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.setMinimumSize(250, 350)

        self.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Top spacer to center content vertically
        top_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        layout.addItem(top_spacer)

        image_label = QtWidgets.QLabel()
        image_label.setFixedSize(200, 250)
        image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        if "card_image_path" in officer_data and officer_data["card_image_path"] != "No Photo":
            pixmap = QPixmap(officer_data["card_image_path"]).scaled(200, 250, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap)
            else:
                image_label.setText("No Image")
        else:
            image_label.setText("No Image")

        name_label = QtWidgets.QLabel(officer_data.get("name", "Unknown"))
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        position_label = QtWidgets.QLabel(officer_data.get("position", "Unknown Position"))
        position_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        btn_details = QtWidgets.QPushButton("Officer Details")
        btn_details.setStyleSheet("background-color: #FFD700; color: black; border-radius: 5px;")
        btn_details.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        btn_details.clicked.connect(lambda: main_window.show_officer_dialog(officer_data))

        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(position_label)
        layout.addWidget(btn_details)

        # Bottom spacer to maintain vertical centering
        bottom_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        layout.addItem(bottom_spacer)

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

class EventCard(QtWidgets.QFrame):
    def __init__(self, event_data, main_window):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(100)  # Adjusted height to fit the design
        self.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
            }
            QFrame#eventHeader {
                background-color: #084924;
                color: #fff;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 5px;
            }
        """)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header = QtWidgets.QFrame(self)
        header.setObjectName("eventHeader")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        name_label = QtWidgets.QLabel(event_data.get("name", "Unknown Event"))
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        date_label = QtWidgets.QLabel(event_data.get("date", "No Date"))
        date_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        header_layout.addWidget(name_label)
        header_layout.addWidget(date_label)
        main_layout.addWidget(header)

        # Content section
        content_label = QtWidgets.QLabel(event_data.get("description", "No Description"))
        content_label.setStyleSheet("padding: 10px; font-size: 12px;")
        content_label.setWordWrap(True)
        content_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(content_label)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.joined_org_count = 0
        self.college_org_count = 0
        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_changed)

        self.ui.back_btn.clicked.connect(self.return_to_prev_page)
        self.setup_scroll_area()

        self.load_orgs()

    def setup_scroll_area(self):
        self.ui.joined_org_scrollable.setStyleSheet("""
            QScrollArea {
                background-color: white;
            }
        """)

        self.ui.college_org_scrollable.setStyleSheet("""
            QScrollArea {
                background-color: white;
            }
        """)

        self.ui.officers_scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
            }
        """)



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
        for org in joined_orgs or []:
            self.add_joined_org(org)
        for org in college_orgs or []:
            self.add_college_org(org)

        self.ui.joined_org_scrollable.adjustSize()
        self.ui.college_org_scrollable.adjustSize()
        self.ui.joined_org_scrollable.updateGeometry()
        self.ui.college_org_scrollable.updateGeometry()
        self.update()

    def load_branches(self):
        self.clear_grid(self.ui.joined_org_grid)
        self.clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0
        for branch in joined_branches or []:
            self.add_joined_org(branch)
        for branch in college_branches or []:
            self.add_college_org(branch)

        self.ui.joined_org_scrollable.adjustSize()
        self.ui.college_org_scrollable.adjustSize()
        self.ui.joined_org_scrollable.updateGeometry()
        self.ui.college_org_scrollable.updateGeometry()
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
        card = JoinedOrgCard(get_logo_path(joined_data["logo_path"]), joined_data["details"], joined_data, self)
        col = self.joined_org_count % 5
        row = self.joined_org_count // 5
        self.ui.joined_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.joined_org_count += 1
        self.ui.joined_org_grid.setRowMinimumHeight(row, 300)

    def add_college_org(self, college_data):
        card = CollegeOrgCard(
            get_logo_path(college_data["logo_path"]),
            college_data["description"],
            college_data["details"],
            college_data["apply"],
            college_data,
            self
        )
        col = self.college_org_count % 5
        row = self.college_org_count // 5
        self.ui.college_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.college_org_count += 1
        self.ui.college_org_grid.setRowMinimumHeight(row, 300)

    def set_circular_logo(self, logo_label, logo_path, size=200, border_width=4):
        logo_label.setFixedSize(size, size)
        if logo_path != "No Photo":
            pixmap = QtGui.QPixmap(logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                centered_pixmap = QtGui.QPixmap(size, size)
                centered_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
                painter = QtGui.QPainter(centered_pixmap)
                painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                x = (size - scaled_pixmap.width()) // 2
                y = (size - scaled_pixmap.height()) // 2
                painter.drawPixmap(x, y, scaled_pixmap)
                painter.end()

                mask = QtGui.QPixmap(size, size)
                mask.fill(QtCore.Qt.GlobalColor.transparent)
                painter = QtGui.QPainter(mask)
                painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                path = QtGui.QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.fillPath(path, QtCore.Qt.GlobalColor.white)
                painter.end()
                centered_pixmap.setMask(mask.createMaskFromColor(QtCore.Qt.GlobalColor.white, QtCore.Qt.MaskMode.MaskOutColor))

                final_pixmap = QtGui.QPixmap(size, size)
                final_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
                painter = QtGui.QPainter(final_pixmap)
                painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                painter.setBrush(QtGui.QBrush(centered_pixmap))
                painter.setPen(QtGui.QPen(QtGui.QColor(8, 73, 36), border_width))
                painter.drawEllipse(border_width//2, border_width//2, size - border_width, size - border_width)
                painter.end()

                logo_label.setPixmap(final_pixmap)
            else:
                logo_label.setText("No Logo")
        else:
            logo_label.setText("No Logo")

    def load_officers(self, officers):
        self.clear_grid(self.ui.officer_cards_grid)
        self.officer_count = 0

        self.ui.officers_scroll_area.verticalScrollBar().setValue(0)

        for officer in officers:
            card = OfficerCard(officer, self)
            col = self.officer_count % 3
            row = self.officer_count // 3
            self.ui.officer_cards_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
            self.officer_count += 1
            self.ui.officer_cards_grid.setRowMinimumHeight(row, 400)

    def show_officer_dialog(self, officer_data):
        dialog = OfficerDialog(officer_data, self)
        dialog.exec()

    def load_events(self, events):
        while self.ui.verticalLayout_14.count():
            item = self.ui.verticalLayout_14.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for event in events:
            card = EventCard(event, self)
            self.ui.verticalLayout_14.addWidget(card)

        self.ui.verticalLayout_14.addStretch()
        self.ui.scroll_area_events.verticalScrollBar().setValue(0)

    def show_org_details(self, org_data):
            self.ui.header_label_2.setText("Organization")
            self.ui.status_btn.setText("Active")
            self.ui.org_name.setText(org_data["name"])
            self.ui.org_type.setText("Organization Type")
            self.ui.brief_label.setText(org_data.get("brief", "No brief available"))
            self.ui.obj_label.setText(org_data.get("objectives", "No objectives available"))
            branches_text = "\n".join(org_data.get("branches", []))
            self.ui.obj_label_2.setText(branches_text or "No branches available")

            self.set_circular_logo(self.ui.logo, org_data["logo_path"])

            self.load_officers(org_data.get("officers", []))
            self.load_events(org_data.get("events", []))

            self.ui.label.setText("A.Y. 2025-2026 - 1st Semester")

            self.ui.stacked_widget.setCurrentIndex(1)

    def return_to_prev_page(self):
        self.load_orgs()
        self.ui.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())