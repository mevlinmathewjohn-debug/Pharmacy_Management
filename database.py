import mysql.connector
import mysql.connector


class DatabaseManager:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pharmacy_management"
        )

        self.cursor = self.connection.cursor(
            dictionary=True
        )

    def execute(self, query, params=None):

        self.cursor.execute(query, params or ())

        return self.cursor

    def fetch_one(self, query, params=None):

        self.cursor.execute(query, params or ())

        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):

        self.cursor.execute(query, params or ())

        return self.cursor.fetchall()

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    def close(self):

        self.cursor.close()
        self.connection.close()