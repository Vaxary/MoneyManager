"""Class for tab that changes the wallets"""
from PyQt6.QtCore import QSize, pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QPushButton, QLineEdit, QGridLayout
)

from utils.dialogs import AlertDialog
from utils import data, iofunctions


class ChangeWalletTab(QWidget):
    """Class for tab that changes the wallets"""
    size = QSize(400, 260)

    walletchanged = pyqtSignal(bool, str, name="walletchanged")

    def __init__(self):
        """Initializes class for tab that changes the wallets"""
        super().__init__()
        self.delete_wallet_combobox = QComboBox()
        self.delete_button = QPushButton("Delete Wallet")
        self.add_wallet_lineedit = QLineEdit()
        self.add_button = QPushButton("Add Wallet")

        self.set_up_widgets()
        self.fill_walletcombobox()
        self.connect_signals()

        self.change_wallet_grid = QGridLayout()
        self.set_up_layout()

        self.setLayout(self.change_wallet_grid)

    def delete_wallet(self):
        """Deletes wallet from stored wallets if it's not empty,
        if it is it shows QDialog showing the error"""
        if self.delete_wallet_combobox.currentIndex() == -1:
            dlg = AlertDialog("Error",
                              "Choose a wallet from the wallet combobox!",
                              self)
            dlg.exec()
        elif data.walletList[self.delete_wallet_combobox.currentText()] != 0:
            dlg = AlertDialog("Error",
                              "The chosen wallet is not empty!",
                              self)
            dlg.exec()
        else:
            del data.walletList[self.delete_wallet_combobox.currentText()]
            iofunctions.update_walletfile()
            (self.walletchanged.
             emit(True, self.delete_wallet_combobox.currentText()))
            self.delete_wallet_combobox.setCurrentIndex(-1)

    def add_wallet(self):
        """Adds wallet to stored wallets if wallet name QLineEdit is not empty,
        if it is it shows QDialog showing the error"""
        if self.add_wallet_lineedit.text() == "":
            dlg = AlertDialog("Error",
                              "Enter the name of the new wallet!",
                              self)
            dlg.exec()
        elif self.add_wallet_lineedit.text() in data.walletList.keys():
            dlg = AlertDialog("Error",
                              "Wallet already exists!",
                              self)
            dlg.exec()
        else:
            data.walletList[self.add_wallet_lineedit.text()] = 0
            iofunctions.update_walletfile()
            self.walletchanged.emit(False, self.add_wallet_lineedit.text())
            self.add_wallet_lineedit.setText("")

    def fill_walletcombobox(self, deleted=False, wallet=None):
        """Fills wallet combobox with stored wallets"""
        chosen = self.delete_wallet_combobox.currentText()
        self.delete_wallet_combobox.clear()
        self.delete_wallet_combobox.addItems(data.walletList.keys())
        if not deleted or (deleted and wallet != chosen):
            if chosen != "" and chosen in data.walletList.keys():
                self.delete_wallet_combobox.setCurrentText(chosen)
            else:
                self.delete_wallet_combobox.setCurrentIndex(-1)

    def set_up_widgets(self):
        """Sets up and formats widgets"""
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_wallet_lineedit.setPlaceholderText("Enter new wallet name")

    def connect_signals(self):
        """Connects signals from widgets"""
        self.delete_button.clicked.connect(self.delete_wallet)
        self.add_button.clicked.connect(self.add_wallet)

    def set_up_layout(self):
        """Sets up and formats layout"""
        self.change_wallet_grid.setContentsMargins(10, 10, 10, 10)
        self.change_wallet_grid.addWidget(self.delete_button, 0, 0)
        self.change_wallet_grid.addWidget(self.delete_wallet_combobox, 0, 1)
        self.change_wallet_grid.addWidget(self.add_button, 1, 0)
        self.change_wallet_grid.addWidget(self.add_wallet_lineedit, 1, 1)

        self.change_wallet_grid.setColumnStretch(0, 1)
        self.change_wallet_grid.setColumnStretch(1, 1)
        self.change_wallet_grid.setRowStretch(0, 1)
        self.change_wallet_grid.setRowStretch(1, 1)
