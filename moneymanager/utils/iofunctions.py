"""Various IO functions for various uses"""
import json
from os import makedirs
from pathlib import Path

from moneymanager.controller.entrycontroller import EntryController
from moneymanager import data
from moneymanager.utils.entry import Entry
from moneymanager.utils.paths import (
    WALLETFILEPATH,
    EXPORTFOLDERPATH,
    DATAFOLDERPATH
)


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
    data.wallet_list = walletfile_data
    data.entry_list = EntryController.getinstance().listentries()


def import_exportfile(src):
    """Imports and loads data of exported persistent json file
        containing the contents of both the wallet and the history"""
    with open(src, 'r', encoding="utf-8") as exportfile:
        exportfile_data = json.load(exportfile)
    data.wallet_list.clear()
    for wallet in exportfile_data["wallet"]:
        data.wallet_list[wallet] = exportfile_data["wallet"][wallet]
    update_walletfile()

    data.entry_list.clear()
    for importentry in exportfile_data["history"]:
        entry = Entry((importentry["_wallet"], importentry["_amount"],
                       importentry["_before"], importentry["_after"],
                       importentry["_date"], importentry["_reason"]))
        data.entry_list.append(entry)
    EntryController.getinstance().deletehistory()
    EntryController.getinstance().initializedb()
    EntryController.getinstance().importhistory(data.entry_list)


def export_history_and_wallets(dest):
    """Exports the data variables into a persistent json file
    containing the contents of both the wallet and the history"""
    entrylist = []
    for entry in data.entry_list:
        entrylist.append(entry.__dict__)
    history_and_wallet_dict = {"wallet": data.wallet_list,
                               "history": entrylist}
    export_content = json.dumps(history_and_wallet_dict, indent=4)
    with open(dest, 'w', encoding="utf-8") as export_file:
        export_file.write(export_content)


def update_walletfile():
    """Rewrites the wallet json file
    to store any changes made to the data variables"""
    walletfile_new_content = json.dumps(data.wallet_list, indent=4)
    with open(WALLETFILEPATH, "w", encoding="utf-8") as walletfile:
        walletfile.write(walletfile_new_content)
