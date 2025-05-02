"""Data Access Object class"""
import sqlite3
from utils import functions

class DAO:
    """Data Access Object singleton class for connecting with the database"""
    _instance = None

    def __init__(self, conn):
        """Singleton instance initialization with the parameter set as the connection url"""
        self._connection = sqlite3.connect(conn)
        self._cursor = self._connection.cursor()

    @staticmethod
    def getinstance(connstring):
        """Get singleton instance of dao"""
        if DAO._instance is None:
            DAO._instance=DAO(connstring)
        return DAO._instance

    def __del__(self):
        self._connection.close()

    def initializedb(self):
        """Creating the HISTORY table in the database if it doesn't already exist"""
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS HISTORY (
               id INTEGER NOT NULL constraint history_pk primary key autoincrement,
               amount INT,
               before INT,
               after INT,
               date TEXT,
               wallet TEXT,
               reason TEXT
               );""")
        self._connection.commit()

    def addentry(self, entry):
        """Adding the given parameter entry to the HISTORY table in the database"""
        self._cursor.execute("""
        INSERT INTO HISTORY (amount, before, after, date, wallet, reason) VALUES (?, ?, ?, ?, ?, ?)
        """, (entry.amount, entry.before, entry.after, entry.date, entry.wallet, entry.reason))
        self._connection.commit()

    def listentries(self):
        """Listing the entries from the HISTORY table in the database
        and making an iterable of entry based on results"""
        res = (self._cursor
               .execute("SELECT wallet, amount, before, after, date, reason FROM HISTORY;")
               .fetchall())
        return [functions.create_entry_from_db(row) for row in res]

    def deletehistory(self):
        """Deleting the HISTORY table from the database if it already exists"""
        self._cursor.execute("""DROP TABLE IF EXISTS HISTORY;""")
        self._connection.commit()

    def importhistory(self, entrylist:list):
        """Inserting the entries at once from the parameter list
         into the HISTORY table in the database"""
        command="BEGIN TRANSACTION;"
        for entry in entrylist:
            command+=\
                (f"\nINSERT INTO HISTORY (wallet, amount, before, after, date, reason) "
                f"VALUES ('{entry.wallet}', {entry.amount}, {entry.before},"
                 f" {entry.after}, '{entry.date}', '{entry.reason}');")
        command+="\nCOMMIT;"
        self._cursor.executescript(command)
        self._connection.commit()
