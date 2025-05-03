"""Main window class and base functions of the app"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QTabWidget, QAbstractItemView, QWidget, QVBoxLayout, QApplication
)

from utils import (tabnames, functions, data)
from utils.customitems import CaseInsensitiveStandardItem, NumStandardItem
from view.addentry import AddEntryTab
from view.changewallets import ChangeWalletTab
from view.listentries import ListTab
from view.iotab import IOTab

class MainWindow(QMainWindow):
    """Main window of the app"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Management")

        self.wallet_table=QTableView()
        self.model = QStandardItemModel()
        self.set_up_wallettable()
        self.fill_wallettable()

        self.tabs = QTabWidget()
        self.add_entry_tab = AddEntryTab()
        self.change_wallets_tab = ChangeWalletTab()
        self.list_entries_tab = ListTab()
        self.io_tab = IOTab()
        self.set_up_tabs()

        self.connect_intertab_signals()
        self.connect_signals()
        self.set_up_layout()


    def change_windowsize(self, i):
        """Change the size of the main window based on the tab we navigate to"""
        if self.tabs.tabText(i)==tabnames.LISTENTRIES_TABNAME:
            self.setFixedSize(ListTab.size)
        elif self.tabs.tabText(i)==tabnames.ADDENTRY_TABNAME:
            self.setFixedSize(AddEntryTab.size)
        elif self.tabs.tabText(i)==tabnames.CHANGEWALLET_TABNAME:
            self.setFixedSize(ChangeWalletTab.size)
        elif self.tabs.tabText(i)==tabnames.IO_TABNAME:
            self.setFixedSize(IOTab.size)

    def fill_wallettable(self):
        """Fill the table that contains the wallets with data"""
        self.model.clear()
        for item in data.walletList.items():
            row=[
                CaseInsensitiveStandardItem(item[0]),
                NumStandardItem(str(item[1]))
            ]
            self.model.insertRow(0,row)
        self.wallet_table.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        self.model.setHorizontalHeaderLabels(['Wallet', 'Amount'])

    def set_up_wallettable(self):
        """Format and set the basic attributes of the table that contains the wallets"""
        self.wallet_table.setSortingEnabled(True)
        self.wallet_table.horizontalHeader().setStretchLastSection(True)
        self.wallet_table.setModel(self.model)
        self.wallet_table.setFixedHeight(100)
        self.wallet_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.wallet_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def connect_signals(self):
        """Connect the signals for the widgets of the main window"""
        self.tabs.currentChanged.connect(self.change_windowsize)

    def connect_intertab_signals(self):
        """Connect the signals that are between tabs"""
        self.change_wallets_tab.walletchanged.connect(self.add_entry_tab.update_walletcombobox)
        self.change_wallets_tab.walletchanged.connect(self.change_wallets_tab.fill_walletcombobox)
        self.change_wallets_tab.walletchanged.connect(self.fill_wallettable)

        self.io_tab.dataimported.connect(self.fill_wallettable)
        self.io_tab.dataimported.connect(self.list_entries_tab.load_items)
        self.io_tab.dataimported.connect(self.add_entry_tab.update_walletcombobox)
        self.io_tab.dataimported.connect(self.change_wallets_tab.fill_walletcombobox)

        self.io_tab.datadeleted.connect(self.fill_wallettable)
        self.io_tab.datadeleted.connect(self.list_entries_tab.load_items)
        self.io_tab.datadeleted.connect(self.add_entry_tab.update_walletcombobox)
        self.io_tab.datadeleted.connect(self.change_wallets_tab.fill_walletcombobox)

        self.add_entry_tab.entryadded.connect(self.fill_wallettable)
        self.add_entry_tab.entryadded.connect(self.list_entries_tab.update_list)

    def set_up_tabs(self):
        """Set up the tabs of the main window"""
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        self.tabs.addTab(self.list_entries_tab, tabnames.LISTENTRIES_TABNAME)
        self.tabs.addTab(self.add_entry_tab, tabnames.ADDENTRY_TABNAME)
        self.tabs.addTab(self.change_wallets_tab, tabnames.CHANGEWALLET_TABNAME)
        self.tabs.addTab(self.io_tab, tabnames.IO_TABNAME)

    def set_up_layout(self):
        """Set up the layout of the main window"""
        layoutwidget = QWidget()
        vbox = QVBoxLayout()

        self.setCentralWidget(layoutwidget)
        vbox.setContentsMargins(0, 0, 0, 0)

        vbox.addWidget(self.wallet_table)
        vbox.addWidget(self.tabs)

        layoutwidget.setLayout(vbox)


if __name__ == '__main__':
    functions.initialize_files_and_dirs()
    functions.load_initialdata()
    app = QApplication([])
    window = MainWindow()
    window.show()
    if len(data.walletList)==0:
        window.tabs.setCurrentIndex(2)
    elif len(data.entryList)==0:
        window.tabs.setCurrentIndex(1)
    else:
        window.tabs.setCurrentIndex(0)
        window.setFixedSize(ListTab.size)
    app.exec()
