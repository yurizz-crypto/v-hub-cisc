from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QStyledItemDelegate, QHBoxLayout, QPushButton, QMessageBox, QFileDialog
import sys
import os
import json
import shutil
from typing import Dict, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from frontend.utils.orgs_custom_widgets.cards import JoinedOrgCard, EventCard, CollegeOrgCard, OfficerCard
from frontend.utils.orgs_custom_widgets.dialogs import OfficerDialog
from frontend.utils.orgs_custom_widgets.tables import ViewMembers, ViewApplicants
from frontend.utils.orgs_custom_widgets.dialogs import EditMemberDialog
from frontend.ui.org_main_ui import Ui_MainWindow

class ActionDelegate(QStyledItemDelegate):
    edit_clicked = QtCore.pyqtSignal(int)
    kick_clicked = QtCore.pyqtSignal(int)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        edit_btn = QPushButton("Edit", editor)
        edit_btn.clicked.connect(lambda: self.edit_clicked.emit(index.row()))
        layout.addWidget(edit_btn)

        kick_btn = QPushButton("Kick", editor)
        kick_btn.clicked.connect(lambda: self.kick_clicked.emit(index.row()))
        layout.addWidget(kick_btn)

        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class EditOrgDialog(QtWidgets.QDialog):
    def __init__(self, org_data: Dict, parent: QtWidgets.QMainWindow):
        super().__init__(parent)
        self.org_data = org_data
        self.parent_window = parent
        self.setWindowTitle("Edit Organization/Branch Details")
        self.setFixedSize(600, 500)

        main_layout = QtWidgets.QVBoxLayout(self)

        content_layout = QtWidgets.QHBoxLayout()

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        self.preview_label = QtWidgets.QLabel()
        self.preview_label.setFixedSize(200, 200)
        self.preview_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.parent_window.set_circular_logo(self.preview_label, self.parent_window._get_logo_path(org_data["logo_path"]))
        left_layout.addWidget(self.preview_label)

        browse_btn = QtWidgets.QPushButton("Browse Image")
        browse_btn.clicked.connect(self.browse_image)
        left_layout.addWidget(browse_btn)

        content_layout.addWidget(left_widget)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        right_layout.addWidget(QtWidgets.QLabel("Brief Overview"))
        self.brief_edit = QtWidgets.QTextEdit(org_data.get("brief", ""))
        right_layout.addWidget(self.brief_edit)

        right_layout.addWidget(QtWidgets.QLabel("Objectives"))
        self.desc_edit = QtWidgets.QTextEdit(org_data.get("description", ""))
        right_layout.addWidget(self.desc_edit)

        content_layout.addWidget(right_widget)
        main_layout.addLayout(content_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        confirm_btn = QtWidgets.QPushButton("Confirm")
        confirm_btn.clicked.connect(self.confirm)
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.org_data["logo_path"] = file_path
            self.parent_window.set_circular_logo(self.preview_label, file_path)

    def confirm(self):
        self.org_data["brief"] = self.brief_edit.toPlainText()
        self.org_data["description"] = self.desc_edit.toPlainText()

        self.parent_window.ui.brief_label.setText(self.org_data["brief"])
        self.parent_window.ui.obj_label.setText(self.org_data["description"])
        self.parent_window.set_circular_logo(self.parent_window.ui.logo, self.org_data["logo_path"])

        self.parent_window.save_data()

        self.accept()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, officer_name: str = "Ruben, Stephen Joseph"):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.officer_name = officer_name
        self.joined_org_count: int = 0
        self.college_org_count: int = 0
        self.officer_count: int = 0
        self.manage_applicants_btn = None
        self.is_managing: bool = False
        self.current_org: Optional[Dict] = None
        self.edit_btn: Optional[QtWidgets.QPushButton] = None
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
    def _load_data() -> List[Dict]:
        """Load organization and branch data from JSON file."""
        json_path = os.path.join(os.path.dirname(__file__), 'organizations_data.json')
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                return data.get('organizations', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {json_path}: {str(e)}")
            return []

    def save_data(self) -> None:
        """Save updated organization data back to JSON file."""
        organizations = self._load_data()
        for org in organizations:
            if org["id"] == self.current_org["id"]:
                org["brief"] = self.current_org["brief"]
                org["description"] = self.current_org["description"]
                org["logo_path"] = self.current_org["logo_path"]
                org["officers"] = self.current_org["officers"]
                org["officer_history"] = self.current_org.get("officer_history", {})
                org["members"] = self.current_org["members"]
                org["applicants"] = self.current_org.get("applicants", [])
                break

        json_path = os.path.join(os.path.dirname(__file__), 'organizations_data.json')
        try:
            with open(json_path, 'w') as file:
                json.dump({"organizations": organizations}, file, indent=4)
        except Exception as e:
            print(f"Error saving {json_path}: {str(e)}")

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
        organizations = self._load_data()
        self._clear_grid(self.ui.joined_org_grid)
        self._clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0

        filtered_joined = [org for org in organizations if org["is_joined"] and not org["is_branch"] and (search_text in org["name"].lower() or not search_text)]
        filtered_college = [org for org in organizations if not org["is_branch"] and (search_text in org["name"].lower() or not search_text)]

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
        organizations = self._load_data()
        self._clear_grid(self.ui.joined_org_grid)
        self._clear_grid(self.ui.college_org_grid)
        self.joined_org_count = 0
        self.college_org_count = 0

        filtered_joined_branches = []
        filtered_college_branches = []

        for org in organizations:
            for branch in org.get("branches", []):
                if search_text in branch["name"].lower() or not search_text:
                    if branch["is_joined"]:
                        filtered_joined_branches.append(branch)
                    filtered_college_branches.append(branch)

        for branch in filtered_joined_branches:
            self._add_joined_org(branch)
        for branch in filtered_college_branches:
            self._add_college_org(branch)

        if self.joined_org_count == 0:
            self._add_no_record_label(self.ui.joined_org_grid)
        if self.college_org_count == 0:
            self._add_no_record_label(self.ui.college_org_grid)

        self._update_scroll_areas()

    def load_members(self, search_text: str = "") -> None:
        """Load members into the table view, filtered by search text."""
        if not self.current_org:
            return

        members = self.current_org.get("members", [])
        filtered_members = [mem for mem in members if search_text in mem[0].lower() or not search_text]

        model = ViewMembers(filtered_members, self.is_managing)
        self.table.setModel(model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().hide()

        # Remove existing Manage Applicants button if present
        if self.manage_applicants_btn:
            self.ui.verticalLayout_16.removeWidget(self.manage_applicants_btn)
            self.manage_applicants_btn.deleteLater()
            self.manage_applicants_btn = None
            # Restore original header layout
            self.ui.verticalLayout_16.removeItem(self.ui.verticalLayout_16.itemAt(0))  # Remove header_hlayout
            self.ui.verticalLayout_16.insertWidget(0, self.ui.label_2)
            self.ui.verticalLayout_16.addWidget(self.ui.line_5)

        if self.is_managing:
            for row in range(len(filtered_members)):
                action_widget = QtWidgets.QWidget()
                hlayout = QtWidgets.QHBoxLayout(action_widget)
                hlayout.setContentsMargins(5, 5, 5, 5)
                hlayout.setSpacing(5)

                edit_btn = QtWidgets.QPushButton("Edit")
                edit_btn.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
                edit_btn.clicked.connect(lambda checked, r=row: self.edit_member(r))

                kick_btn = QtWidgets.QPushButton("Kick")
                kick_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
                kick_btn.clicked.connect(lambda checked, r=row: self.kick_member(r))

                hlayout.addWidget(edit_btn)
                hlayout.addWidget(kick_btn)

                self.table.setIndexWidget(model.index(row, model.columnCount() - 1), action_widget)

            # Add Manage Applicants button only if user is an officer
            self.ui.verticalLayout_16.removeWidget(self.ui.label_2)
            self.ui.verticalLayout_16.removeWidget(self.ui.line_5)
            header_hlayout = QtWidgets.QHBoxLayout()
            self.ui.label_2.setText("Member List")
            header_hlayout.addWidget(self.ui.label_2)
            header_hlayout.addStretch()
            self.manage_applicants_btn = QtWidgets.QPushButton("Manage Applicants")
            self.manage_applicants_btn.setStyleSheet("background-color: #084924; color: white; border-radius: 5px;")
            self.manage_applicants_btn.clicked.connect(self.manage_applicants)
            header_hlayout.addWidget(self.manage_applicants_btn)
            self.ui.verticalLayout_16.insertLayout(0, header_hlayout)
            self.ui.verticalLayout_16.addWidget(self.ui.line_5)

        if not filtered_members:
            self.table.hide()
            self.no_member_label.show()
        else:
            self.table.show()
            self.no_member_label.hide()

    def manage_applicants(self):
        """Load applicants into the table view with action buttons."""
        if not self.current_org:
            return

        applicants = self.current_org.get("applicants", [])

        model = ViewApplicants(applicants)
        self.table.setModel(model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().hide()

        for row in range(len(applicants)):
            action_widget = QtWidgets.QWidget()
            hlayout = QtWidgets.QHBoxLayout(action_widget)
            hlayout.setContentsMargins(5, 5, 5, 5)
            hlayout.setSpacing(5)

            details_btn = QtWidgets.QPushButton("Details")
            details_btn.setStyleSheet("background-color: #FFD700; color: black; border-radius: 5px;")

            accept_btn = QtWidgets.QPushButton("Accept")
            accept_btn.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
            accept_btn.clicked.connect(lambda checked, r=row: self.accept_applicant(r))

            decline_btn = QtWidgets.QPushButton("Decline")
            decline_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
            decline_btn.clicked.connect(lambda checked, r=row: self.decline_applicant(r))

            hlayout.addWidget(details_btn)
            hlayout.addWidget(accept_btn)
            hlayout.addWidget(decline_btn)

            self.table.setIndexWidget(model.index(row, model.columnCount() - 1), action_widget)

        self.ui.label_2.setText("Applicant List")
        self.ui.stacked_widget.setCurrentIndex(2)
        self.no_member_label.setVisible(not applicants)

    def accept_applicant(self, row: int):
        """Confirm and move applicant to members list."""
        applicant = self.current_org["applicants"][row]
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Accept",
            f"Are you sure you want to accept {applicant[0]} as a member?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            # Remove from applicants
            self.current_org["applicants"].pop(row)
            # Add to members with default status + join date
            self.current_org["members"].append([
                applicant[0], applicant[1], "Active",
                QtCore.QDate.currentDate().toString("yyyy-MM-dd")
            ])
            self.save_data()
            self.manage_applicants()

    def decline_applicant(self, row: int):
        """Confirm and remove applicant from list."""
        applicant = self.current_org["applicants"][row]
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Decline",
            f"Are you sure you want to decline {applicant[0]}'s application?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            self.current_org["applicants"].pop(row)
            self.save_data()
            self.manage_applicants()

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
            org_data["details"], org_data, self
        )
        col = self.college_org_count % 5
        row = self.college_org_count // 5
        self.ui.college_org_grid.addWidget(card, row, col, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.college_org_count += 1
        self.ui.college_org_grid.setRowMinimumHeight(row, 300)

    def set_circular_logo(self, logo_label: QtWidgets.QLabel, logo_path: str, size: int = 200, border_width: int = 4) -> None:
        """Set a circular logo with a border on the given label."""
        logo_label.setFixedSize(size, size)
        if logo_path == "No Photo" or QtGui.QPixmap(logo_path).isNull():
            logo_label.setText("No Logo")
            return

        pixmap = QtGui.QPixmap(logo_path).scaled(size, size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        centered_pixmap = QtGui.QPixmap(size, size)
        centered_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        
        with QtGui.QPainter(centered_pixmap) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            x = (size - pixmap.width()) // 2
            y = (size - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)

        mask = QtGui.QPixmap(size, size)
        mask.fill(QtCore.Qt.GlobalColor.transparent)
        with QtGui.QPainter(mask) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            path = QtGui.QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.fillPath(path, QtCore.Qt.GlobalColor.white)

        centered_pixmap.setMask(mask.createMaskFromColor(QtCore.Qt.GlobalColor.white, QtCore.Qt.MaskMode.MaskOutColor))

        final_pixmap = QtGui.QPixmap(size, size)
        final_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
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
        officers = self.current_org.get("officer_history", {}).get(selected_semester, []) if selected_semester != "Current Officers" else self.current_org.get("officers", [])
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

    def open_edit_dialog(self):
        """Open the edit dialog for current org."""
        if self.current_org:
            dialog = EditOrgDialog(self.current_org, self)
            dialog.exec()

    def show_org_details(self, org_data: Dict) -> None:
        """Display organization details on the details page."""
        self.current_org = org_data

        # Remove existing edit button if present
        if self.edit_btn:
            self.ui.verticalLayout_10.removeWidget(self.edit_btn)
            self.edit_btn.deleteLater()
            self.edit_btn = None

        self.ui.header_label_2.setText("Organization" if not org_data["is_branch"] else "Branch")
        self.ui.status_btn.setText("Active")
        self.ui.org_name.setText(org_data["name"])
        self.ui.org_type.setText("Branch" if org_data["is_branch"] else "Organization")
        self.ui.brief_label.setText(org_data.get("brief", "No brief available"))
        self.ui.obj_label.setText(org_data.get("description", "No description available"))
        self.ui.obj_label_2.setText("\n".join([branch["name"] for branch in org_data.get("branches", [])]) or "No branches available")
        self.set_circular_logo(self.ui.logo, self._get_logo_path(org_data["logo_path"]))
        
        self.ui.officer_history_dp.clear()
        semesters = org_data.get("officer_history", {}).keys()
        self.ui.officer_history_dp.addItem("Current Officers")
        self.ui.officer_history_dp.addItems(sorted(semesters))
        
        self.load_officers(org_data.get("officers", []))
        self.load_events(org_data.get("events", []))
        self.ui.label.setText("A.Y. 2025-2026 - 1st Semester")

        # Officer check: Add edit button if user is an officer
        officers = org_data.get("officers", [])
        officer_names = [off.get("name", "") for off in officers]
        self.is_managing = self.officer_name in officer_names
        if self.is_managing:
            self.ui.view_members_btn.setText("Manage Members")
            self.edit_btn = QtWidgets.QPushButton("Edit")
            self.edit_btn.setObjectName("edit_btn")
            self.edit_btn.clicked.connect(self.open_edit_dialog)
            # Insert after derscription_container (find index and insert)
            desc_index = self.ui.verticalLayout_10.indexOf(self.ui.derscription_container)
            self.ui.verticalLayout_10.insertWidget(desc_index + 1, self.edit_btn)
        else:
            self.ui.view_members_btn.setText("View Members")

        self.ui.stacked_widget.setCurrentIndex(1)

    def _to_members_page(self) -> None:
        """Navigate to the members page."""
        self.load_members()
        self.ui.stacked_widget.setCurrentIndex(2)

    def _return_to_prev_page(self) -> None:
        """Navigate back to the previous page."""
        if self.ui.stacked_widget.currentIndex() == 2:
            # If currently viewing applicants, go back to members
            if self.ui.label_2.text() == "Applicant List":
                self.load_members()
            else:
                self.ui.stacked_widget.setCurrentIndex(1)
        else:
            self.load_orgs() if self.ui.comboBox.currentIndex() == 0 else self.load_branches()
            self.ui.stacked_widget.setCurrentIndex(0)

    def update_officer_in_org(self, updated_officer: Dict) -> None:
        """Update the officer data in the current organization and save."""
        if not self.current_org:
            return
        # Update current officers
        if "officers" in self.current_org:
            for i, off in enumerate(self.current_org["officers"]):
                if off["name"] == updated_officer["name"]:
                    self.current_org["officers"][i] = updated_officer
                    break
        # Update in officer history if present
        if "officer_history" in self.current_org:
            for semester, offs in self.current_org["officer_history"].items():
                for i, off in enumerate(offs):
                    if off["name"] == updated_officer["name"]:
                        self.current_org["officer_history"][semester][i] = updated_officer
                        break
        self.save_data()
        # Refresh officers display
        current_index = self.ui.officer_history_dp.currentIndex()
        selected_semester = self.ui.officer_history_dp.itemText(current_index)
        officers = self.current_org.get("officer_history", {}).get(selected_semester, []) if selected_semester != "Current Officers" else self.current_org.get("officers", [])
        self.load_officers(officers)

    def edit_member(self, row: int) -> None:
        """Open dialog to edit member's position."""
        if not self.current_org:
            return
        # Get filtered members based on current search text
        search_text = self.ui.search_line_3.text().strip().lower()
        members = self.current_org.get("members", [])
        filtered_members = [mem for mem in members if search_text in mem[0].lower() or not search_text]
        
        if row >= len(filtered_members):
            return
        
        # Map filtered member back to original member index
        filtered_member = filtered_members[row]
        original_index = next((i for i, mem in enumerate(members) if mem[0] == filtered_member[0]), None)
        
        if original_index is None:
            return
        
        member = self.current_org["members"][original_index]
        dialog = EditMemberDialog(member, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_position = dialog.updated_position
            self.current_org["members"][original_index][1] = new_position
            self.save_data()
            self.load_members(self.ui.search_line_3.text().strip().lower())

    def kick_member(self, row: int) -> None:
        """Remove a member from the organization."""
        if not self.current_org:
            return
        search_text = self.ui.search_line_3.text().strip().lower()
        members = self.current_org.get("members", [])
        filtered_members = [mem for mem in members if search_text in mem[0].lower() or not search_text]
        
        if row >= len(filtered_members):
            return
        
        filtered_member = filtered_members[row]
        original_index = next((i for i, mem in enumerate(members) if mem[0] == filtered_member[0]), None)
        
        if original_index is None:
            return
        
        confirm = QMessageBox.question(
            self, "Confirm Kick",
            f"Are you sure you want to kick {members[original_index][0]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            del self.current_org["members"][original_index]
            self.save_data()
            self.load_members(search_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())