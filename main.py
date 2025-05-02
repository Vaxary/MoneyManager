"""Main window class and base functions of the app"""
from utils import (Qt, QWidget, QApplication, QVBoxLayout, QMainWindow, QTableView,
                   QStandardItemModel, QTabWidget,
                   QAbstractItemView, tabnames, functions, data)
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

        self.wallettable=QTableView()
        self.model = QStandardItemModel()
        self.set_up_wallettable()
        self.fill_wallettable()

        self.tabs = QTabWidget()
        self.addentrytab = AddEntryTab()
        self.changewalletstab = ChangeWalletTab()
        self.listentriestab = ListTab()
        self.iotab = IOTab()
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
        self.wallettable.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        self.model.setHorizontalHeaderLabels(['Wallet', 'Amount'])

    def set_up_wallettable(self):
        """Format and set the basic attributes of the table that contains the wallets"""
        self.wallettable.setSortingEnabled(True)
        self.wallettable.horizontalHeader().setStretchLastSection(True)
        self.wallettable.setModel(self.model)
        self.wallettable.setFixedHeight(100)
        self.wallettable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.wallettable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def connect_signals(self):
        """Connect the signals for the widgets of the main window"""
        self.tabs.currentChanged.connect(self.change_windowsize)

    def connect_intertab_signals(self):
        """Connect the signals that are between tabs"""
        self.changewalletstab.walletchanged.connect(self.addentrytab.update_walletcombobox)
        self.changewalletstab.walletchanged.connect(self.changewalletstab.fill_walletcombobox)
        self.changewalletstab.walletchanged.connect(self.fill_wallettable)

        self.iotab.dataimported.connect(self.fill_wallettable)
        self.iotab.dataimported.connect(self.listentriestab.load_items)
        self.iotab.dataimported.connect(self.addentrytab.update_walletcombobox)
        self.iotab.dataimported.connect(self.changewalletstab.fill_walletcombobox)

        self.iotab.datadeleted.connect(self.fill_wallettable)
        self.iotab.datadeleted.connect(self.listentriestab.load_items)
        self.iotab.datadeleted.connect(self.addentrytab.update_walletcombobox)
        self.iotab.datadeleted.connect(self.changewalletstab.fill_walletcombobox)

        self.addentrytab.entryadded.connect(self.fill_wallettable)
        self.addentrytab.entryadded.connect(self.listentriestab.update_list)

    def set_up_tabs(self):
        """Set up the tabs of the main window"""
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        self.tabs.addTab(self.listentriestab, tabnames.LISTENTRIES_TABNAME)
        self.tabs.addTab(self.addentrytab, tabnames.ADDENTRY_TABNAME)
        self.tabs.addTab(self.changewalletstab, tabnames.CHANGEWALLET_TABNAME)
        self.tabs.addTab(self.iotab, tabnames.IO_TABNAME)

    def set_up_layout(self):
        """Set up the layout of the main window"""
        layoutwidget = QWidget()
        vbox = QVBoxLayout()

        self.setCentralWidget(layoutwidget)
        vbox.setContentsMargins(0, 0, 0, 0)

        vbox.addWidget(self.wallettable)
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
