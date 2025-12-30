"""Database adapter layer for exporting data to various SQL backends."""

import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


# Notion type to SQL type mapping
NOTION_TO_SQL_TYPE: Dict[str, str] = {
    "title": "TEXT",
    "rich_text": "TEXT",
    "number": "REAL",
    "checkbox": "BOOLEAN",
    "date": "TIMESTAMP",
    "select": "TEXT",
    "multi_select": "TEXT",
    "url": "TEXT",
    "email": "TEXT",
    "phone_number": "TEXT",
    "status": "TEXT",
    "created_time": "TIMESTAMP",
    "last_edited_time": "TIMESTAMP",
    "formula": "TEXT",
    "rollup": "TEXT",
}


def notion_type_to_sql(notion_type: str) -> str:
    """Convert a Notion property type to a SQL column type."""
    return NOTION_TO_SQL_TYPE.get(notion_type, "TEXT")


def sanitize_column_name(name: str) -> str:
    """Sanitize a column name for SQL (replace spaces, special chars)."""
    # Replace spaces and special chars with underscores
    sanitized = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
    # Ensure doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    # Truncate to PostgreSQL limit of 63 characters
    sanitized = sanitized[:63]
    return sanitized.lower()


# PostgreSQL reserved words that need quoting
RESERVED_WORDS = {
    'column', 'table', 'index', 'type', 'limit', 'order', 'group', 'where', 
    'select', 'from', 'to', 'primary', 'key', 'default', 'check', 'constraint', 
    'references', 'user', 'role', 'session', 'action', 'do', 'limit'
}


def quote_column_name(name: str) -> str:
    """Quote column name if it's a PostgreSQL reserved word."""
    if name.lower() in RESERVED_WORDS:
        return f'"{name}"'
    return name


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass

    @abstractmethod
    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        """Create a table based on Notion schema.
        
        Args:
            table_name: Name of the table to create
            schema: Dict mapping column names to Notion types
        """
        pass

    @abstractmethod
    def insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> int:
        """Insert rows into the table.
        
        Args:
            table_name: Name of the table
            rows: List of row dictionaries
            
        Returns:
            Number of rows inserted
        """
        pass

    def __enter__(self) -> "DatabaseAdapter":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "notion_page_id TEXT"]
        for col_name, notion_type in schema.items():
            safe_name = sanitize_column_name(col_name)
            sql_type = notion_type_to_sql(notion_type)
            # SQLite uses INTEGER for BOOLEAN
            if sql_type == "BOOLEAN":
                sql_type = "INTEGER"
            columns.append(f"{safe_name} {sql_type}")
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.conn.execute(create_sql)
        self.conn.commit()

    def insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> int:
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        if not rows:
            return 0
        
        # Get column names from first row (excluding internal _page_id)
        sample = rows[0]
        col_names = [sanitize_column_name(k) for k in sample.keys() if k != "_page_id"]
        col_names.insert(0, "notion_page_id")
        
        placeholders = ", ".join(["?" for _ in col_names])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
        
        count = 0
        for row in rows:
            values = [row.get("_page_id")]
            for k in sample.keys():
                if k != "_page_id":
                    values.append(row.get(k))
            self.conn.execute(insert_sql, values)
            count += 1
        
        self.conn.commit()
        return count


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter using psycopg2."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn: Any = None

    def connect(self) -> None:
        try:
            import psycopg2
        except ImportError:
            raise ImportError("psycopg2 is required for PostgreSQL. Install with: pip install psycopg2-binary")
        
        self.conn = psycopg2.connect(self.connection_string)

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        columns = ["id SERIAL PRIMARY KEY", "notion_page_id TEXT"]
        for col_name, notion_type in schema.items():
            safe_name = sanitize_column_name(col_name)
            sql_type = notion_type_to_sql(notion_type)
            columns.append(f"{safe_name} {sql_type}")
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        
        with self.conn.cursor() as cur:
            cur.execute(create_sql)
        self.conn.commit()

    def insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> int:
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        if not rows:
            return 0
        
        sample = rows[0]
        col_names = [sanitize_column_name(k) for k in sample.keys() if k != "_page_id"]
        col_names.insert(0, "notion_page_id")
        
        placeholders = ", ".join(["%s" for _ in col_names])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
        
        count = 0
        with self.conn.cursor() as cur:
            for row in rows:
                values = [row.get("_page_id")]
                for k in sample.keys():
                    if k != "_page_id":
                        values.append(row.get(k))
                cur.execute(insert_sql, values)
                count += 1
        
        self.conn.commit()
        return count


class SupabaseAdapter(DatabaseAdapter):
    """Supabase database adapter using supabase-py."""

    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.client: Any = None

    def connect(self) -> None:
        try:
            from supabase import create_client
        except ImportError:
            raise ImportError("supabase is required for Supabase. Install with: pip install supabase")
        
        self.client = create_client(self.url, self.key)

    def close(self) -> None:
        # Supabase client doesn't require explicit close
        self.client = None

    def create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        # Supabase doesn't support DDL via the REST API
        # Tables must be created via the Supabase dashboard or SQL Editor
        # We'll generate and print the SQL for the user
        columns = ["id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY", "notion_page_id TEXT"]
        for col_name, notion_type in schema.items():
            safe_name = sanitize_column_name(col_name)
            sql_type = notion_type_to_sql(notion_type)
            columns.append(f"{safe_name} {sql_type}")
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        print(f"\n[Supabase] Create this table in your Supabase SQL Editor:\n{create_sql}\n")

    def insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> int:
        if not self.client:
            raise RuntimeError("Not connected to Supabase")
        
        if not rows:
            return 0
        
        # Transform rows for Supabase (sanitize column names)
        # Note: Supabase REST API handles reserved words automatically when using the client
        transformed = []
        for row in rows:
            new_row = {"notion_page_id": row.get("_page_id")}
            for k, v in row.items():
                if k != "_page_id":
                    safe_name = sanitize_column_name(k)
                    new_row[safe_name] = v
            transformed.append(new_row)
        
        # Supabase insert in batches
        batch_size = 100
        count = 0
        for i in range(0, len(transformed), batch_size):
            batch = transformed[i:i + batch_size]
            self.client.table(table_name).insert(batch).execute()
            count += len(batch)
        
        return count


def get_adapter(target: str, connection_string: str) -> DatabaseAdapter:
    """Factory function to get the appropriate database adapter.
    
    Args:
        target: One of 'sqlite', 'postgres', 'supabase'
        connection_string: Connection string or path
            - sqlite: path to .db file
            - postgres: postgresql://user:pass@host:port/db
            - supabase: url|key (pipe-separated)
    
    Returns:
        DatabaseAdapter instance
    """
    target = target.lower()
    
    if target == "sqlite":
        return SQLiteAdapter(connection_string)
    
    if target in ("postgres", "postgresql"):
        return PostgreSQLAdapter(connection_string)
    
    if target == "supabase":
        if "|" not in connection_string:
            raise ValueError("Supabase connection string must be: url|key")
        url, key = connection_string.split("|", 1)
        return SupabaseAdapter(url.strip(), key.strip())
    
    raise ValueError(f"Unknown target database: {target}. Supported: sqlite, postgres, supabase")

