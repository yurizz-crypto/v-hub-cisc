from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QAbstractTableModel, Qt
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from frontend.utils.orgs_custom_widgets.cards import JoinedOrgCard, EventCard, CollegeOrgCard, OfficerCard
from frontend.utils.orgs_custom_widgets.dialogs import OfficerDialog
from frontend.utils.orgs_custom_widgets.tables import ViewMembers

from frontend.ui.org_main_ui import Ui_MainWindow

def get_logo_path(rel_path):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    abs_path = os.path.join(base_dir, rel_path)
    return abs_path if os.path.exists(abs_path) else rel_path

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
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.joined_org_count = 0
        self.college_org_count = 0
        self.table = self.findChild(QtWidgets.QTableView, "list_view")
        self.current_org = None
    
        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.view_members_btn.clicked.connect(self.to_members_page)
        self.ui.back_btn_member.clicked.connect(self.return_to_prev_page)
        self.ui.back_btn.clicked.connect(self.return_to_prev_page)
        # Connect search button to search function
        self.ui.search_btn.clicked.connect(self.perform_search)

        self.ui.search_btn_3.clicked.connect(self.perform_member_search)
        self.no_member_label = QtWidgets.QLabel("No Record(s) Found", self.ui.list_container)
        self.no_member_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.no_member_label.setStyleSheet("font-size: 20px;")
        self.no_member_label.hide()

        self.load_orgs()

    def perform_member_search(self):
        """Handle member search button click and filter members based on search text."""
        search_text = self.ui.search_line_3.text().strip().lower()
        self.load_members(search_text)

    def perform_search(self):
        """Handle search button click and filter organizations/branches based on search text."""
        search_text = self.ui.search_line.text().strip().lower()
        current_index = self.ui.comboBox.currentIndex()
        if current_index == 0:
            self.load_orgs(search_text)
        else:
            self.load_branches(search_text)

    def clear_grid(self, grid_layout):
        for i in reversed(range(grid_layout.count())):
            item = grid_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def load_orgs(self, search_text=""):
        """Load organizations, filtered by search_text if provided."""
        self.clear_grid(self.ui.joined_org_grid)
        self.clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0
        
        filtered_joined_orgs = [
            org for org in joined_orgs
            if search_text in org["name"].lower() or search_text == ""
        ]
        filtered_college_orgs = [
            org for org in college_orgs
            if search_text in org["name"].lower() or search_text == ""
        ]
        
        for org in filtered_joined_orgs:
            self.add_joined_org(org)
        for org in filtered_college_orgs:
            self.add_college_org(org)

        if self.joined_org_count == 0:
            no_record_label = QtWidgets.QLabel("No Record(s) Found")
            no_record_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_record_label.setStyleSheet("font-size: 20px;")
            self.ui.joined_org_grid.addWidget(no_record_label, 0, 0, 1, 5)

        if self.college_org_count == 0:
            no_record_label = QtWidgets.QLabel("No Record(s) Found")
            no_record_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_record_label.setStyleSheet("font-size: 20px;")
            self.ui.college_org_grid.addWidget(no_record_label, 0, 0, 1, 5)

            self.ui.joined_org_scrollable.adjustSize()
            self.ui.college_org_scrollable.adjustSize()
            self.ui.joined_org_scrollable.updateGeometry()
            self.ui.college_org_scrollable.updateGeometry()
            self.update()

    def load_branches(self, search_text=""):
        """Load branches, filtered by search_text if provided."""
        self.clear_grid(self.ui.joined_org_grid)
        self.clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0
        
        filtered_joined_branches = [
            branch for branch in joined_branches
            if search_text in branch["name"].lower() or search_text == ""
        ]
        filtered_college_branches = [
            branch for branch in college_branches
            if search_text in branch["name"].lower() or search_text == ""
        ]
        
        for branch in filtered_joined_branches:
            self.add_joined_org(branch)
        for branch in filtered_college_branches:
            self.add_college_org(branch)

        if self.joined_org_count == 0:
            no_record_label = QtWidgets.QLabel("No Record(s) Found")
            no_record_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_record_label.setStyleSheet("font-size: 20px;")
            self.ui.joined_org_grid.addWidget(no_record_label, 0, 0, 1, 5)

        if self.college_org_count == 0:
            no_record_label = QtWidgets.QLabel("No Record(s) Found")
            no_record_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_record_label.setStyleSheet("font-size: 20px;")
            self.ui.college_org_grid.addWidget(no_record_label, 0, 0, 1, 5)

        self.ui.joined_org_scrollable.adjustSize()
        self.ui.college_org_scrollable.adjustSize()
        self.ui.joined_org_scrollable.updateGeometry()
        self.ui.college_org_scrollable.updateGeometry()
        self.update()

    def load_members(self, search_text=""):
        """Load and filter members into the table, show 'No Record(s) Found' if empty."""
        if self.current_org:
            members_data = self.current_org.get("members", [])
            filtered_members = [
                member for member in members_data
                if any(search_text in str(field).lower() for field in member)
            ] if search_text else members_data

        model = ViewMembers(filtered_members)
        self.ui.list_view.setModel(model)
        self.ui.list_view.horizontalHeader().setStretchLastSection(True)
        self.ui.list_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        if model.rowCount() == 0:
            self.ui.list_view.hide()
            self.no_member_label.show()
        else:
            self.ui.list_view.show()
            self.no_member_label.hide()

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
        self.current_org = org_data

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

    def to_members_page(self):
        self.load_members()
        self.ui.stacked_widget.setCurrentIndex(2)

    def return_to_prev_page(self):
        current_index = self.ui.comboBox.currentIndex()
        if current_index == 0:
            self.load_orgs()
        else:
            self.load_branches()
        if self.ui.stacked_widget.currentIndex() == 2:
            self.ui.stacked_widget.setCurrentIndex(1)
        else:
            self.ui.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())