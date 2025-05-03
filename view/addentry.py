"""Class for tab that adds entries to the history"""
import datetime
import sys

from PyQt6.QtCore import QSize, pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget, QSpinBox, QComboBox, QCheckBox,
    QCalendarWidget, QPushButton, QLabel,
    QGridLayout, QTextEdit
)

from utils.entry import Entry
from utils.dialogs import AlertDialog
from utils import data
from utils import functions
from controller.entrycontroller import EntryController

class AddEntryTab(QWidget):
    """Class for tab that adds entries to the history"""
    size = QSize(450, 650)

    maxvalue=min(2147483647,sys.maxsize)
    entryadded = pyqtSignal(Entry, name="entryadded")

    def __init__(self):
        """Initializes class for tab that adds entries to the history"""
        super().__init__()
        self.amount_spinbox = QSpinBox()
        self.wallet_combobox = QComboBox()
        self.date_picker = QCalendarWidget()
        self.reason_lineedit = QTextEdit()
        self.action_type_checkbox=QCheckBox("Spent")

        self.reset_button = QPushButton("Reset")
        self.submit_button = QPushButton("Submit")

        self.set_up_widgets()
        self.connect_signals()
        self.set_up_layout()


    def addentry(self):
        """Adds entry to the database if necessary data has been entered,
         if not it throws custom QDialog showing the error"""
        if self.amount_spinbox.value()==0:
            dlg = AlertDialog(
                "Error",
                "Enter a valid amount in the amount field!",self
            )
            dlg.exec()
        elif self.wallet_combobox.currentIndex()==-1:
            dlg = AlertDialog("Error", "Choose a wallet from the wallet combobox!", self)
            dlg.exec()
        elif self.reason_lineedit.toPlainText()== "":
            dlg = AlertDialog("Error", "Enter a reason in the reason field!", self)
            dlg.exec()
        else:
            amount= self.amount_spinbox.value() * -1 if\
                self.action_type_checkbox.isChecked() else self.amount_spinbox.value()
            after= data.walletList[self.wallet_combobox.currentText()] + amount
            before=data.walletList[self.wallet_combobox.currentText()]
            newentry = Entry((
                self.wallet_combobox.currentText(),
                amount,
                before,
                after,
                self.date_picker.selectedDate().toString("yyyy-MM-dd"),
                self.reason_lineedit.toPlainText()
            ))
            EntryController.getinstance().addentry(newentry)
            data.walletList[self.wallet_combobox.currentText()]=after
            functions.update_walletfile()
            data.entryList.append(newentry)
            self.entryadded.emit(newentry)
            self.reset_fields()

    def reset_fields(self):
        """Resets the entry fields"""
        self.amount_spinbox.setValue(0)
        self.wallet_combobox.setCurrentIndex(-1)
        self.date_picker.setMaximumDate(datetime.date.today())
        self.date_picker.setSelectedDate(datetime.date.today())
        self.reason_lineedit.clear()
        self.action_type_checkbox.setChecked(False)

    def update_walletcombobox(self, deleted=False, wallet=None):
        """Updates wallet combobox items"""
        chosen=self.wallet_combobox.currentText()
        self.wallet_combobox.clear()
        self.wallet_combobox.addItems(data.walletList.keys())
        if not deleted or (deleted and wallet!=chosen):
            if chosen != "" and chosen in data.walletList.keys():
                self.wallet_combobox.setCurrentText(chosen)
            else:
                self.wallet_combobox.setCurrentIndex(-1)

    def update_amountspinbox(self):
        """Updates amount spinbox maximum value based on wallet"""
        if self.wallet_combobox.currentText()!= "":
            if self.action_type_checkbox.isChecked():
                self.amount_spinbox.setMaximum(data.walletList[self.wallet_combobox.currentText()])
            else:
                self.amount_spinbox.setMaximum(self.maxvalue)

    def connect_signals(self):
        """Connects signals from widgets"""
        self.wallet_combobox.currentTextChanged.connect(self.update_amountspinbox)
        self.action_type_checkbox.checkStateChanged.connect(self.update_amountspinbox)
        self.submit_button.clicked.connect(self.addentry)
        self.reset_button.clicked.connect(self.reset_fields)

    def set_up_widgets(self):
        """Sets up and formats widgets"""
        self.amount_spinbox.setMinimum(0)
        self.amount_spinbox.setMaximum(self.maxvalue)
        self.amount_spinbox.setFixedWidth(105)
        self.wallet_combobox.addItems(data.walletList.keys())
        self.wallet_combobox.setCurrentIndex(-1)
        self.action_type_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_type_checkbox.setFixedWidth(55)
        self.date_picker.setMaximumDate(datetime.date.today())
        self.reason_lineedit.setFixedHeight(100)
        self.reason_lineedit.setPlaceholderText("Enter your reason")
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_up_layout(self):
        """Sets up and formats layout"""
        form_grid = QGridLayout()

        form_grid.addWidget(QLabel("Amount:"), 0, 0)
        form_grid.addWidget(self.amount_spinbox, 0, 1)
        form_grid.addWidget(QLabel("Wallet:"), 1, 0)
        form_grid.addWidget(self.wallet_combobox, 1, 1)
        form_grid.addWidget(QLabel("Date:"), 2, 0)
        form_grid.addWidget(self.date_picker, 2, 1)
        form_grid.addWidget(QLabel("Reason:"), 3, 0)
        form_grid.addWidget(self.reason_lineedit, 3, 1)
        form_grid.addWidget(self.action_type_checkbox, 4, 0)
        form_grid.addWidget(self.reset_button, 5, 0)
        form_grid.addWidget(self.submit_button, 5, 1)

        form_grid.setSpacing(10)

        self.setLayout(form_grid)
