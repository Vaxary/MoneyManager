"""QStandardItemModel custom QStandardItem implementations"""
from PyQt6.QtCore import QVariant
from PyQt6.QtGui import QStandardItem


class NumStandardItem(QStandardItem):
    """QStandardItem implementation for displaying Ft after currency
    and sorting based on currency numbers, not strings"""

    def data(self, role=...):
        """QStandardItem data method override for displaying Ft after currency"""
        if super().data(role) is not None:
            return QVariant(str(super().data(role)) + " Ft")
        return QVariant(None)

    def __lt__(self, other):
        """QStandardItem sort method override for number based sorting"""
        return int(str(self.data(self.model().sortRole()).value())[:-3]) < int(
            str(other.data(other.model().sortRole()).value())[:-3])


class CaseInsensitiveStandardItem(QStandardItem):
    """QStandardItem implementation for case-insensitive sorting"""

    def data(self, role=...):
        """QStandardItem data method"""
        if super().data(role) is not None:
            return QVariant(str(super().data(role)))
        return QVariant(None)

    def __lt__(self, other):
        """QStandardItem sort method override for case-insensitive sorting"""
        return (str(self.data(self.model().sortRole()).value()).lower()
                < str(other.data(other.model().sortRole()).value()).lower())
