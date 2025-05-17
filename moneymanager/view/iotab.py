"""Class for tab that exports, imports and deletes history"""
import datetime
from pathlib import Path

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QFileDialog, QGridLayout

from moneymanager.utils import paths
from moneymanager.utils.dialogs import SureDialog
from moneymanager.utils import iofunctions
from moneymanager import data
from moneymanager.controller.entrycontroller import EntryController


class IOTab(QWidget):
    """Class for tab that exports, imports and deletes history"""
    size = QSize(400, 300)

    dataimported = pyqtSignal(name="dataimported")
    datadeleted = pyqtSignal(name="datadeleted")

    def __init__(self):
        """Initializes class for tab
        that exports, imports and deletes history"""
        super().__init__()
        self.exportbutton = QPushButton("Export")
        self.importbutton = QPushButton("Import")
        self.deletebutton = QPushButton("Delete History")

        self.set_up_widgets()

        self.buttongrid = QGridLayout()
        self.set_up_layot()

        self.connect_signals()

        self.setLayout(self.buttongrid)

    def export_history(self):
        """Shows dialog for choosing a path for the export json file
        then exports history and wallets to the given file and location"""
        savedlg = QFileDialog(directory=paths.EXPORTFOLDERPATH)
        savedlg.setDefaultSuffix("json")
        savedlg.setFilter(savedlg.filter())
        savedlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        savedlg.setViewMode(QFileDialog.ViewMode.List)
        savedlg.selectFile("export"+datetime.date.today().isoformat()+".json")
        savedlg.setNameFilters(['JSON (*.json)'])
        if savedlg.exec() and savedlg.selectedFiles()[0].endswith(".json"):
            iofunctions.export_history_and_wallets(savedlg.selectedFiles()[0])

    def import_history(self):
        """Shows dialog for selecting an exported json file
        then replaces current data with
        history and wallets from the file to the database"""
        dlg = SureDialog("Importing",
                         "Are you sure? "
                         "This will replace the current history!")
        if dlg.exec():
            savedlg = QFileDialog(directory=paths.EXPORTFOLDERPATH)
            savedlg.setDefaultSuffix("json")
            savedlg.setFilter(savedlg.filter())
            savedlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
            savedlg.setDirectory(paths.EXPORTFOLDERPATH)
            savedlg.setNameFilters(['JSON (*.json)'])
            if savedlg.exec() and savedlg.selectedFiles()[0].endswith(".json"):
                if Path.is_file(Path(savedlg.selectedFiles()[0])):
                    iofunctions.import_exportfile(savedlg.selectedFiles()[0])
                    self.dataimported.emit()

    def set_up_widgets(self):
        """Sets up and formats widgets"""
        self.importbutton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exportbutton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deletebutton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.importbutton.setFixedWidth(200)
        self.exportbutton.setFixedWidth(200)
        self.deletebutton.setFixedWidth(200)

    def connect_signals(self):
        """Connects signals from widgets"""
        self.exportbutton.clicked.connect(self.export_history)
        self.importbutton.clicked.connect(self.import_history)
        self.deletebutton.clicked.connect(self.reset_history)

    def reset_history(self):
        """Deletes history from the database
        and wallets from the wallet json file"""
        dlg = SureDialog("Deleting History",
                         "Are you sure? "
                         "This will delete the current history!")
        if dlg.exec():
            EntryController.getinstance().deletehistory()
            EntryController.getinstance().initializedb()
            data.wallet_list.clear()
            iofunctions.update_walletfile()
            data.entry_list.clear()
            self.datadeleted.emit()

    def set_up_layot(self):
        """Sets up and formats layout"""
        self.buttongrid.addWidget(self.importbutton, 0, 0)
        self.buttongrid.addWidget(self.exportbutton, 1, 0)
        self.buttongrid.addWidget(self.deletebutton, 2, 0)
        self.buttongrid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.buttongrid.setSpacing(20)
