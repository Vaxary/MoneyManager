"""Various functions needed to manage data"""
import json
from os import makedirs
from pathlib import Path

from controller.entrycontroller import EntryController
from utils import data
from utils.customitems import NumStandardItem, CaseInsensitiveStandardItem
from utils.entry import Entry
from utils.paths import WALLETFILEPATH, DATAFOLDERPATH, EXPORTFOLDERPATH

def initialize_files_and_dirs():
    """Initializes the following if they don't exist:
    default data folder, default wallet json file, default export folder"""
    if not Path.is_dir(Path(DATAFOLDERPATH)):
        makedirs(DATAFOLDERPATH)

    if not Path.is_file(Path(WALLETFILEPATH)):
        default_walletfile = json.dumps({}, indent=4)
        with open(WALLETFILEPATH, "w", encoding="utf-8") as walletfile:
            walletfile.write(default_walletfile)

    if not Path.is_dir(Path(EXPORTFOLDERPATH)):
        makedirs(EXPORTFOLDERPATH)
    EntryController.getinstance().initializedb()

def load_initialdata():
    """Loads the persistent data into the data variables for inter-tab usage"""
    with open(WALLETFILEPATH, 'r', encoding="utf-8") as walletfile:
        walletfile_data = json.load(walletfile)
    data.walletList=walletfile_data
    data.entryList = EntryController.getinstance().listentries()

def update_walletfile():
    """Rewrites the wallet json file to store any changes made to the data variables"""
    walletfile_new_content = json.dumps(data.walletList, indent=4)
    with open(WALLETFILEPATH, "w", encoding="utf-8") as walletfile:
        walletfile.write(walletfile_new_content)

def create_entry_from_db(row):
    """Creates an entry from one row of the database provided data"""
    entry=Entry((row[0],row[1],row[2],row[3],row[4],row[5]))
    return entry

def create_tablerow_from_entry(entry):
    """Creates a row compatible for QStandardItemModel that is used in tables"""
    return [
        CaseInsensitiveStandardItem(str(entry.wallet)),
        NumStandardItem(str(entry.amount)),
        NumStandardItem(str(entry.before)),
        NumStandardItem(str(entry.after)),
        CaseInsensitiveStandardItem(str(entry.date)),
        CaseInsensitiveStandardItem(str(entry.reason))
    ]

def export_history_and_wallets(dest):
    """Exports the data variables into a persistent json file
    containing the contents of both the wallet and the history"""
    entrylist=[]
    for entry in data.entryList:
        entrylist.append(entry.__dict__)
    history_and_wallet_dict={"wallet":data.walletList,
                             "history":entrylist}
    export_content = json.dumps(history_and_wallet_dict, indent=4)
    with open(dest, 'w', encoding="utf-8") as walletfile:
        walletfile.write(export_content)

def import_exportfile(src):
    """Imports and loads data of exported persistent json file
        containing the contents of both the wallet and the history"""
    with open(src, 'r', encoding="utf-8") as exportfile:
        exportfile_data = json.load(exportfile)
    data.walletList.clear()
    for wallet in exportfile_data["wallet"]:
        data.walletList[wallet]=exportfile_data["wallet"][wallet]
    update_walletfile()

    data.entryList.clear()
    for importentry in exportfile_data["history"]:
        entry=Entry((importentry["_wallet"],importentry["_amount"],importentry["_before"],
                     importentry["_after"],importentry["_date"],importentry["_reason"]))
        data.entryList.append(entry)
    EntryController.getinstance().deletehistory()
    EntryController.getinstance().initializedb()
    EntryController.getinstance().importhistory(data.entryList)
