"""
Database connector for SQLite and PostgreSQL.
Provides unified interface for both database backends.
"""

import sqlite3
from typing import Optional, List, Tuple, Any, Dict


class DatabaseConnector:
    """Base class for database connectors."""
    
    def __init__(self, db_path: Optional[str] = None, **kwargs):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        raise NotImplementedError
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    
    def execute_many(self, query: str, params: List[Tuple]) -> None:
        cursor = self.connection.cursor()
        cursor.executemany(query, params)
        self.connection.commit()


class SQLiteConnector(DatabaseConnector):
    """SQLite database connector."""
    
    def __init__(self, db_path: str = "ecommerce.db"):
        super().__init__(db_path)
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        self.disconnect()


class PostgreSQLConnector:
    """PostgreSQL database connector using pg8000."""
    
    def __init__(self, host: str = "localhost", port: int = 5432,
                 user: str = "postgres", password: str = "",
                 database: str = "ecommerce"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            import pg8000
        except ImportError:
            raise ImportError("pg8000 is required for PostgreSQL. Install with: pip install pg8000")
        
        self.connection = pg8000.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


def get_table_info(connector) -> List[Dict]:
    """Get information about all tables in the database."""
    pass


def get_columns(connector, table_name: str) -> List[str]:
    """Get column names for a table."""
    conn = connector.connect()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})" if isinstance(connector, SQLiteConnector) 
                   else f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    
    if isinstance(connector, SQLiteConnector):
        columns = [row[1] for row in cursor.fetchall()]
    else:
        columns = [row[0] for row in cursor.fetchall()]
    
    connector.close()
    return columns