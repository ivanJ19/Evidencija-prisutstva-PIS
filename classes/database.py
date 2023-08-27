# Imports
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        self.database_name = "database/project-student.db"
 
    # Connect to database
    def connectDB(self):
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except Error as e:
            print(e)
 

    # Create tables
    def createTables(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS usertype(id INTEGER PRIMARY KEY AUTOINCREMENT, typename TEXT NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, usertype INTEGER DEFAULT 1, name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY AUTOINCREMENT, coursename TEXT NOT NULL, description TEXT NOT NULL, link TEXT NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS courseapplication(id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER NOT NULL, courseid INTEGER NOT NULL, logindate DATETIME DEFAULT CURRENT_TIMESTAMP)
            """,
            """
            CREATE TABLE IF NOT EXISTS profesorscourses(id INTEGER PRIMARY KEY AUTOINCREMENT, profesorid INTEGER NOT NULL, courseid INTEGER NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS studentscourses(id INTEGER PRIMARY KEY AUTOINCREMENT, studentid INTEGER NOT NULL, courseid INTEGER NOT NULL, grade REAL DEFAULT 0)
            """
        ]
        db = self.connectDB()
        cursor = db.cursor()
        for table in tables:
            cursor.execute(table)
