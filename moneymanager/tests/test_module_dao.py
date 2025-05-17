"""Tests for DAO functions"""
import unittest
import os

from moneymanager.controller.entrycontroller import DAO
from moneymanager.utils.entry import Entry


class TestDAOCreate(unittest.TestCase):
    """Tests for database creation"""
    def setUp(self):
        """Setting up needs for database creation test"""
        self.dao = DAO.getinstance("test1.db")

    def test_dao_creation_and_reading(self):
        """Test database creation"""
        self.dao.initializedb()
        self.assertTrue(self.dao.listentries() == [])

    def tearDown(self):
        """Delete database creation test needs"""
        os.remove("test1.db")


class TestDAODelete(unittest.TestCase):
    """Tests for database deletion"""
    def setUp(self):
        """Setting up needs for database deletion test"""
        self.dao = DAO.getinstance("test2.db")

    def test_dao_deletion(self):
        """Test database deletion"""
        self.dao.initializedb()
        self.dao.deletehistory()
        error = False
        try:
            res = self.dao.listentries()
            print(res)
        except ():
            error = True
        finally:
            self.assertTrue(error)

    def tearDown(self):
        """Delete database deletion test needs"""
        os.remove("test2.db")


class TestDAOAdd(unittest.TestCase):
    """Tests for database entry addition"""
    def setUp(self):
        """Setting up needs for database entry addition"""
        self.dao = DAO.getinstance("test3.db")

    def test_dao_creation_addition_and_read(self):
        """Test database entry addition"""
        self.dao.initializedb()
        entry = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        self.dao.addentry(entry)
        self.assertTrue(self.dao.listentries()[0] == entry)

    def tearDown(self):
        """Delete entry addition test needs"""
        os.remove("test3.db")


class TestDAOImport(unittest.TestCase):
    """Tests for database export file import"""
    def setUp(self):
        """Setting up needs for database export file import"""
        self.dao = DAO.getinstance("test4.db")

    def test_dao_creation_addition_and_read(self):
        """Test database export file import"""
        self.dao.initializedb()
        entry1 = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        entry2 = Entry(("Wallet", 400, 100, 500, "2025-01-02", "Reason2"))
        self.dao.importhistory([entry1, entry2])
        self.assertTrue(self.dao.listentries()[0] == entry1)
        self.assertTrue(self.dao.listentries()[1] == entry2)

    def tearDown(self):
        """Delete database export file import test needs"""
        os.remove("test4.db")
