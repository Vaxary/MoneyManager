"""Class for tab that shows history entries"""
from PyQt6.QtCore import Qt, QSize, QModelIndex
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QTableView, QAbstractItemView, QVBoxLayout

from utils.entry import Entry
from utils.dialogs import DetailsDialog
from utils import functions
from utils import data


class ListTab(QWidget):
    """Class for tab that shows history entries"""
    size = QSize(900, 600)

    def __init__(self):
        """Initializes class for tab that shows history entries"""
        super().__init__()
        self.history_table = QTableView()
        self.model = QStandardItemModel()
        self.set_up_table()
        self.load_items()

        self.layout = QVBoxLayout()
        self.set_up_layout()
        self.setLayout(self.layout)

    def update_list(self, entry):
        """Updates table that shows the history entries with a new entry"""
        self.model.insertRow(0, functions.create_tablerow_from_entry(entry))
        self.resize_table()

    def open_details(self, item: QModelIndex):
        """Opens a custom QDialog showing the details of an entry"""
        selected_entry_data = Entry((
            self.model.itemData(self.model.index(item.row(), 0))[0],
            int(self.model.itemData(self.model.index(item.row(), 1))[0]),
            int(self.model.itemData(self.model.index(item.row(), 2))[0]),
            int(self.model.itemData(self.model.index(item.row(), 3))[0]),
            self.model.itemData(self.model.index(item.row(), 4))[0],
            self.model.itemData(self.model.index(item.row(), 5))[0],
        ))
        dlg = DetailsDialog("Details", selected_entry_data, self)
        dlg.exec()

    def load_items(self):
        """Fills the table that shows
        the history entries with the stored entries"""
        self.model.clear()
        for entry in data.entryList:
            self.model.insertRow(0, functions.
                                 create_tablerow_from_entry(entry))
        self.resize_table()
        self.model.setHorizontalHeaderLabels(
            ['Wallet', 'Amount', 'Before', 'After', 'Date', 'Reason']
        )

    def set_up_table(self):
        """Sets up and formats the table that shows
        the history entries with the stored entries"""
        self.model.setColumnCount(6)
        self.history_table.setSortingEnabled(True)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(1, 30)
        self.history_table.setModel(self.model)
        (self.history_table.
         setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers))
        self.history_table.doubleClicked.connect(self.open_details)
        (self.history_table.
         setSelectionMode(QAbstractItemView.SelectionMode.NoSelection))

    def resize_table(self):
        """Resizes and sorts the table
        that shows the history entries with the
        stored entries based on its contents"""
        self.history_table.sortByColumn(4, Qt.SortOrder.DescendingOrder)
        self.history_table.resizeColumnsToContents()

    def set_up_layout(self):
        """Sets up and formats the layout"""
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.history_table)
