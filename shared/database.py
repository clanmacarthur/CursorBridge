"""Supabase database client and shared utilities."""

import os
from typing import Any, Dict, List, Optional
from functools import lru_cache


def get_supabase_client():
    """Get a Supabase client instance."""
    try:
        from supabase import create_client
    except ImportError:
        raise ImportError("supabase is required. Install with: pip install supabase")
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
    
    return create_client(url, key)


class DatabaseService:
    """Service for querying the Supabase database."""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    # =========================================================================
    # Generic CRUD operations
    # =========================================================================
    
    def get_all(self, table: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get all rows from a table."""
        response = self.client.table(table).select("*").limit(limit).execute()
        return response.data
    
    def get_by_id(self, table: str, id: int) -> Optional[Dict[str, Any]]:
        """Get a single row by ID."""
        response = self.client.table(table).select("*").eq("id", id).execute()
        return response.data[0] if response.data else None
    
    def get_by_notion_id(self, table: str, notion_page_id: str) -> Optional[Dict[str, Any]]:
        """Get a single row by Notion page ID."""
        response = self.client.table(table).select("*").eq("notion_page_id", notion_page_id).execute()
        return response.data[0] if response.data else None
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a row into a table."""
        response = self.client.table(table).insert(data).execute()
        return response.data[0] if response.data else {}
    
    def update(self, table: str, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a row by ID."""
        response = self.client.table(table).update(data).eq("id", id).execute()
        return response.data[0] if response.data else {}
    
    def delete(self, table: str, id: int) -> bool:
        """Delete a row by ID."""
        self.client.table(table).delete().eq("id", id).execute()
        return True
    
    # =========================================================================
    # Domain-specific queries
    # =========================================================================
    
    def get_attribute_taxonomy(self) -> List[Dict[str, Any]]:
        """Get the full attribute taxonomy."""
        return self.get_all("attribute_taxonomy")
    
    def get_programme_profiles(self) -> List[Dict[str, Any]]:
        """Get all programme profiles."""
        return self.get_all("programme_profiles")
    
    def get_session_templates(self) -> List[Dict[str, Any]]:
        """Get all session templates."""
        return self.get_all("session_templates")
    
    def get_safety_rules(self) -> List[Dict[str, Any]]:
        """Get all safety rules."""
        return self.get_all("safety_rules")
    
    def get_breath_library(self) -> List[Dict[str, Any]]:
        """Get the breath protocol library."""
        return self.get_all("breath_library")
    
    def get_movements(self) -> List[Dict[str, Any]]:
        """Get the movements library."""
        return self.get_all("movements_system")
    
    def get_archetypal_personas(self) -> List[Dict[str, Any]]:
        """Get archetypal personas (styles)."""
        return self.get_all("archetypal_personas")
    
    def get_dashboard_blocks(self) -> List[Dict[str, Any]]:
        """Get dashboard block definitions."""
        return self.get_all("dashboard_blocks")
    
    def get_rules_gating(self) -> List[Dict[str, Any]]:
        """Get gating rules."""
        return self.get_all("rules_gating")


# Singleton instance
_db_service: Optional[DatabaseService] = None


def get_db() -> DatabaseService:
    """Get the database service singleton."""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service



