import sqlite3
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query, params=None):
        pass

    @abstractmethod
    def fetch_one(self):
        pass

    @abstractmethod
    def fetch_all(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close() 