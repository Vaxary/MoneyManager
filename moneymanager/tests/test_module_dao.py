"""Tests for DAO functions"""
import sqlite3
import unittest
import os

from moneymanager.controller.entrycontroller import DAO
from moneymanager.utils.entry import Entry


class TestDAOCreate(unittest.TestCase):
    """Tests for database creation"""

    def test_dao_creation_and_reading(self):
        """Test database creation"""
        dao = DAO.getinstance("test1.db")
        dao.initializedb()
        self.assertTrue(dao.listentries() == [])
        os.remove("test1.db")


class TestDAODelete(unittest.TestCase):
    """Tests for database deletion"""

    def test_dao_deletion(self):
        """Test database deletion"""
        dao = DAO.getinstance("test2.db")
        dao.initializedb()
        dao.deletehistory()
        error = False
        try:
            res = dao.listentries()
            print(res)
        except sqlite3.OperationalError:
            error = True
        finally:
            self.assertTrue(error)
            os.remove("test2.db")


class TestDAOAdd(unittest.TestCase):
    """Tests for database entry addition"""

    def test_dao_creation_addition_and_read(self):
        """Test database entry addition"""
        dao = DAO.getinstance("test3.db")
        dao.initializedb()
        entry = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        dao.addentry(entry)
        self.assertTrue(dao.listentries()[0] == entry)
        os.remove("test3.db")


class TestDAOImport(unittest.TestCase):
    """Tests for database export file import"""

    def test_dao_creation_addition_and_read(self):
        """Test database export file import"""
        dao = DAO.getinstance("test4.db")
        dao.initializedb()
        entry1 = Entry(("Wallet", 100, 0, 100, "2025-01-01", "Reason"))
        entry2 = Entry(("Wallet", 400, 100, 500, "2025-01-02", "Reason2"))
        dao.importhistory([entry1, entry2])
        self.assertTrue(dao.listentries()[0] == entry1)
        self.assertTrue(dao.listentries()[1] == entry2)
        os.remove("test4.db")
