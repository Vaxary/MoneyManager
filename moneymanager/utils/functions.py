"""Various functions needed to manage data"""
from moneymanager.utils.customitems import CaseInsensitiveStandardItem, NumStandardItem
from moneymanager.utils.entry import Entry


def create_entry_from_db(row):
    """Creates an entry from one row of the database provided data"""
    entry = Entry((row[0], row[1], row[2], row[3], row[4], row[5]))
    return entry


def create_tablerow_from_entry(entry):
    """Creates a row compatible
    with QStandardItemModel that is used in tables"""
    return [
        CaseInsensitiveStandardItem(str(entry.wallet)),
        NumStandardItem(str(entry.amount)),
        NumStandardItem(str(entry.before)),
        NumStandardItem(str(entry.after)),
        CaseInsensitiveStandardItem(str(entry.date)),
        CaseInsensitiveStandardItem(str(entry.reason))
    ]
