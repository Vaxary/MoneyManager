import unittest
import os

from controller.entrycontroller import DAO
from utils.entry import Entry


class TestDAOCreate(unittest.TestCase):
    def setUp(self):
        self.dao = DAO.getinstance("test1.db")

    def test_dao_creation_and_reading(self):
        self.dao.initializedb()
        self.assertTrue(self.dao.listentries() == list())

    def tearDown(self):
        os.remove("test1.db")


class TestDAODelete(unittest.TestCase):
    def setUp(self):
        self.dao = DAO.getinstance("test2.db")

    def test_dao_deletion(self):
        self.dao.initializedb()
        self.dao.deletehistory()
        error = False
        try:
            res = self.dao.listentries()
            print(res)
        except:
            error = True
        finally:
            self.assertTrue(error)

    def tearDown(self):
        os.remove("test2.db")


class TestDAOAdd(unittest.TestCase):
    def setUp(self):
        self.dao = DAO.getinstance("test3.db")

    def test_dao_creation_addition_and_read(self):
        self.dao.initializedb()
        entry = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        self.dao.addentry(entry)
        self.assertTrue(self.dao.listentries()[0] == entry)

    def tearDown(self):
        os.remove("test3.db")

class TestDAOImport(unittest.TestCase):
    def setUp(self):
        self.dao = DAO.getinstance("test4.db")

    def test_dao_creation_addition_and_read(self):
        self.dao.initializedb()
        entry1 = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        entry2 = Entry(("Wallet", 400, 100, 500, "2025-01-02", "Reason2"))
        self.dao.importhistory([entry1,entry2])
        self.assertTrue(self.dao.listentries()[0] == entry1)
        self.assertTrue(self.dao.listentries()[1] == entry2)

    def tearDown(self):
        os.remove("test4.db")
