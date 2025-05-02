"""Custom QDialog implementations for various usecases"""
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QTextEdit
)

class AlertDialog(QDialog):
    """Custom QDialog implementation for alerting user of a mistake"""
    size = QSize(300, 100)

    def __init__(self, title, msg, parent=None):
        """Initializing custom QDialog implementation for alerting user of a mistake"""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(self.size)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.connect_signals()

        self.set_up_layout(msg)

    def connect_signals(self):
        """Connecting the accept and reject events from the button box"""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def set_up_layout(self, msg):
        """Set up the layout for the custom QDialog"""
        layout = QVBoxLayout()
        message = QLabel(msg)
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)


class SureDialog(QDialog):
    """Custom QDialog implementation for
    making sure the user wants to take the given action"""
    size = QSize(350, 100)

    def __init__(self, title, msg, parent=None):
        """Initializing QDialog implementation for
        making sure the user wants to take the given action"""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(self.size)

        self.button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.connect_signals()
        self.set_up_layout(msg)

    def connect_signals(self):
        """Connecting the accept and reject events from the button box"""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def set_up_layout(self, msg):
        """Set up the layout for the custom QDialog"""
        layout = QVBoxLayout()
        message = QLabel(msg)
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

class DetailsDialog(QDialog):
    """Custom QDialog implementation for
    viewing the details of an entry"""
    size = QSize(400, 500)

    def __init__(self, title, entry, parent=None):
        """Initializing custom QDialog implementation for
        viewing the details of an entry"""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(self.size)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.connect_signals()

        self.set_up_window(entry)

    def connect_signals(self):
        """Connecting the accept and reject events from the button box"""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def set_up_window(self, entry):
        """Set up the layout with the variables for the custom QDialog"""
        layout = QGridLayout()
        amount_label = QLabel("Amount:")
        amount_value = QLineEdit(str(entry.amount) + " Ft")
        amount_value.setReadOnly(True)

        before_label = QLabel("Before:")
        before_value = QLineEdit(str(entry.before) + " Ft")
        before_value.setReadOnly(True)

        after_label = QLabel("After:")
        after_value = QLineEdit(str(entry.after) + " Ft")
        after_value.setReadOnly(True)

        wallet_label = QLabel("Wallet:")
        wallet_value = QLineEdit(entry.wallet)
        wallet_value.setReadOnly(True)

        date_label = QLabel("Date:")
        date_value = QLineEdit(entry.date)
        date_value.setReadOnly(True)

        reason_label = QLabel("Reason:")
        reason_value = QTextEdit()
        reason_value.setText(entry.reason)
        reason_value.setReadOnly(True)

        layout.addWidget(wallet_label, 0, 0)
        layout.addWidget(wallet_value, 0, 1)
        layout.addWidget(amount_label, 1, 0)
        layout.addWidget(amount_value, 1, 1)
        layout.addWidget(before_label, 2, 0)
        layout.addWidget(before_value, 2, 1)
        layout.addWidget(after_label, 3, 0)
        layout.addWidget(after_value, 3, 1)
        layout.addWidget(date_label, 4, 0)
        layout.addWidget(date_value, 4, 1)
        layout.addWidget(reason_label, 5, 0)
        layout.addWidget(reason_value, 5, 1)

        layout.addWidget(self.button_box, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
