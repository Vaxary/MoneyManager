"""Entry controller class"""
from model.dao import DAO
from utils.paths import HISTORYDATABASEPATH


class EntryController:
    """Singleton class of database controller for entry objects"""
    _instance = None

    def __init__(self):
        """Initialize the singleton instance
        and the dao by getting the dao instance"""
        self._dao = DAO.getinstance(HISTORYDATABASEPATH)

    @staticmethod
    def getinstance():
        """Get singleton instance of controller"""
        if EntryController._instance is None:
            EntryController._instance = EntryController()
        return EntryController._instance

    def __del__(self):
        """Destructor where the dao is deleted"""
        self._dao.__del__()

    def initializedb(self):
        """Initialize the database with the dao"""
        self._dao.initializedb()

    def addentry(self, entry):
        """Add parameter entry to the database with the dao"""
        self._dao.addentry(entry)

    def listentries(self):
        """List entries from the database with the dao"""
        return self._dao.listentries()

    def importhistory(self, entrylist: list):
        """Import parameter entry list to the database with the dao"""
        self._dao.importhistory(entrylist)

    def deletehistory(self):
        """Delete the database with the dao"""
        self._dao.deletehistory()
