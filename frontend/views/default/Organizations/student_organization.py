from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import os
import json
from typing import Dict, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from frontend.utils.orgs_custom_widgets.cards import JoinedOrgCard, EventCard, CollegeOrgCard, OfficerCard
from frontend.utils.orgs_custom_widgets.dialogs import OfficerDialog
from frontend.utils.orgs_custom_widgets.tables import ViewMembers
from frontend.ui.org_main_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.joined_org_count: int = 0
        self.college_org_count: int = 0
        self.officer_count: int = 0
        self.current_org: Optional[Dict] = None
        self.table = self.findChild(QtWidgets.QTableView, "list_view")
        
        self._setup_connections()
        self._setup_no_member_label()
        self.load_orgs()

    def _setup_connections(self) -> None:
        """Set up signal-slot connections."""
        self.ui.comboBox.currentIndexChanged.connect(self._on_combobox_changed)
        self.ui.view_members_btn.clicked.connect(self._to_members_page)
        self.ui.back_btn_member.clicked.connect(self._return_to_prev_page)
        self.ui.back_btn.clicked.connect(self._return_to_prev_page)
        self.ui.search_btn.clicked.connect(self._perform_search)
        self.ui.search_btn_3.clicked.connect(self._perform_member_search)
        self.ui.officer_history_dp.currentIndexChanged.connect(self._on_officer_history_changed)

    def _setup_no_member_label(self) -> None:
        """Initialize the 'No Record(s) Found' label for members."""
        self.no_member_label = QtWidgets.QLabel("No Record(s) Found", self.ui.list_container)
        self.no_member_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.no_member_label.setStyleSheet("font-size: 20px;")
        self.no_member_label.hide()

    @staticmethod
    def _get_logo_path(rel_path: str) -> str:
        """Resolve absolute logo path, return relative path if file doesn't exist."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        abs_path = os.path.join(base_dir, rel_path)
        return abs_path if os.path.exists(abs_path) else rel_path

    @staticmethod
    def _load_data() -> tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
        """Load organization and branch data from JSON file."""
        json_path = os.path.join(os.path.dirname(__file__), 'organizations_data.json')
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                return (
                    data.get('joined_orgs', []),
                    data.get('college_orgs', []),
                    data.get('joined_branches', []),
                    data.get('college_branches', [])
                )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {json_path}: {str(e)}")
            return [], [], [], []

    def _clear_grid(self, grid_layout: QtWidgets.QGridLayout) -> None:
        """Remove all widgets from the given grid layout."""
        for i in reversed(range(grid_layout.count())):
            if widget := grid_layout.itemAt(i).widget():
                widget.setParent(None)

    def _add_no_record_label(self, grid_layout: QtWidgets.QGridLayout) -> None:
        """Add 'No Record(s) Found' label to the grid layout."""
        no_record_label = QtWidgets.QLabel("No Record(s) Found")
        no_record_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        no_record_label.setStyleSheet("font-size: 20px;")
        grid_layout.addWidget(no_record_label, 0, 0, 1, 5)

    def _update_scroll_areas(self) -> None:
        """Update scroll areas and geometry."""
        self.ui.joined_org_scrollable.adjustSize()
        self.ui.college_org_scrollable.adjustSize()
        self.ui.joined_org_scrollable.updateGeometry()
        self.ui.college_org_scrollable.updateGeometry()
        self.update()

    def _perform_search(self) -> None:
        """Handle organization/branch search based on combo box selection."""
        search_text = self.ui.search_line.text().strip().lower()
        self.load_orgs(search_text) if self.ui.comboBox.currentIndex() == 0 else self.load_branches(search_text)

    def _perform_member_search(self) -> None:
        """Handle member search based on input text."""
        search_text = self.ui.search_line_3.text().strip().lower()
        self.load_members(search_text)

    def load_orgs(self, search_text: str = "") -> None:
        """Load and display organizations, filtered by search text."""
        joined_orgs, college_orgs, _, _ = self._load_data()
        self._clear_grid(self.ui.joined_org_grid)
        self._clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0

        filtered_joined = [org for org in joined_orgs if search_text in org["name"].lower() or not search_text]
        filtered_college = [org for org in college_orgs if search_text in org["name"].lower() or not search_text]

        for org in filtered_joined:
            self._add_joined_org(org)
        for org in filtered_college:
            self._add_college_org(org)

        if self.joined_org_count == 0:
            self._add_no_record_label(self.ui.joined_org_grid)
        if self.college_org_count == 0:
            self._add_no_record_label(self.ui.college_org_grid)

        self._update_scroll_areas()

    def load_branches(self, search_text: str = "") -> None:
        """Load and display branches, filtered by search text."""
        _, _, joined_branches, college_branches = self._load_data()
        self._clear_grid(self.ui.joined_org_grid)
        self._clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0

        filtered_joined = [branch for branch in joined_branches if search_text in branch["name"].lower() or not search_text]
        filtered_college = [branch for branch in college_branches if search_text in branch["name"].lower() or not search_text]

        for branch in filtered_joined:
            self._add_joined_org(branch)
        for branch in filtered_college:
            self._add_college_org(branch)

        if self.joined_org_count == 0:
            self._add_no_record_label(self.ui.joined_org_grid)
        if self.college_org_count == 0:
            self._add_no_record_label(self.ui.college_org_grid)

        self._update_scroll_areas()

    def load_members(self, search_text: str = "") -> None:
        """Load and filter members into the table view."""
        if not self.current_org:
            return

        members_data = self.current_org.get("members", [])
        filtered_members = [
            member for member in members_data
            if any(search_text in str(field).lower() for field in member)
        ] if search_text else members_data

        model = ViewMembers(filtered_members)
        self.ui.list_view.setModel(model)
        self.ui.list_view.horizontalHeader().setStretchLastSection(True)
        self.ui.list_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.ui.list_view.setVisible(bool(filtered_members))
        self.no_member_label.setVisible(not filtered_members)

    def _on_combobox_changed(self, index: int) -> None:
        """Handle combo box change to switch between organizations and branches."""
        self.ui.joined_label.setText("Joined Organization(s)" if index == 0 else "Joined Branch(es)")
        self.ui.college_label.setText("College Organization(s)" if index == 0 else "College Branch(es)")
        self.load_orgs() if index == 0 else self.load_branches()
        self.ui.joined_org_scrollable.verticalScrollBar().setValue(0)
        self.ui.college_org_scrollable.verticalScrollBar().setValue(0)

    def _add_joined_org(self, org_data: Dict) -> None:
        """Add a joined organization card to the grid."""
        card = JoinedOrgCard(self._get_logo_path(org_data["logo_path"]), org_data["details"], org_data, self)
        col = self.joined_org_count % 5
        row = self.joined_org_count // 5
        self.ui.joined_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.joined_org_count += 1
        self.ui.joined_org_grid.setRowMinimumHeight(row, 300)

    def _add_college_org(self, org_data: Dict) -> None:
        """Add a college organization card to the grid."""
        card = CollegeOrgCard(
            self._get_logo_path(org_data["logo_path"]), org_data["description"],
            org_data["details"], org_data["apply"], org_data, self
        )
        col = self.college_org_count % 5
        row = self.college_org_count // 5
        self.ui.college_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.college_org_count += 1
        self.ui.college_org_grid.setRowMinimumHeight(row, 300)

    def set_circular_logo(self, logo_label: QtWidgets.QLabel, logo_path: str, size: int = 200, border_width: int = 4) -> None:
        """Set a circular logo with a border on the given label."""
        logo_label.setFixedSize(size, size)
        if logo_path == "No Photo" or not QtGui.QPixmap(logo_path).isNull():
            logo_label.setText("No Logo")
            return

        pixmap = QtGui.QPixmap(logo_path).scaled(size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        centered_pixmap = QtGui.QPixmap(size, size).fill(QtCore.Qt.GlobalColor.transparent)
        
        with QtGui.QPainter(centered_pixmap) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            x = (size - pixmap.width()) // 2
            y = (size - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)

        mask = QtGui.QPixmap(size, size).fill(QtCore.Qt.GlobalColor.transparent)
        with QtGui.QPainter(mask) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            path = QtGui.QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.fillPath(path, QtCore.Qt.GlobalColor.white)

        centered_pixmap.setMask(mask.createMaskFromColor(QtCore.Qt.GlobalColor.white, QtCore.Qt.MaskMode.MaskOutColor))

        final_pixmap = QtGui.QPixmap(size, size).fill(QtCore.Qt.GlobalColor.transparent)
        with QtGui.QPainter(final_pixmap) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            painter.setBrush(QtGui.QBrush(centered_pixmap))
            painter.setPen(QtGui.QPen(QtGui.QColor(8, 73, 36), border_width))
            painter.drawEllipse(border_width // 2, border_width // 2, size - border_width, size - border_width)

        logo_label.setPixmap(final_pixmap)

    def _on_officer_history_changed(self, index: int) -> None:
        """Handle officer history combobox change to display officers for selected semester."""
        if not self.current_org:
            return
        selected_semester = self.ui.officer_history_dp.itemText(index)
        officers = self.current_org.get("officer_history", {}).get(selected_semester, [])
        self.load_officers(officers)

    def load_officers(self, officers: List[Dict]) -> None:
        """Load officer cards into the officer grid."""
        self._clear_grid(self.ui.officer_cards_grid)
        self.officer_count = 0
        self.ui.officers_scroll_area.verticalScrollBar().setValue(0)

        if not officers:
            self._add_no_record_label(self.ui.officer_cards_grid)
            return

        for officer in officers:
            card = OfficerCard(officer, self)
            col = self.officer_count % 3
            row = self.officer_count // 3
            self.ui.officer_cards_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
            self.officer_count += 1
            self.ui.officer_cards_grid.setRowMinimumHeight(row, 400)

    def show_officer_dialog(self, officer_data: Dict) -> None:
        """Display officer details in a dialog."""
        OfficerDialog(officer_data, self).exec()

    def load_events(self, events: List[Dict]) -> None:
        """Load event cards into the events layout."""
        while self.ui.verticalLayout_14.count():
            if item := self.ui.verticalLayout_14.takeAt(0).widget():
                item.deleteLater()

        for event in events:
            self.ui.verticalLayout_14.addWidget(EventCard(event, self))

        self.ui.verticalLayout_14.addStretch()
        self.ui.scroll_area_events.verticalScrollBar().setValue(0)

    def show_org_details(self, org_data: Dict) -> None:
        """Display organization details on the details page."""
        self.current_org = org_data
        self.ui.header_label_2.setText("Organization")
        self.ui.status_btn.setText("Active")
        self.ui.org_name.setText(org_data["name"])
        self.ui.org_type.setText("Organization Type")
        self.ui.brief_label.setText(org_data.get("brief", "No brief available"))
        self.ui.obj_label.setText(org_data.get("objectives", "No objectives available"))
        self.ui.obj_label_2.setText("\n".join(org_data.get("branches", [])) or "No branches available")
        self.set_circular_logo(self.ui.logo, org_data["logo_path"])
        
        self.ui.officer_history_dp.clear()
        semesters = org_data.get("officer_history", {}).keys()
        self.ui.officer_history_dp.addItem("Current Officers")
        self.ui.officer_history_dp.addItems(sorted(semesters))
        
        self.load_officers(org_data.get("officers", []))
        self.load_events(org_data.get("events", []))
        self.ui.label.setText("A.Y. 2025-2026 - 1st Semester")
        self.ui.stacked_widget.setCurrentIndex(1)

    def _to_members_page(self) -> None:
        """Navigate to the members page."""
        self.load_members()
        self.ui.stacked_widget.setCurrentIndex(2)

    def _return_to_prev_page(self) -> None:
        """Navigate back to the previous page."""
        if self.ui.stacked_widget.currentIndex() == 2:
            self.ui.stacked_widget.setCurrentIndex(1)
        else:
            self.load_orgs() if self.ui.comboBox.currentIndex() == 0 else self.load_branches()
            self.ui.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())