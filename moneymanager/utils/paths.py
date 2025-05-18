"""Constants storing the default locations of the program"""
import pathlib

DATAFOLDERPATH = str(pathlib.Path(__file__).absolute().parent.parent)+"/data"
WALLETFILEPATH = DATAFOLDERPATH + "/wallets.json"
EXPORTFOLDERPATH = DATAFOLDERPATH + "/exports"
HISTORYDATABASEPATH = DATAFOLDERPATH + "/history.db"
