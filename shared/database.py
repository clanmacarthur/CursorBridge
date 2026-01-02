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
    
    # =========================================================================
    # Lens System - Evidence & Techniques
    # =========================================================================
    
    def get_evidence_sources(self) -> List[Dict[str, Any]]:
        """Get all evidence sources."""
        return self.get_all("evidence_sources")
    
    def get_techniques(self) -> List[Dict[str, Any]]:
        """Get all techniques with lens templates."""
        return self.get_all("techniques")
    
    def get_technique_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a technique by name."""
        response = self.client.table("techniques").select("*").ilike("technique", f"%{name}%").execute()
        return response.data[0] if response.data else None
    
    def get_techniques_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get techniques by category."""
        response = self.client.table("techniques").select("*").eq("technique_category", category).execute()
        return response.data
    
    def get_techniques_by_lens(self, lens: str) -> List[Dict[str, Any]]:
        """Get techniques available in a specific lens (Western, TCM, Hybrid)."""
        response = self.client.table("techniques").select("*").ilike("lens_availability", f"%{lens}%").execute()
        return response.data
    
    # =========================================================================
    # Lens Registry
    # =========================================================================
    
    def get_all_lenses(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all lens definitions."""
        query = self.client.table("lens_definitions").select("*").order("sort_order")
        if active_only:
            query = query.eq("is_active", True)
        response = query.execute()
        return response.data
    
    def get_lens_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get a lens definition by slug."""
        response = self.client.table("lens_definitions").select("*").eq("lens_slug", slug).execute()
        return response.data[0] if response.data else None
    
    def get_technique_lens_explanations(self, technique_id: int) -> List[Dict[str, Any]]:
        """Get all lens explanations for a technique."""
        response = self.client.table("technique_lens_explanations").select("*, lens_definitions(*)").eq("technique_id", technique_id).execute()
        return response.data
    
    def get_user_lens_preferences(self, user_id: str) -> List[Dict[str, Any]]:
        """Get a user's lens preferences."""
        response = self.client.table("user_lens_preferences").select("*, lens_definitions(*)").eq("user_id", user_id).order("preference_level", desc=True).execute()
        return response.data
    
    def update_user_lens_context(self, user_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update or insert user lens context for today."""
        from datetime import date
        context_data["user_id"] = user_id
        context_data["context_date"] = date.today().isoformat()
        
        # Upsert (insert or update)
        response = self.client.table("user_lens_context").upsert(
            context_data, 
            on_conflict="user_id,context_date"
        ).execute()
        return response.data[0] if response.data else {}


# Singleton instance
_db_service: Optional[DatabaseService] = None


def get_db() -> DatabaseService:
    """Get the database service singleton."""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service






