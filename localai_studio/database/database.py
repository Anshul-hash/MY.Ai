"""SQLite database for ZENA."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path: str = "localai_studio/data/zena.db"):

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(db_path)

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile(

            id INTEGER PRIMARY KEY,

            name TEXT,

            creator TEXT,

            language TEXT,

            voice TEXT,

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT NOT NULL,

            content TEXT NOT NULL,

            importance INTEGER DEFAULT 5,

            approved INTEGER DEFAULT 0,

            source TEXT DEFAULT 'conversation',

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            role TEXT,

            message TEXT,

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            description TEXT,

            status TEXT

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            key TEXT PRIMARY KEY,

            value TEXT

        )
        """)

        self.connection.commit()

    def execute(self, sql: str, values=()):

        cursor = self.connection.cursor()

        cursor.execute(sql, values)

        self.connection.commit()

        return cursor

    def query(self, sql: str, values=()):

        cursor = self.connection.cursor()

        cursor.execute(sql, values)

        return cursor.fetchall()
